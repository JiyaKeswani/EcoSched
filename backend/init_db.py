
from app.database import Base, engine
from app.models import Job

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

from sqlalchemy import inspect

print("Available tables:", inspect(engine).get_table_names())
