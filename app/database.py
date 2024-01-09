from sqlmodel import create_engine

database_url = "postgresql://postgres:postgres-admin@db:5432/fastapi"
engine = create_engine(database_url, echo=True)
