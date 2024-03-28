from abc import ABC, abstractmethod

from esturide_api.contexts.user.domain.errors import UserServiceValidationError


class ValidationRule(ABC):
    @abstractmethod
    def validate(self):
        pass


class UserExistsRule(ValidationRule):
    def __init__(self, user_repository, user_id: int):
        self.user_repository = user_repository
        self.user_id = user_id

    def validate(self):
        if not self.user_repository.get_user_by_id(self.user_id):
            raise UserServiceValidationError(
                f"User with id {self.user_id} was not found"
            )


class UniqueEmailRule(ValidationRule):
    def __init__(self, user_repository, email: str):
        self.user_repository = user_repository
        self.email = email

    def validate(self):
        if self.user_repository.get_user_by_email(self.email):
            raise UserServiceValidationError(
                f"Email {self.email} is already registered"
            )


class UniqueCURPRule(ValidationRule):
    def __init__(self, user_repository, curp: str):
        self.user_repository = user_repository
        self.curp = curp

    def validate(self):
        if self.user_repository.get_user_by_curp(self.curp):
            raise UserServiceValidationError(f"CURP {self.curp} is already registered")
