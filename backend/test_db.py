
from app.database import engine

try:
    with engine.connect() as connection:
        print("Successfully connected to EcoSched PostgreSQL!")

except Exception as error:
    print("Database connection failed:")
    print(error)
