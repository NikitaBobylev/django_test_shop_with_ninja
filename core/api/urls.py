from django.urls import path
from ninja import NinjaAPI
from .v1.urls import router as v1_router
from core.api.schemas import PingResponseSchema

api = NinjaAPI()


@api.get("/ping", response=PingResponseSchema)
def ping(request) -> dict:
    return {"result": True}


api.add_router('v1/', v1_router)
urlpatterns = [
    path('', api.urls)
]
