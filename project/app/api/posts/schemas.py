from app.models import BaseModel


class AverageLikesInfluencer(BaseModel):
    influencer_id: int
    average_likes: float


class AverageCommentsInfluencer(BaseModel):
    influencer_id: int
    average_comments: float


class GetInfluencerAverageResponse(BaseModel):
    influencer_id: int
    average_likes: float
    average_comments: float


class GetTopLikedInfluencersResponse(BaseModel):
    influencers: list[AverageLikesInfluencer]


class GetTopCommentedInfluencersResponse(BaseModel):
    influencers: list[AverageCommentsInfluencer]


class NounCounts(BaseModel):
    noun: str
    count: int


class GetInfluencerNumOfUseNounResponse(BaseModel):
    influencer_id: int
    nouns: list[NounCounts]
