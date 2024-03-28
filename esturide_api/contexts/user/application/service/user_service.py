from typing import List

from esturide_api.contexts.user.application.service.validation_rule_factory import (
    validation_rule_factory,
)
from esturide_api.contexts.user.domain.model.user_model import (
    UserCreate,
    UserOut,
    UserUpdatePatch,
    UserUpdatePut,
)
from esturide_api.contexts.user.domain.repository.user_repository import UserRepository
from esturide_api.contexts.user.domain.validation.validation_rules import (
    UniqueCURPRule,
    UniqueEmailRule,
    UserExistsRule,
)


class UserApplicationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.create_validation_rule = validation_rule_factory(self.user_repository)

    def _execute_validations(self, rules):
        for rule in rules:
            rule.validate()

    def get_user(self, user_id: int) -> UserOut:
        return self.user_repository.get_user_by_id(user_id)

    def get_users(self) -> List[UserOut]:
        return self.user_repository.get_all_users()

    def create_user(self, created_data: UserCreate) -> UserOut:
        validations = [
            self.create_validation_rule(UniqueEmailRule, created_data.email),
            self.create_validation_rule(UniqueCURPRule, created_data.curp),
        ]
        self._execute_validations(validations)

        return self.user_repository.create_user(created_data)

    def update_user_put(self, user_id: int, updated_data: UserUpdatePut) -> UserOut:
        validations = [
            self.create_validation_rule(UserExistsRule, user_id),
            self.create_validation_rule(UniqueEmailRule, updated_data.email),
            self.create_validation_rule(UniqueCURPRule, updated_data.curp),
        ]
        self._execute_validations(validations)

        return self.user_repository.update_user(user_id, updated_data)

    def update_user_patch(self, user_id: int, updated_data: UserUpdatePatch) -> UserOut:
        validations = [
            self.create_validation_rule(UserExistsRule, user_id),
            self.create_validation_rule(UniqueEmailRule, updated_data.email),
            self.create_validation_rule(UniqueCURPRule, updated_data.curp),
        ]
        self._execute_validations(validations)

        return self.user_repository.update_user(user_id, updated_data)

    def delete_user(self, user_id: int):
        validations = [
            self.create_validation_rule(UserExistsRule, user_id),
        ]
        self._execute_validations(validations)

        self.user_repository.delete_user(user_id)
        return {"message": f"User with id {user_id} was successfully deleted"}
