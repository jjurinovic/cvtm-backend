from fastapi import HTTPException, status


def TimeEntryNotFound():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Time Entry not found!")
