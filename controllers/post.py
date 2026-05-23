
from fastapi import APIRouter, status
from services.posts import PostService
from views.post import PostOut
from schemas.post import PostIn, PostUpdateIn

router = APIRouter(prefix="/posts")

post_service = PostService()

@router.get("", response_model=list[PostOut], description="Get all posts")
async def read_posts(published: bool = True, limit: int = 10, skip: int = 0):
    return await post_service.get_all(published=published, limit=limit, skip=skip)

@router.get("/{id}", response_model=PostOut, description="Get post by id")
async def read_post(id: int):
    return await post_service.get_by_id(id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostOut, description="Create a new post")
async def create_post(post: PostIn):
    return await post_service.create(post)

@router.patch("/{id}", response_model=PostOut, description="Update a post")
async def update_post(id: int, post: PostUpdateIn):
    return await post_service.update(id=id, post=post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a post", response_model=None)
async def delete_post(id: int):
    return await post_service.delete(id=id) 