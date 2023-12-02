import logging
from typing import Callable, TypeVar, Any

from sqlalchemy import (
    insert, select, update, delete, cast, text, func,
    String, Select, BinaryExpression
)
from sqlalchemy.orm import InstrumentedAttribute, DeclarativeBase
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.inspection import inspect

from database import async_session, Base
from models.customer import Customer
from models.tasks import Task
from utils.config_dict import AnnotateJoin
from utils.paging import PagingModel
from utils.sorting import SortOrderParam, SortOrder

logger = logging.getLogger("uvicorn")

Dump = TypeVar('Dump', bound=dict[str, Any])


suffixes: dict[str, Callable] = {
    '__neq': lambda col, val: col != val,
    '__eq': lambda col, val: col == val,
    '__ge': lambda col, val: col >= val,
    '__le': lambda col, val: col <= val,
    '__gt': lambda col, val: col > val,
    '__lt': lambda col, val: col < val,
}


def add_suffix(suffix: str) -> Callable:
    def decorator(func) -> Callable:
        suffixes['__' + suffix] = func
        return func

    return decorator


@add_suffix('ilike')
def ilike(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return cast(col, String).ilike(f'%{str(fld_val)}%')


@add_suffix('in')
def in_(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    return col.in_(fld_val)


@add_suffix('is_none')
def is_none(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression:
    if fld_val:
        return col.is_(None)
    return col.is_not(None)


@add_suffix('text_ilike')
def json_text_ilike(col: InstrumentedAttribute, fld_val: Any) -> BinaryExpression | None:
    fld_text = get_json_field(col, 'text')

    if isinstance(fld_text, BinaryExpression):
        return fld_text.cast(String).ilike(f"%{fld_val}%")
    else:
        logger.warning(
            f'{fld_text.name=} is not {BinaryExpression}'
        )


def get_json_field(col: InstrumentedAttribute, key: str) -> BinaryExpression:
    try:
        col = col[key].astext
        return col
    except NotImplementedError:
        logger.warning(
            f'{col.name=}[\'{key}\'] not implemented'
        )
    except AttributeError:
        logger.warning(
            f'{col.name=} has no attr \'astext\''
        )


def get_model_col(model: Base, fld: str) -> InstrumentedAttribute | None:
    try:
        column = getattr(model, fld)
        if isinstance(column, InstrumentedAttribute):
            return column

    except AttributeError:
        logger.warning(
            f"{__name__}.{get_model_col.__name__}:\n{model} has no attr \"{fld}\""
        )


class SelectGenerator:
    def __init__(
            self,
            model: Base,
            params: Dump = None,
            relations: dict[str, AnnotateJoin] = None
    ):
        self.model = model
        self.params = params or {}
        self.relations = relations or {}

    def get_stmt(
        self,
        sort_order: SortOrder = None,
        paging: bool = True
    ) -> Select:
        stmt = self.join_relations(
            select(self.model)
        ).where(
            *self.where_from_params()
        )
        for pk_col in inspect(self.model).primary_key:
            stmt = stmt.group_by(pk_col)

        order_expr = self.parse_sorting(sort_order)
        if isinstance(order_expr, UnaryExpression):
            stmt = stmt.order_by(order_expr)

        if paging:
            offset, limit = self.parse_paging()
            stmt = stmt.offset(offset).limit(limit)
        return stmt

    def join_relations(self, stmt: Select) -> Select:
        for annotate_join in self.relations.values():
            join_args = dict(target=annotate_join['model'])
            if 'onclause' in annotate_join:
                join_args['onclause'] = annotate_join['onclause']
            stmt = stmt.outerjoin(**join_args)
        return stmt

    def where_from_params(self) -> list[BinaryExpression]:
        where = [self.parse_param(_fld, val) for _fld, val in self.params.items()]
        return [el for el in where if isinstance(el, BinaryExpression)]

    def parse_prefix(self, fld: str) -> tuple[Base, str]:
        for prefix, annotate_join in self.relations.items():
            prefix += '__'
            if fld.startswith(prefix):
                return annotate_join['model'], fld.removeprefix(prefix)
        return self.model, fld

    def parse_param(self, fld: str, val: Any) -> BinaryExpression | None:
        model, fld = self.parse_prefix(fld)

        for suffix, fn in suffixes.items():
            if fld.endswith(suffix):
                if col := get_model_col(model, fld.removesuffix(suffix)):
                    return fn(col, val)

        if fld not in [
            *PagingModel.model_fields,
            *SortOrderParam.model_fields
        ]:
            if col := get_model_col(model, fld):
                return col == val

    def parse_sorting(self, sort_order: SortOrder = None) -> UnaryExpression | None:
        sorting = SortOrderParam.model_validate(self.params)

        def get_first_pk_col():
            for pk_col in inspect(self.model).primary_key:
                return pk_col

        col = get_first_pk_col()
        if sorting.sort_col:
            col = get_model_col(self.model, sorting.sort_col) or col

        expr_key = sorting.sort_order
        if sort_order and hasattr(col, sort_order):
            expr_key = sort_order
        return getattr(col, expr_key, col.asc)()

    def parse_paging(self) -> tuple[int, int]:
        pg = PagingModel.model_validate(self.params)

        def offset(pg: PagingModel) -> int:
            return (pg.page_number - 1) * pg.page_limit
        return offset(pg), pg.page_limit


class SQLAlchemyRepository:
    model: DeclarativeBase = None

    async def add_one(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_one(self, id: Any):
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            return (await session.execute(stmt)).scalar()

    async def update_one(self, id: Any, data: dict):
        async with async_session() as session:
            stmt = update(self.model).where(
                self.model.id == id
            ).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    async def get_all(self, params: Dump = None, relations: dict = None):
        async with async_session() as session:
            stmt = SelectGenerator(self.model, params, relations).get_stmt()
            return (await session.execute(stmt)).scalars()

    async def get_last(self, params: Dump = None):
        async with async_session() as session:
            stmt = SelectGenerator(
                self.model, params
            ).get_stmt(
                sort_order='desc',
                paging=False
            ).limit(1)
            return (await session.execute(stmt)).scalar()

    async def del_one(self, id):
        async with async_session() as session:
            stmt = delete(self.model).where(
                self.model.id == id
            ).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()


class CustomerRepository(SQLAlchemyRepository):
    model = Customer


class TaskRepository(SQLAlchemyRepository):
    model = Task

    async def get_order_count(self):
        stmt = select(func.count(Task.id))
        async with async_session() as session:
            return (await session.execute(stmt)).scalar()

    async def add_one(self, data: dict):
        def order_details_values(order_detail: dict, args: dict, idx: int) -> str:
            descr_key = "descr" + str(idx)
            cost_key = "cost" + str(idx)
            args[descr_key] = order_detail["description"]
            args[cost_key] = order_detail["cost"]
            return f'((select id from new_order), :{descr_key}, :{cost_key})'

        args = dict(
            customer_id=data["customer_id"],
            due_date=data["due_date"],
        )
        values = [
            order_details_values(order_detail, args, idx)
            for idx, order_detail
            in enumerate(data["order_details"])
        ]
        insert_order_with_details = f"""
            WITH new_order AS (
                INSERT INTO "order"
                (customer_id, due_date, "comment")
                VALUES(:customer_id, :due_date, '') RETURNING "order".id
            )
            INSERT INTO order_detail (order_id, description, "cost")
            VALUES {', '.join(values)}
            RETURNING (select id from new_order)
        """
        async with async_session() as session:
            res = (await session.execute(text(insert_order_with_details), args)).scalar()
            await session.commit()

        return res

