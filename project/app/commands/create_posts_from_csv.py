import csv
import logging
from datetime import datetime

import fire
from app.database import AsyncSessionLocal
from app.repositories.post import PostRepository

logger = logging.getLogger(__name__)


async def create_post_from_csv(file_path: str, session):
    repo = PostRepository()
    # csvファイルの読み取り
    with open(file_path, newline="", encoding="cp932") as f:
        next(csv.reader(f))
        reader = csv.reader(f)
        for row in reader:

            post = await repo.get_by_id(session, int(row[1]))
            if not post:
                await repo.add(
                    session=session,
                    influencer_id=int(row[0]),
                    post_id=int(row[1]),
                    shortcode=row[2],
                    likes=int(row[3]),
                    comments=int(row[4]),
                    thumbnail=row[5],
                    text=row[6],
                    post_date=datetime.strptime(
                        row[7],
                        "%Y-%m-%d %H:%M:%S",
                    ),
                )
            else:
                await repo.update(session, post)


if __name__ == "__main__":

    async def main(file_path: str):
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await create_post_from_csv(file_path, session)

    logger.info("Start creating post data")
    fire.Fire(main)
    logger.info("Created")
