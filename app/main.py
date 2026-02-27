from fastapi import FastAPI
from app.routers import posts,users,register,login
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(register.router)
app.include_router(login.router)

# config of uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")