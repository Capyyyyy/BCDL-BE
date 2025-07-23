from fastapi import APIRouter, Depends
from db import get_connection

router = APIRouter()


@router.get("/{level_id}/completions")
async def get_level_completions(level_id: int, conn=Depends(get_connection)):
    data = await conn.fetch(
        'SELECT * FROM completions WHERE "levelId" = $1 ORDER BY completion_date ASC',
        level_id,
    )

    clean_data = [dict(row) for row in data]

    return clean_data
