from datetime import datetime, timezone
from unittest.mock import ANY

import pytest
from app.repositories.post import PostORM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def setup_data(session: AsyncSession):

    post1 = PostORM(
        post_id=1,
        influencer_id=101,
        shortcode="abc123",
        likes=150,
        comments=100,
        thumbnail="http://example.com/image1.jpg",
        text="foo",
        post_date=datetime(2023, 5, 1, 12, 0),
    )
    post2 = PostORM(
        post_id=2,
        influencer_id=102,
        shortcode="efg456",
        likes=200,
        comments=20,
        thumbnail="http://example.com/image2.jpg",
        text="彼は新しいパンツを買うためにショッピングモールへ行きました。",
        post_date=datetime(2023, 5, 2, 14, 30),
    )
    post3 = PostORM(
        post_id=3,
        influencer_id=102,
        shortcode="hij789",
        likes=250,
        comments=40,
        thumbnail="http://example.com/image2.jpg",
        text="彼は新しいパンツを買うためにショッピングモールへ行きました。子供たちは積み木で大きな塔を作りました。",
        post_date=datetime(2023, 5, 2, 14, 30),
    )
    post4 = PostORM(
        post_id=4,
        influencer_id=103,
        shortcode="hij789",
        likes=500,
        comments=10,
        thumbnail="http://example.com/image2.jpg",
        text=(
            "「ではみなさんは、そういうふうに川だと言われたり、乳の流れたあとだと言われたりしていた、"
            "このぼんやりと白いものがほんとうは何かご承知ですか」先生は、黒板につるした大きな黒い星座の図の、"
            "上から下へ白くけぶった銀河帯のようなところを指しながら、みんなに問いをかけました。"
            "カムパネルラが手をあげました。"
            "それから四、五人手をあげました。"
            "ジョバンニも手をあげようとして、急いでそのままやめました。"
            "たしかにあれがみんな星だと、いつか雑誌で読んだのでしたが、このごろはジョバンニはまるで毎日教室でもねむく、本を読むひまも読む本"
        ),
        post_date=datetime(2023, 5, 2, 14, 30),
    )
    post5 = PostORM(
        post_id=5,
        influencer_id=103,
        shortcode="hij789",
        likes=500,
        comments=10,
        thumbnail="http://example.com/image2.jpg",
        text=(
            "「ではみなさんは、そういうふうに川だと言われたり、乳の流れたあとだと言われたりしていた、"
            "このぼんやりと白いものがほんとうは何かご承知ですか」先生は、黒板につるした大きな黒い星座の図の、"
            "上から下へ白くけぶった銀河帯のようなところを指しながら、みんなに問いをかけました。"
            "カムパネルラが手をあげました。"
            "それから四、五人手をあげました。"
            "ジョバンニも手をあげようとして、急いでそのままやめました。"
            "たしかにあれが"
        ),
        post_date=datetime(2023, 5, 2, 14, 30),
    )
    session.add_all([post1, post2, post3, post4, post5])
    await session.flush()
    await session.commit()


@pytest.mark.anyio
async def test_get_influencer_average_normal(ac, session: AsyncSession):
    """
    平均いいね数、平均コメント数をJSON形式で返すAPI
    正常系_1
    """
    await setup_data(session)
    post = await session.scalar(select(PostORM).where(PostORM.post_id == 1))
    response = await ac.get(f"/api/v1/posts/influencer/{post.influencer_id}/average")
    assert response.status_code == 200
    data = response.json()
    assert data["influencer_id"] == 101
    assert data["average_likes"] == 150
    assert data["average_comments"] == 100


@pytest.mark.anyio
async def test_get_influencer_average_normal_2(ac, session: AsyncSession):
    """
    平均いいね数、平均コメント数をJSON形式で返すAPI
    正常系_2
    """
    await setup_data(session)
    post = await session.scalar(select(PostORM).where(PostORM.post_id == 2))
    response = await ac.get(f"/api/v1/posts/influencer/{post.influencer_id}/average")
    assert response.status_code == 200
    data = response.json()
    assert data["influencer_id"] == 102
    assert data["average_likes"] == 225
    assert data["average_comments"] == 30


