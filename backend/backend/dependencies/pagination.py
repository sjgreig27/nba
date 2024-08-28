async def pagination_parameters(limit: int = 100, offset: int = 0):
    return {"limit": limit, "offset": offset}
