import subprocess
from config import settings

def generate_models():
    db_url = f'mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
    output_file = "./db/models.py"

    cmd = [
        "sqlacodegen",
        db_url,
        "--outfile", output_file
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ Model generated to {output_file}")

if __name__ == "__main__":
    generate_models()
