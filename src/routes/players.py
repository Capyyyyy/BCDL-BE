from fastapi import APIRouter, Depends
from db import get_connection

router = APIRouter()

@router.get("/players")
async def get_levels(conn = Depends(get_connection)):

        data = await conn.fetch('SELECT * FROM players ORDER BY score ASC')

        clean_data = [dict(row) for row in data]

        return(clean_data)
