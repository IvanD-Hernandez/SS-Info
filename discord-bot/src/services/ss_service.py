import asyncpg

class StarSystem:
    def __init__(self,pool:asyncpg.Pool):
        self.pool = pool


    async def top_rankers(self, house: str, limit: int = 10):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT student_name, ss_ranking FROM users \
                                    WHERE affiliation = $1 ORDER BY ss_ranking DESC LIMIT $2;",house,limit)

    async def get_student_rank(self, house: str, student: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT ss_ranking FROM users \
                                    WHERE affiliation = $1 AND student_name = $2;",house,student)
        
    async def set_student_rank(self, house: str, student: str, quantity: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch("UPDATE users \
                                    SET ss_ranking = $1 \
                                    WHERE affiliation = $2 AND student_name = $3 \
                                    RETURNING student_name, ss_ranking;",quantity,house,student)
