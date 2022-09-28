from dependency_injector import containers, providers

from src.domain.handlers.use_cases.start import StartHandler


class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repos = providers.DependenciesContainer()

    start_handler = providers.Factory(StartHandler, user_repo=repos.user_repo, config=config.app)
