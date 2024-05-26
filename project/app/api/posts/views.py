from typing import Annotated

from app.routes import LoggingRoute
from fastapi import APIRouter, Depends

from .schemas import (GetInfluencerAverageResponse,
                      GetInfluencerMostCommentsResponse,
                      GetInfluencerMostLikesResponse,
                      GetInfluencerMostNounsResponse)
from .use_cases import (GetInfluencerAverage, GetInfluencerMostComments,
                        GetInfluencerMostLikes, GetInfluencerMostNouns)

router = APIRouter(
    prefix="/v1/posts",
    route_class=LoggingRoute,
)


@router.get(
    "/influencer/{influencer_id}/average",
    response_model=GetInfluencerAverageResponse,
)
async def get_influencer_average(
    influencer_id: int,
    use_case: Annotated[GetInfluencerAverage, Depends(GetInfluencerAverage)],
) -> GetInfluencerAverageResponse:
    """Postの平均いいね数および平均コメント数を返すAPIエンドポイント"""
    result = await use_case.execute(
        influencer_id=influencer_id,
    )
    return GetInfluencerAverageResponse.model_validate(result)


@router.get(
    "/influencer/most-likes/",
    response_model=GetInfluencerMostLikesResponse,
)
async def get_influencer_most_likes(
    use_case: Annotated[
        GetInfluencerMostLikes,
        Depends(GetInfluencerMostLikes),
    ],
    limit: int = 10,
) -> GetInfluencerMostLikesResponse:
    return GetInfluencerMostLikesResponse(
        influencers=await use_case.execute(limit),
    )


@router.get(
    "/influencer/most-comments/",
    response_model=GetInfluencerMostCommentsResponse,
)
async def get_influencer_most_comments(
    use_case: Annotated[
        GetInfluencerMostComments,
        Depends(GetInfluencerMostComments),
    ],
    limit: int = 10,
) -> GetInfluencerMostCommentsResponse:
    return GetInfluencerMostCommentsResponse(
        influencers=await use_case.execute(limit),
    )


@router.get(
    "/influencer/{influencer_id}/most-nouns/",
    response_model=GetInfluencerMostNounsResponse,
)
async def get_influencer_most_nouns(
    use_case: Annotated[GetInfluencerMostNouns, Depends(GetInfluencerMostNouns)],
    influencer_id: int,
    limit: int = 10,
) -> GetInfluencerMostNounsResponse:
    result = await use_case.execute(influencer_id, limit)
    return GetInfluencerMostNounsResponse.model_validate(result)
