from datetime import datetime

from app.exceptions import AppException
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

    def update(self, post: Post) -> None:
        self.influencer_id = post.influencer_id
        self.post_id = post.post_id
        self.shortcode = post.shortcode
        self.likes = post.likes
        self.comments = post.comments
        self.thumbnail = post.thumbnail
        self.text = post.text
        self.post_date = post.post_date


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

    async def update(self, session: AsyncSession, post: Post) -> Post:
        stmt = select(PostORM).where(PostORM.post_id == post.post_id)
        post_ = await session.scalar(stmt)
        if not post_:
            raise AppException()
        post_.update(post)
        await session.flush()
        return post_.to_entity()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[Post]:
        stmt = select(PostORM)
        return [post.to_entity() for post in await session.scalars(stmt)]

    async def get_by_id(
        self,
        session: AsyncSession,
        post_id: int,
    ) -> Post | None:
        stmt = select(PostORM).where(PostORM.post_id == post_id)
        post = await session.scalar(stmt)
        if not post:
            return None
        return post.to_entity()

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