@pytest.mark.anyio
async def test_get_influencer_average_not_found(ac, session: AsyncSession):
    """
    平均いいね数、平均コメント数をJSON形式で返すAPI
    異常系_1
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/999/average")
    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Not Found"
    assert data["details"] == {"influencer_id": 999}


@pytest.mark.anyio
async def test_get_influencer_most_likes_normal_1(ac, session: AsyncSession):
    """
    平均いいね数が多いinfluencer上位N件をJSON形式で返すAPI
    正常系_1
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/most-likes/?limit=3")
    assert response.status_code == 200
    expected = {
        "influencers": [
            {"influencer_id": 103, "average_likes": 500},
            {"influencer_id": 102, "average_likes": 225},
            {"influencer_id": 101, "average_likes": 150},
        ]
    }
    data = response.json()
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_likes_normal_2(ac, session: AsyncSession):
    """
    平均いいね数が多いinfluencer上位N件をJSON形式で返すAPI
    正常系_2
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/most-likes/?limit=1000")
    assert response.status_code == 200
    expected = {
        "influencers": [
            {"influencer_id": 103, "average_likes": 500},
            {"influencer_id": 102, "average_likes": 225},
            {"influencer_id": 101, "average_likes": 150},
        ]
    }
    data = response.json()
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_likes_normal_3(ac, session: AsyncSession):
    """
    平均いいね数が多いinfluencer上位N件をJSON形式で返すAPI
    正常系_3
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/most-likes/?limit=0")
    assert response.status_code == 200
    expected = {"influencers": []}
    data = response.json()
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_comments_normal_1(ac, session: AsyncSession):
    """
    平均コメント数が多いinfluencer上位N件をJSON形式で返すAPI
    正常系_1
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/most-comments/?limit=3")
    assert response.status_code == 200
    expected = {
        "influencers": [
            {"influencer_id": 101, "average_comments": 100},
            {"influencer_id": 102, "average_comments": 30},
            {"influencer_id": 103, "average_comments": 10},
        ]
    }
    data = response.json()
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_comments_normal_2(ac, session: AsyncSession):
    """
    平均コメント数が多いinfluencer上位N件をJSON形式で返すAPI
    正常系_2
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/most-comments/?limit=1000")
    assert response.status_code == 200
    expected = {
        "influencers": [
            {"influencer_id": 101, "average_comments": 100},
            {"influencer_id": 102, "average_comments": 30},
            {"influencer_id": 103, "average_comments": 10},
        ]
    }
    data = response.json()
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_comments_normal_3(ac, session: AsyncSession):
    """
    平均コメント数が多いinfluencer上位N件をJSON形式で返すAPI
    正常系_3
    """
    await setup_data(session)
    response = await ac.get("/api/v1/posts/influencer/most-comments/?limit=0")
    assert response.status_code == 200
    expected = {"influencers": []}
    data = response.json()
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_nouns_normal_1(ac, session: AsyncSession):
    """
    influencer_id毎に、格納したデータのtextカラムに格納されたデータから名詞を抽出し、
    その使用回数を集計し、上位N件（NはAPIのリクエストデータ）をJSON形式で返すAPI
    正常系_1
    """
    await setup_data(session)
    post = await session.scalar(select(PostORM).where(PostORM.post_id == 2))
    response = await ac.get(
        f"/api/v1/posts/influencer/{post.influencer_id}/most-nouns/?limit=5"
    )
    expected = {
        "influencer_id": 102,
        "nouns": [
            {"count": 2, "noun": "パンツ"},
            {"count": 2, "noun": "ショッピングモール"},
            {"count": 1, "noun": "子供たち"},
            {"count": 1, "noun": "積み木"},
            {"count": 1, "noun": "塔"},
        ],
    }
    data = response.json()
    assert response.status_code == 200
    assert data == expected


@pytest.mark.anyio
async def test_get_influencer_most_nouns_normal_2(ac, session: AsyncSession):
    """
    influencer_id毎に、格納したデータのtextカラムに格納されたデータから名詞を抽出し、
    その使用回数を集計し、上位N件（NはAPIのリクエストデータ）をJSON形式で返すAPI
    正常系_2
    """
    await setup_data(session)
    post = await session.scalar(select(PostORM).where(PostORM.post_id == 4))
    response = await ac.get(
        f"/api/v1/posts/influencer/{post.influencer_id}/most-nouns/?limit=5"
    )
    expected = {
        "influencer_id": 103,
        "nouns": [
            {"count": 2, "noun": "川"},
            {"count": 2, "noun": "乳"},
            {"count": 2, "noun": "ほんとう"},
            {"count": 2, "noun": "ご承知"},
            {"count": 2, "noun": "先生"},
        ],
    }
    data = response.json()
    assert response.status_code == 200
    assert data == expected
