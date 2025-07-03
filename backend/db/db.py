from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.config import settings

# Tạo engine bất đồng bộ
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Tạo session
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
async def get_session():
    async with async_session() as session:
        yield session

# Hàm khởi tạo DB
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)