from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.controllers.event_driven_controller import EventDrivenController
from src.controllers.rest_controller import RestController


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    edc = EventDrivenController()
    edc.start()
    try:
        yield
    finally:
        edc.stop()

app = FastAPI(lifespan=lifespan)

rest_controller = RestController()
app.include_router(rest_controller.router, prefix="/water-systems", tags=["Water Systems"])

