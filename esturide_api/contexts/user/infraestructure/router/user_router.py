from typing import List

from fastapi import APIRouter, Depends, status

from esturide_api.contexts.user.application.service.user_service import (
    UserApplicationService,
)
from esturide_api.contexts.user.depencencies import get_user_application_service
from esturide_api.contexts.user.domain.model.user_model import (
    UserCreate,
    UserOut,
    UserUpdatePatch,
    UserUpdatePut,
)
from esturide_api.shared.authentication.dependencies import get_request_user

router = APIRouter(prefix="/v2/users", tags=["Users"])


@router.get("/{id}", response_model=UserOut)
def get_user(
    id: int,
    user_app_service: UserApplicationService = Depends(get_user_application_service),
    current_user=Depends(get_request_user),
):
    return user_app_service.get_user(id)


@router.get("/", response_model=List[UserOut])
def get_users(
    user_app_service: UserApplicationService = Depends(get_user_application_service),
    current_user=Depends(get_request_user),
):
    return user_app_service.get_users()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(
    user: UserCreate,
    user_app_service: UserApplicationService = Depends(get_user_application_service),
):
    return user_app_service.create_user(user)


@router.put("/{id}", response_model=UserOut)
def update_user_put(
    id: int,
    updated_data: UserUpdatePut,
    user_app_service: UserApplicationService = Depends(get_user_application_service),
    current_user=Depends(get_request_user),
):
    return user_app_service.update_user_put(id, updated_data)


@router.patch("/{id}", response_model=UserOut)
def udpate_user_patch(
    id: int,
    updated_data: UserUpdatePatch,
    user_app_service: UserApplicationService = Depends(get_user_application_service),
    current_user=Depends(get_request_user),
):
    return user_app_service.update_user_patch(id, updated_data)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    id: int,
    user_app_service: UserApplicationService = Depends(get_user_application_service),
    current_user=Depends(get_request_user),
):
    return user_app_service.delete_user(id)
