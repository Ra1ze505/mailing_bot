from datetime import datetime

import factory

from src.data.models.rate import Rate
from tests.async_alchemy_factory import AsyncSQLAlchemyModelFactory

FAKE_RATE_DATA = {
    "EUR": {
        "CharCode": "EUR",
        "ID": "R01239",
        "Name": "Евро",
        "Nominal": 1,
        "NumCode": "978",
        "Previous": 101.3451,
        "Value": 100.5506,
    },
    "USD": {
        "CharCode": "USD",
        "ID": "R01235",
        "Name": "Доллар США",
        "Nominal": 1,
        "NumCode": "840",
        "Previous": 91.7051,
        "Value": 90.3041,
    },
}


class RateFactory(AsyncSQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    data = FAKE_RATE_DATA
    date = factory.Sequence(lambda _: datetime.now())

    class Meta:
        model = Rate
