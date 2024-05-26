from app.models import BaseModel


class InfluencerAverageLikes(BaseModel):
    influencer_id: int
    average_likes: float


class InfluencerAverageComments(BaseModel):
    influencer_id: int
    average_comments: float


class GetInfluencerAverageResponse(BaseModel):
    influencer_id: int
    average_likes: float
    average_comments: float


class GetInfluencerMostLikesResponse(BaseModel):
    influencers: list[InfluencerAverageLikes]


class GetInfluencerMostCommentsResponse(BaseModel):
    influencers: list[InfluencerAverageComments]


class NounCounts(BaseModel):
    noun: str
    count: int


class GetInfluencerMostNounsResponse(BaseModel):
    influencer_id: int
    nouns: list[NounCounts]
