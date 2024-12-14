from typing import List


class ObjectUtil:
    @staticmethod
    def remove_fields(obj: dict, fields: List[str]) -> dict:
        """Remove campos de um objeto."""
        return {k: v for k, v in obj.items() if k not in fields}
