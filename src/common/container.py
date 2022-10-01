from dependency_injector import containers, providers


class BaseAppContainer(containers.DeclarativeContainer):
    config: providers.Configuration
    wiring_config: containers.WiringConfiguration
    repos: providers.Container
    use_cases: providers.Container
    gateways: providers.Container
