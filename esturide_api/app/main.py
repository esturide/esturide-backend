from fastapi import FastAPI, HTTPException

from esturide_api import models
from esturide_api.config.database import engine
from esturide_api.contexts.user.domain.errors import UserServiceValidationError
from esturide_api.contexts.user.infraestructure.router.user_router import (
    router as V2_UserRouter,
)
from esturide_api.routers.auth import router as AuthorizationRouter
from esturide_api.routers.automobile import router as AutomobileRouter
from esturide_api.routers.drivers import router as DriverRouter
from esturide_api.routers.populate_db import router as DBRouter
from esturide_api.routers.user import router as UserRouter
from esturide_api.shared.authentication.infraestructure.router.authentication_router import (
    router as V2_AuthorizationRouter,
)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(UserRouter)
app.include_router(AuthorizationRouter)
app.include_router(DriverRouter)
app.include_router(AutomobileRouter)
app.include_router(DBRouter)
app.include_router(V2_UserRouter)
app.include_router(V2_AuthorizationRouter)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(UserServiceValidationError)
def user_service_validation_exception_handler(request, exc: UserServiceValidationError):
    raise HTTPException(status_code=400, detail=str(exc))
