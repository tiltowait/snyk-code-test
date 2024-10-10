"""Model for BlogPost."""

from typing import Optional

from pydantic import BaseModel


class BlogPost(BaseModel):
    """Represents a blog post."""

    id: Optional[int] = None
    title: str
    content: str
