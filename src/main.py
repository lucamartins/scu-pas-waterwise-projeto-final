from fastapi import FastAPI

from src.controllers.rest_controller import RestController

app = FastAPI()

rest_controller = RestController()
app.include_router(rest_controller.router, prefix="/water-systems", tags=["Water Systems"])

