from fastapi import HTTPException, status


def TimeEntryNotFound():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Time Entry not found!")


def NotAllowedTimeEntries():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You are not allowed to get time entries!")
