import asyncpg
from typing import Optional, Sequence

class StarSystemService:
    def __init__(self,pool:asyncpg.Pool):
        self.pool = pool

    async def get_event_participants(self, id_list: Sequence[int]):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT id, student_name, affiliation FROM users \
                                        WHERE id = ANY($1::int[]) \
                                        ORDER BY student_name DESC",id_list)
        
    async def get_events(self, event_id: Optional[int] = None):
        base = "SELECT id, post_title, author_id, participants FROM events"
        args = []
        if event_id:
            base += " WHERE " + "id = $1"
            args.append(event_id)

        base += f" ORDER BY id DESC"

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(base, *args) 

        return [dict(r) for r in rows]
        
    async def count_events(self) -> int:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT COUNT(*) FROM events")

        return row["count"]
    
    async def get_names(self, house: list[str] | None, page: int, page_size: int,order:str = "ss_ranking"):
        base = "SELECT student_name, affiliation, ss_ranking, id FROM users"
        where = []
        args = []
        idx = 1

        if house:
            where.append(f"affiliation = ANY(${idx}::text[])")
            args.append(house)
            idx += 1

        if where:
            base += " WHERE " + " AND ".join(where)

        base += f" ORDER BY {order} DESC LIMIT {page_size} OFFSET {(page) * page_size}"

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
    
    async def get_student_rank(self, student: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT ss_ranking, affiliation FROM users \
                                    WHERE student_name = $1;",student)
        
    async def set_student_rank(self, student: str, quantity: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch("UPDATE users \
                                    SET ss_ranking = $1 \
                                    WHERE student_name = $2 \
                                    RETURNING student_name, ss_ranking;",quantity,student)