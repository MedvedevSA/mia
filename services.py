from typing import TypeVar

from pydantic import BaseModel
from repositories import SQLAlchemyRepository

Model = TypeVar('Model', bound='BaseModel')
ParamsModel = TypeVar('ParamsModel', bound='BaseModel')
ResponseModel = TypeVar('ResponseModel', bound='BaseModel')


class BaseService:
    def __init__(self, repository: type[SQLAlchemyRepository]):
        self.repository = repository()

    async def add_one(self, obj: Model) -> int:
        return await self.repository.add_one(
            obj.model_dump()
        )

    async def get_one(
            self,
            id: int,
            response_model: ResponseModel
    ) -> ResponseModel | None:
        row = await self.repository.get_one(id)
        if row:
            return response_model.model_validate(row, from_attributes=True)

    async def get_all(
            self,
            params: ParamsModel = None,
            response_model: type[ResponseModel] = None
    ) -> list[ResponseModel]:
        relations = None
        if params:
            relations = params.model_config.get('relation_prefix')
            params = {k: v for k, v in params.model_dump().items() if v is not None}
        rows = await self.repository.get_all(params, relations)
        return [response_model.model_validate(row, from_attributes=True) for row in rows]

    async def get_last(
            self,
            params: ParamsModel = None,
            response_model: type[ResponseModel] = None
    ) -> ResponseModel:
        if params:
            params = {k: v for k, v in params.model_dump().items() if v is not None}
        row = await self.repository.get_last(params)
        if row:
            return response_model.model_validate(row)

    async def update_one(self, id: int, obj: Model) -> int:
        return await self.repository.update_one(
            id, obj.model_dump()
        )

    async def patch_one(self, id: int, obj: Model) -> int:
        return await self.repository.update_one(id, obj.model_dump(exclude_unset=True))

    async def del_one(self, id: int) -> int:
        return await self.repository.del_one(id)
