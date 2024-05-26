from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseModel(_BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Post(BaseModel):
    post_id: int
    influencer_id: int
    shortcode: str
    likes: int
    comments: int
    thumbnail: str
    text: str
    post_date: datetime


class InfluencerAverage(BaseModel):
    influencer_id: int
    average_likes: float
    average_comments: float


class AverageLikesInfluencer(BaseModel):
    influencer_id: int
    average_likes: float


class AverageCommentsInfluencer(BaseModel):
    influencer_id: int
    average_comments: float


class NounCounts(BaseModel):
    noun: str
    count: int


class GetInfluencerNumOfUseNoun(BaseModel):
    influencer_id: int
    nouns: list[NounCounts]
