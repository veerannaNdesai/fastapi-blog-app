from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from fastapi import UploadFile, File
from app.oauth2 import get_current_user
import os
import uuid
import shutil

from app.database import get_db
from app.models import Post,User
from app.schemas import PostCreate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(User.id == post.user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {post.user_id} does not exist"
        )
    new_post = Post(**post.model_dump())

    db.add(new_post)

    await db.commit()
    await db.refresh(new_post)

    return new_post

@router.post("/{post_id}/upload-image")
async def upload_post_image(
    post_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    # 1️⃣ Check if post exists
    result = await db.execute(
        select(Post).where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # 2️⃣ Validate file type
    allowed_extensions = ["jpg", "jpeg", "png"]
    ext = file.filename.split(".")[-1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )

    # 3️⃣ Generate unique filename
    unique_filename = f"{uuid.uuid4()}.{ext}"
    upload_dir = "uploads/"
    file_path = os.path.join(upload_dir, unique_filename)

    # 4️⃣ Save file (UploadFile is already async-friendly)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 5️⃣ Save path in database
    post.image_url = f"/uploads/{unique_filename}"
    await db.commit()
    await db.refresh(post)

    return {"image_url": post.image_url}

@router.get("/")
async def get_posts(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Post))
    posts = result.scalars().all()

    return posts