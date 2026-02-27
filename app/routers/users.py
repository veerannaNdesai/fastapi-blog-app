from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User
from app.schemas import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):

    new_user = User(**user.model_dump())
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User))
    users = result.scalars().all()

    return users