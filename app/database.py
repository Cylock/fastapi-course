from sqlmodel import SQLModel, Session, create_engine

database_url = "postgresql://postgres:postgres-admin@db:5432/fastapi"
# connection_args = {"check_same_thread": False} <-- Arg used by SQLite, not Postgress

engine = create_engine(database_url, echo=True)  # connect_args=connection_args)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
