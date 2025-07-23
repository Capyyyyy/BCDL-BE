from fastapi import APIRouter, Depends
from db import get_connection

router = APIRouter()


@router.get("/")
async def get_levels(conn=Depends(get_connection)):
    data = await conn.fetch("SELECT * FROM levels ORDER BY rank ASC")

    clean_data = [dict(row) for row in data]

    return clean_data
