import asyncpg
from typing import Optional, Sequence

class ForumHandler:
    def __init__(self,pool:asyncpg.Pool):
        self.pool = pool

    async def get_names(self, house: list[str] | None, page: int, page_size: int):
        base = "SELECT student_name, affiliation FROM users"
        where = []
        args = []
        idx = 1

        if house:
            where.append(f"affiliation = ANY(${idx}::text[])")
            args.append(house)
            idx += 1

        if where:
            base += " WHERE " + " AND ".join(where)

        base += f" ORDER BY student_name DESC LIMIT {page_size} OFFSET {(page) * page_size}"

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(base, *args)
            

        return [dict(r) for r in rows]

    async def count_names(self, house: Optional[Sequence[str]]) -> int:
        base = "SELECT COUNT(*) FROM users"
        where = []
        args = []
        idx = 1

        if house:
            where.append(f"affiliation = ANY(${idx}::text[])")
            args.append(list(house))
            idx += 1

        if where:
            base += " WHERE " + " AND ".join(where)

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(base, *args)

        return row["count"]