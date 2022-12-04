from src.common.repo.base import BaseRepository
from src.data.models.rate import Rate
from src.domain.rate.dto.base import RateOutSchema


class RateRepository(BaseRepository):

    model = Rate
    schema = RateOutSchema
