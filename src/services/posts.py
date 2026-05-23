from databases.interfaces import Record
from fastapi import HTTPException, status

from src.models.post import posts
from src.schemas.post import PostIn, PostUpdateIn
from src.database import database

class PostService:
    async def get_all(self, published: bool = True, limit: int = 10, skip: int = 0) -> list[Record]:
        query = posts.select().where(posts.c.published == published).limit(limit).offset(skip)
        return await database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Record | None:
        return await self.__get_by_id(id)

    async def create(self, post: PostIn) -> dict:
        query = posts.insert().values(
            title=post.title, 
            content=post.content, 
            published=post.published,
            published_at=post.published_at
        )
        last_record_id = await database.execute(query)
        return {**post.model_dump(), "id": last_record_id}

    async def update(self, id: int, post: PostUpdateIn) -> Record:
        total = self.count(id=id)
        if not total:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        data = post.model_dump(exclude_unset=True)
        query = posts.update().where(posts.c.id == id).values(**data)
        await database.execute(query)

        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        query = posts.delete().where(posts.c.id == id)
        await database.execute(query)
    
    async def __get_by_id(self, id: int) -> Record:
        query = posts.select().where(posts.c.id == id)
        post = await database.fetch_one(query=query)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
    
    async def count(self, id: int) -> int:
        query = "SELECT COUNT(id) as total FROM posts WHERE id = :id"
        result = await database.fetch_one(query, {"id": id})
        return result.total