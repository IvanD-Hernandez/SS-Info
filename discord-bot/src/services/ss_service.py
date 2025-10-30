import asyncpg

class StarSystem:
    def __init__(self,pool:asyncpg.Pool):
        self.pool = pool


    async def top_rankers(self, house: str, limit: int = 10):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT student_name, ss_ranking FROM users \
                                    WHERE affiliation = $1 ORDER BY ss_ranking DESC LIMIT $2;",house,limit)
