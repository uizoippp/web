import base64
from db.config import settings

# Hàm tạo token từ user_id (giả định đơn giản, bạn có thể dùng JWT)
def generate_token(user_id: str) -> str:
    # Mã hóa base64 từ user_id + bí mật đơn giản
    secret = settings.SECRET_KEY
    if not secret:
        raise ValueError("Secret key is not set in the environment variables.")
    raw = f"{user_id}:{secret}"
    return base64.urlsafe_b64encode(raw.encode()).decode()

