import asyncio
from sqlmodel import select
from db.db import async_session, init_db
from db.models import User


async def test_db_connection():
    try:
        # Gọi khởi tạo DB (tạo bảng nếu chưa có)
        await init_db()
        print("✅ Đã kết nối database và khởi tạo bảng thành công.")

        # Kiểm tra truy vấn SELECT
        async with async_session() as session:
            result = await session.exec(select(User))
            users = result.all()
            print(f"📦 Số lượng user hiện có: {len(users)}")

    except Exception as e:
        print("❌ Lỗi kết nối hoặc truy vấn database:")
        print(e)


if __name__ == "__main__":
    asyncio.run(test_db_connection())
