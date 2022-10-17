from __future__ import annotations

from .base import Database

class LevesDatabase(Database):
    def __init__(self) -> None:
        super().__init__("./data/levels.db")
        
    async def on_ready(self) -> None:
        await self.create_table(
            "levels", 
            table_attrs=(
                "member_id INTEGER(19) UNIQUE NOT NULL",
                "xp_relative INTEGER(20)",
                "total_xp INTEGER(20)",
                "level INTEGER(5)"
                )
            )

    async def increment_xp(self, member_id: int, amount: int) -> tuple[int] | tuple[bool]:
        """Retorna o level e o xp total do user se ele upar"""
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE member_id=?",
                (member_id)
            )

            row = await cursor.fetchone()
            
            # User não está na database
            if not row: 
                await cursor.execute(
                    f"INSERT INTO {self.table_name} VALUES(?, ?, ?, ?)",
                    (member_id, amount, amount, 0)
                )
                return (False, False)

            relative_xp_on_db = row[1]
            lvl_on_db = row[3]
            relative_updated_xp = relative_xp_on_db + amount
            total_updated_xp = row[2] + amount

            await cursor.execute(
                f"UPDATE {self.table_name} SET xp_relative=?, total_xp=? WHERE member_id=?",
                (relative_updated_xp, total_updated_xp, member_id)
            )

            excedent = 5 * (lvl_on_db ^ 2) + (50 * lvl_on_db) + 100 - relative_updated_xp

            if excedent <= 0:
                await cursor.execute(
                    f"UPDATE {self.table_name} SET xp_relative=?, level=? WHERE member_id=?",
                    (excedent * -1, lvl_on_db + 1, member_id)
                )
                return (total_updated_xp, lvl_on_db + 1)
            return (False, False)

    async def get_rank(self, member_id: int) -> tuple[int]:
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE member_id=?",
                (member_id)
            )
            row = await cursor.fetchone()
            return (row[2], row[3])

    async def get_leaderboard_ids(self) -> set[int]:
        leaderboard: set[int] = set()
        async with self.conn.cursor() as cursor:
            await cursor.execute(
                f"SELECT member_id FROM {self.table_name} ORDER BY level DESC LIMIT 10"
            )
            rows = await cursor.fetchall()
            for row in rows:
                leaderboard.add(row[0])

        return leaderboard