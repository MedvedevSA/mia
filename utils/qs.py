from urllib.parse import parse_qs

from fastapi import Body


def converted_qs(body: bytes = Body()):
    return convert_qs(parse_qs(body.decode()))


def convert_qs(body: dict) -> dict:
    converted = {}
    for field_pattern, val in body.items():
        val = val[0] if val else val
        field_pattern = field_pattern.split('__')

        current = converted
        for idx, name in enumerate(field_pattern):
            if idx == len(field_pattern) - 1:
                current[name] = val
            else:
                current[name] = current.get(name, {})
                current = current[name]

        list_keys = [fld for fld in converted.keys() if fld[-1].isdigit()]
        for key in list_keys:
            parent_schema = key[:-1]
            if parent_schema not in converted:
                converted[parent_schema] = list()
            converted[key[:-1]].append(converted.pop(key))
    return converted
