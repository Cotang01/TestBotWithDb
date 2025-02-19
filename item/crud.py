from typing import List

from sqlalchemy import insert, select, Sequence, Row
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import db_session
from item.models import Item


@db_session
async def create_item(session: AsyncSession, data: str) -> None:
    await session.execute(insert(Item).values(data=data))


@db_session
async def get_items(session: AsyncSession) -> List[Item]:
    res = await session.execute(select(Item))
    return [r[0] for r in res.fetchall()]

