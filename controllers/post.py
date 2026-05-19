
from fastapi import APIRouter, Response, status
from views.post import PostOut
from schemas.post import PostIn
from models.post import posts
from database import database

router = APIRouter(prefix="/posts")

@router.get("", response_model=list[PostOut], description="Get all posts")
async def read_posts(published: bool = True, limit: int = 10, skip: int = 0):
    query = posts.select()
    return await database.fetch_all(query=query)

@router.get("/{id}", response_model=PostOut, description="Get post by id")
async def read_post(id: int):
    query = posts.select().where(posts.c.id == id)
    post = await database.fetch_one(query=query)

    if not post:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return post

@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostOut, description="Create a new post")
async def create_posts(post: PostIn):
    query = posts.insert().values(title=post.title, content=post.content, published=post.published)
    last_record_id = await database.execute(query)
    return {**post.model_dump(), "id": last_record_id}
    