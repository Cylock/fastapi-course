from typing import Optional
from sqlmodel import Field, SQLModel


class Posts(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = True
