from fastapi import Depends, HTTPException

from src.application.services.rest.rest_service_dtos import WaterSystemCreateUpdateRequest
from src.domain.entities.water_system import WaterSystem
from src.domain.repositories.water_system_repository import WaterSystemRepository


def get_repository() -> WaterSystemRepository:
    return WaterSystemRepository()


class RestService:
    @staticmethod
    async def create_water_system(
            water_system_req: WaterSystemCreateUpdateRequest, repository: WaterSystemRepository = Depends(get_repository)
    ):
        """Cria um novo WaterSystem."""
        water_system = WaterSystem(
            name=water_system_req.name,
            location=water_system_req.location,
            capacityCubicMeters=water_system_req.capacity,
            system_type=water_system_req.system_type,
            sensors=water_system_req.sensors,
            twinning_rate_seconds=water_system_req.twinning_rate_seconds
        )
        water_system_id = await repository.create_water_system(water_system)
        return water_system_id

    @staticmethod
    async def get_water_system(
            water_system_id: str, repository: WaterSystemRepository = Depends(get_repository)
    ):
        """Retorna um WaterSystem pelo ID."""
        result = await repository.get_water_system_by_id(water_system_id)
        if not result:
            raise HTTPException(status_code=404, detail="WaterSystem not found")
        return result

    @staticmethod
    async def update_water_system(
            water_system_id: str,
            water_system_req: WaterSystemCreateUpdateRequest,
            repository: WaterSystemRepository = Depends(get_repository),
    ):
        """Atualiza um WaterSystem pelo ID."""
        updated_count = await repository.update_water_system(water_system_id, water_system_req)
        if updated_count == 0:
            raise HTTPException(status_code=404, detail="WaterSystem not found")
        return updated_count

    @staticmethod
    async def delete_water_system(
            water_system_id: str, repository: WaterSystemRepository = Depends(get_repository)
    ):
        """Deleta um WaterSystem pelo ID."""
        deleted_count = await repository.delete_water_system(water_system_id)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="WaterSystem not found")
        return deleted_count

    @staticmethod
    async def list_water_systems(
            repository: WaterSystemRepository = Depends(get_repository)
    ):
        """Lista todos os WaterSystems."""
        return await repository.list_water_systems()
