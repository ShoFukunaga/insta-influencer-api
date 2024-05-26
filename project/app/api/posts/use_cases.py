from collections import Counter, defaultdict

import spacy
from app.database import AsyncSession, PostRepository
from app.exceptions import NotFound
from app.models import (InfluencerAverage, InfluencerMostComments,
                        InfluencerMostLikes, InfluencerMostNouns, NounCounts)

nlp = spacy.load("ja_ginza")


class GetInfluencerAverage:
    def __init__(
        self,
        session: AsyncSession,
        repo: PostRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        influencer_id: int,
    ) -> InfluencerAverage:
        async with self.session() as session:
            posts = await self.repo.get_by_influencer_id(
                session,
                influencer_id,
            )
            if not posts:
                raise NotFound("influencer_id", influencer_id)
        return InfluencerAverage(
            influencer_id=influencer_id,
            average_likes=sum([post.likes for post in posts]) / len(posts),
            average_comments=sum([post.comments for post in posts]) / len(posts),
        )


class GetInfluencerMostLikes:
    def __init__(
        self,
        session: AsyncSession,
        repo: PostRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        limit: int,
    ) -> list[InfluencerMostLikes]:
        async with self.session() as session:
            posts = await self.repo.get_all(session)
            # influencer_idごとの投稿数、いいね数を集計します
            influencer_counts = defaultdict(int)
            influencer_likes = defaultdict(int)
            for post in posts:
                influencer_counts[post.influencer_id] += 1
                influencer_likes[post.influencer_id] += post.likes
            average_likes_list = []
            for influencer_id, counts in influencer_counts.items():
                average_likes_list.append(
                    InfluencerMostLikes(
                        influencer_id=influencer_id,
                        average_likes=round(
                            influencer_likes[influencer_id] / counts, 2
                        ),
                    )
                )
            return sorted(
                average_likes_list,
                key=lambda x: x.average_likes,
                reverse=True,
            )[:limit]


class GetInfluencerMostComments:
    def __init__(
        self,
        session: AsyncSession,
        repo: PostRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        limit: int,
    ) -> list[InfluencerMostComments]:
        async with self.session() as session:
            posts = await self.repo.get_all(session)
            # influencer_idごとの投稿数、コメント数を集計します
            influencer_counts = defaultdict(int)
            influencer_comments = defaultdict(int)
            for post in posts:
                influencer_counts[post.influencer_id] += 1
                influencer_comments[post.influencer_id] += post.comments
            average_comments_list = []
            for influencer_id, counts in influencer_counts.items():
                average_comments_list.append(
                    InfluencerMostComments(
                        influencer_id=influencer_id,
                        average_comments=round(
                            influencer_comments[influencer_id] / counts, 2
                        ),
                    )
                )
            return sorted(
                average_comments_list,
                key=lambda x: x.average_comments,
                reverse=True,
            )[:limit]


class GetInfluencerMostNouns:
    def __init__(
        self,
        session: AsyncSession,
        repo: PostRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        influencer_id: int,
        limit: int,
    ) -> InfluencerMostNouns:
        async with self.session() as session:
            posts = await self.repo.get_by_influencer_id(
                session,
                influencer_id,
            )
            if not posts:
                raise NotFound("influencer_id", influencer_id)
            nouns = []

            for post in posts:
                # 改行コードを取り除きます
                text = post.text.replace("\r", "").replace("\n", "").replace("\r\n", "")
                doc = nlp(text)
                for token in doc:
                    if token.pos_ == "NOUN" and token.tag_ in {
                        "名詞-普通名詞-一般",
                        "名詞-固有名詞-一般",
                    }:
                        nouns.append(token.text)
            counter = Counter(nouns)
            most_common = counter.most_common(limit)

        return InfluencerMostNouns(
            influencer_id=influencer_id,
            nouns=[
                NounCounts(
                    noun=noun,
                    count=count,
                )
                for noun, count in most_common
            ],
        )
