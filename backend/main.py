from fastapi import FastAPI
import uvicorn
from crud.user.user import router as user_router

app = FastAPI()
app.include_router(user_router, prefix="/auth", tags=["user"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)