from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from esturide_api.config.database import get_db
from esturide_api.contexts.user.domain.model.user_model import UserOut
from esturide_api.contexts.user.domain.repository.user_repository import UserRepository
from esturide_api.contexts.user.infraestructure.database.db_user_repository import (
    UserPostgresRepository,
)
from esturide_api.shared.authentication.application.authentication_service import (
    AuthenticationApplicationService,
)
from esturide_api.shared.authentication.domain.service.authentication_domain_service import (
    AuthenticationService,
)
from esturide_api.shared.authentication.infraestructure.oauth import PasswordHandler


def get_user_repository(db: Session = Depends(get_db)):
    return UserPostgresRepository(db)


def get_authentication_application_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthenticationApplicationService:
    return AuthenticationApplicationService(
        AuthenticationService(
            user_repository,
            PasswordHandler(),
        ),
    )


def get_request_user(
    token: OAuth2PasswordBearer = Depends(OAuth2PasswordBearer(tokenUrl="v2/login")),
    authentication_service: AuthenticationApplicationService = Depends(
        get_authentication_application_service
    ),
) -> UserOut:
    return authentication_service.get_request_user(token)
