from typing import Annotated

from app.routes import LoggingRoute
from fastapi import APIRouter, Depends

from .schemas import (GetInfluencerAverageResponse,
                      GetInfluencerNumOfUseNounResponse,
                      GetTopCommentedInfluencersResponse,
                      GetTopLikedInfluencersResponse)
from .use_cases import (GetInfluencerAverage, GetInfluencerNoun,
                        GetTopCommentedInfluencers, GetTopLikedInfluencers)

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
    "/influencer/top/likes/",
    response_model=GetTopLikedInfluencersResponse,
)
async def get_top_liked_influencers(
    use_case: Annotated[GetTopLikedInfluencers, Depends(GetTopLikedInfluencers)],
    limit: int = 10,
) -> GetTopLikedInfluencersResponse:
    return GetTopLikedInfluencersResponse(
        influencers=await use_case.execute(limit),
    )


@router.get(
    "/influencer/top/comments/",
    response_model=GetTopCommentedInfluencersResponse,
)
async def get_influencer_top_comments(
    use_case: Annotated[
        GetTopCommentedInfluencers, Depends(GetTopCommentedInfluencers)
    ],
    limit: int = 10,
) -> GetTopCommentedInfluencersResponse:
    return GetTopCommentedInfluencersResponse(
        influencers=await use_case.execute(limit),
    )


@router.get(
    "/influencer/{influencer_id}/noun/",
    response_model=GetInfluencerNumOfUseNounResponse,
)
async def get_influencer_noun_uses(
    use_case: Annotated[GetInfluencerNoun, Depends(GetInfluencerNoun)],
    influencer_id: int,
    limit: int = 10,
) -> GetInfluencerNumOfUseNounResponse:
    result = await use_case.execute(influencer_id, limit)
    return GetInfluencerNumOfUseNounResponse.model_validate(result)
