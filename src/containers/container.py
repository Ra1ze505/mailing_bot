from dependency_injector import containers, providers

from src.common.container import BaseAppContainer
from src.config import Settings
from src.containers.gateways import Gateways
from src.containers.repos_container import ReposContainer
from src.containers.use_cases import UseCasesContainer

app_config = Settings()


class Container(BaseAppContainer):
    config: providers.Configuration
    wiring_config: containers.WiringConfiguration
    repos: providers.Container
    use_cases: providers.Container
    gateways: providers.Container

    config = providers.Configuration(pydantic_settings=[app_config])
    gateways = providers.Container(Gateways, config=config)
    repos = providers.Container(ReposContainer, config=config, db=gateways.db, gateways=gateways)
    use_cases = providers.Container(UseCasesContainer, repos=repos, config=config)


container = Container()
