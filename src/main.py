from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from src.application.services.processing_pipeline.processing_pipeline_service import ProcessingPipelineService
from src.controllers.event_driven_controller import EventDrivenController
from src.controllers.rest_controller import RestController

task_scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    edc = EventDrivenController()
    edc.start()

    processing_pipeline_service = ProcessingPipelineService()
    task_scheduler.add_job(processing_pipeline_service.run, "interval", seconds=15)
    task_scheduler.start()
    try:
        yield
    finally:
        edc.stop()
        task_scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
rest_controller = RestController()
app.include_router(rest_controller.router, prefix="/water-systems", tags=["Water Systems"])

