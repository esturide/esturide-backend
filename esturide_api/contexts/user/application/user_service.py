from typing import List

from esturide_api.contexts.user.domain.model.user_model import (
    UserCreate,
    UserOut,
    UserUpdatePatch,
    UserUpdatePut,
)
from esturide_api.contexts.user.domain.service.user_domain_service import UserService


class UserApplicationService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user(
        self,
        user_id: int,
    ) -> UserOut:
        return self.user_service.get_user(user_id)

    def get_users(self) -> List[UserOut]:
        return self.user_service.get_users()

    def delete_user(
        self,
        user_id: int,
    ):
        return self.user_service.delete_user(user_id)

    def update_user_put(self, user_id: int, updated_data: UserUpdatePut) -> UserOut:
        return self.user_service.update_user_put(user_id, updated_data)

    def create_user(self, created_data: UserCreate) -> UserOut:
        return self.user_service.create_user(created_data)

    def update_user_patch(self, user_id: int, updated_data: UserUpdatePatch) -> UserOut:
        return self.user_service.update_user_patch(user_id, updated_data)
