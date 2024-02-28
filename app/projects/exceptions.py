from fastapi import HTTPException, status


def ProjectNotFound():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found!"
    )


def UserAlreadyAssigned():
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User already assigned to project!"
    )
