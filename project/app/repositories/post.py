from datetime import datetime

from app.models import Post
from sqlalchemy import (BigInteger, CheckConstraint, Column, Integer, String,
                        select)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseORM(DeclarativeBase):
    pass


class PostORM(BaseORM):
    __tablename__ = "posts"
    post_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    influencer_id: Mapped[int] = mapped_column(Integer)
    shortcode: Mapped[str] = mapped_column(String(100))
    likes: Mapped[int] = mapped_column(Integer)
    comments: Mapped[int] = mapped_column(Integer)
    thumbnail: Mapped[str]
    text: Mapped[str]
    post_date: Mapped[datetime]

    def to_entity(self) -> Post:
        return Post.model_validate(self)


class PostRepository:
    async def add(
        self,
        session: AsyncSession,
        influencer_id: int,
        post_id: int,
        shortcode: str,
        likes: int,
        comments: int,
        thumbnail: str,
        text: str,
        post_date: datetime,
    ) -> Post:
        post = PostORM(
            influencer_id=influencer_id,
            post_id=post_id,
            shortcode=shortcode,
            likes=likes,
            comments=comments,
            thumbnail=thumbnail,
            text=text,
            post_date=post_date,
        )
        session.add(post)
        await session.flush()
        return post.to_entity()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[Post]:
        stmt = select(PostORM)
        return [post.to_entity() for post in await session.scalars(stmt)]

    async def get_by_influencer_id(
        self,
        session: AsyncSession,
        influencer_id: int,
    ) -> list[Post] | None:
        stmt = select(PostORM).where(PostORM.influencer_id == influencer_id)
        posts = await session.scalars(stmt)
        if not posts:
            return None
        return [post.to_entity() for post in posts]
