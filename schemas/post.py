from pydantic import AwareDatetime, BaseModel


class PostIn(BaseModel):
    title: str
    content: str
    published_at: AwareDatetime | None = None
    published: bool = False