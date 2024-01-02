from src.containers.container import Container
from src.domain.user.interfaces import ICreateFeedBack
from tests.factories.event import ConversationFactory, EventFactory, Response


async def test_feedback(container: Container) -> None:
    use_case: ICreateFeedBack = container.use_cases.create_feedback()
    event = EventFactory()

    async def get_response() -> Response:
        return Response("Feedback1")

    conv = ConversationFactory(event, get_response)

    await use_case(event, conv)

    assert event.messages == [(("Внимательно слушаю :)",), {}), (("Спасибо за отзыв!",), {})]
