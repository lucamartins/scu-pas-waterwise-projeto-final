from typing import List

from fastapi import APIRouter

from src.application.services.rest.rest_service import RestService
from src.domain.entities.water_system import WaterSystem


class RestController:
    def __init__(self):
        command_service = RestService()
        self.router = APIRouter()
        self.router.post("", response_model=str)(command_service.create_water_system)
        self.router.get("/{water_system_id}", response_model=WaterSystem)(command_service.get_water_system)
        self.router.put("/{water_system_id}", response_model=int)(command_service.update_water_system)
        self.router.delete("/{water_system_id}", response_model=int)(command_service.delete_water_system)
        self.router.get("", response_model=List[WaterSystem])(command_service.list_water_systems)
