from datetime import datetime
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types.user import User
from database.models import ShortProjects, Users


async def orm_add_poject(session: AsyncSession, data: dict):
    obj = ShortProjects(
        name=data['name'],
        cost=int(data['cost']),
        profit=int(data['profit']),
        guarantee=data['guarantee'],
        result_date=data['result_date'],
        deadline_date=data['deadline_date'],
        place=int(data['place']),
        status='available'
    )
    session.add(obj)
    await session.commit()

async def orm_get_projects(session: AsyncSession):
    query = select(ShortProjects)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_projects_available(session: AsyncSession):
    query = select(ShortProjects).where(ShortProjects.status == 'available')
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_project(session: AsyncSession, project_id: int):
    query = select(ShortProjects).where(ShortProjects.id == project_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_poject(session: AsyncSession, project_id: int, data: dict):
    query = update(ShortProjects).where(ShortProjects.id == project_id).values(
        name=data['name'],
        cost=int(data['cost']),
        profit=int(data['profit']),
        guarantee=data['guarantee'],
        result_date=data['result_date'],
        deadline_date=data['deadline_date'],
        place=int(data['place']),
    )
    await session.execute(query)
    await session.commit()

async def orm_delete_project(session: AsyncSession, project_id: int):
    query = delete(ShortProjects).where(ShortProjects.id == project_id)
    await session.execute(query)
    await session.commit()


async def orm_add_user(session: AsyncSession, user: User):
    obj = Users(
        tg_id=user.id,
        name=user.full_name,
        username=user.username,
    )
    session.add(obj)
    await session.commit()