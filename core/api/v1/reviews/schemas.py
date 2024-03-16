from datetime import datetime

from ninja import Schema

from core.apps.products.entities.reviews import Review


class ReviewInSchema(Schema):
    rating: int
    text: str

    def to_entity(self) -> Review:
        return Review(
            rating=self.rating,
            text=self.text,
        )


class ReviewOutSchema(ReviewInSchema):
    id: int  # noqa
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, review: Review) -> 'ReviewOutSchema':
        return ReviewOutSchema(
            id=review.id,
            rating=review.rating,
            text=review.text,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
