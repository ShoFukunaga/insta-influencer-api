import os
import tempfile
from collections.abc import AsyncGenerator, Generator

import pytest
from app.database import get_session
from app.main import app
from app.repositories import BaseORM
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, SessionTransaction


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def temp_csv_file_1():
    data = """influencer_id,post_id,shortcode,likes,comments,thumbnail,text,post_date
1,1,shortcode1,100,10,thumbnail1,こんにちは,2023-01-01 12:00:00
2,2,shortcode2,200,20,thumbnail2,今日の天気,2023-02-02 13:00:00"""
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="cp932", newline=""
    )
    temp_file.write(data)
    temp_file.close()
    yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture
def temp_csv_file_2():
    data = """influencer_id,post_id,shortcode,likes,comments,thumbnail,text,post_date
1,1,shortcode1,100,10,thumbnail1,こんにちは,2023-01-01 12:00:00
2,2,shortcode2_update,200,20,thumbnail2,今日の天気,2023-02-02 13:00:00
2,3,shortcode3,300,30,thumbnail3,今日の天気,2023-02-02 13:00:00"""
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="cp932", newline=""
    )
    temp_file.write(data)
    temp_file.close()
    yield temp_file.name
    os.remove(temp_file.name)


@pytest.fixture(scope="function")
async def ac():
    headers = {"API-KEY": "API-KEY"}
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers=headers,
    ) as c:
        yield c


@pytest.fixture
async def session() -> AsyncGenerator:
    DATABASE_URL = os.environ.get("DATABASE_TEST_URL")
    async_engine = create_async_engine(DATABASE_URL)
    async with async_engine.connect() as conn:
        await conn.run_sync(
            lambda sync_conn: BaseORM.metadata.create_all(sync_conn.engine)
        )

        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()
