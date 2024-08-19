from dataclasses import dataclass
from fastapi import HTTPException
from typing import Optional
import json
import asyncpg
import re


@dataclass
class Database:
    """
    Database object used for connectiong to postgres.
    Configures connection pulling to reduce managment cost of connections
    """

    user: str
    password: str
    host: str
    database: str
    port: str
    _con = None
    _connection_pool = None
    _cusor = None

    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=10,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )

            except Exception as e:
                print(e)

    async def fetch_rows(self, query: str):
        if not self._connection_pool:
            await self.connect()
        else:
            self.con = await self._connection_pool.acquire()
            await self.con.set_type_codec(
                "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
            )
            try:
                result = await self.con.fetch(query)
                return result
            except Exception as e:
                print(e)
            finally:
                await self._connection_pool.release(self.con)


def sql_search(query: str):
    """
    Returns query input for searching table
    used in to_tsquwery form to_tsvector
    """
    user_query = re.sub("[^A-Za-z0-9 ]+", "", query)
    user_query = user_query.split(" ")
    fmt_query = " & ".join(f"{item}" for item in user_query)
    return fmt_query


async def query_handler(
    db: Database,
    query: str,
    code: int,
    message: str = "Resource does not exist",
    skip_error: Optional[bool] = False,
):
    rsp = await db.fetch_rows(query)
    if not rsp and not skip_error:
        raise HTTPException(status_code=code, detail=message)
    return rsp
