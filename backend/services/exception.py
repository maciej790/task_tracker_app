from fastapi import HTTPException

def create_exception(title : str, code : int):
    raise HTTPException(
        status_code=code,
        detail=title,
    )