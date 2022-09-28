from dependency_injector import containers, providers

from src.common.db import Database
from src.data.repositories.user import UserRepository


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db: providers.Provider[Database] = providers.Dependency()
    gateways = providers.DependenciesContainer()

    user_repo = providers.Factory(UserRepository, db=db)
