from esturide_api.contexts.user.domain.repository.user_repository import UserRepository
from esturide_api.contexts.user.domain.validation.validation_rules import ValidationRule


def validation_rule_factory(user_repository: UserRepository):
    def create_rule(rule_class: ValidationRule, *args, **kwargs):
        return rule_class(user_repository, *args, **kwargs)

    return create_rule
