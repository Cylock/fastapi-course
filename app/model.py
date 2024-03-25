
# Python std libs
from typing import Optional
from datetime import datetime

# SQLModel and SQLAlchemy libs

from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func

class Posts(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    # default is client-side, and server_default is server side. Default is used when executing an INSERT command (python generates the *default* value and then orm inserts into the db)
    # server_default is used when executing CREATE TABLE command (letting the db server handle the default value generation).  https://docs.sqlalchemy.org/en/20/core/defaults.html#sqlalchemy.schema.ColumnDefault
    published: bool = Field(default=True, nullable=False)
    created_at: datetime | None = Field(
        default=None,
        sa_type= DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    modified_at: datetime | None = Field(
        default=None,
        sa_type= DateTime(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
    )



# sa_column <--- sqlalchemy_column


# If I want to add pydantic strict type checking on
# a field and combine it with a default 
# https://docs.pydantic.dev/2.2/usage/strict_mode/#strict-mode-with-field
# rating: Optional[int] = Field(default=None,strict=True)

