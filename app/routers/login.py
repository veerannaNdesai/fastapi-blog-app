from app.auth import verify_password, create_access_token
from fastapi.exceptions import HTTPException
from app.schemas import LoginRequest,TokenResponse
from app.models import User
from sqlalchemy import select
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,APIRouter

router = APIRouter() 

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginRequest, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"user_id": db_user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }