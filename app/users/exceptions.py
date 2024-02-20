from fastapi import HTTPException, status


def OnlyRootCanCreateRoot():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Only ROOT user can create another root user"
    )


def EmailAlreadyTaken():
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Email is already taken"
    )


def UserNotFound():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User not found!"
    )


def NotSameCompany():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Company must be same like your company!"
    )


def InvalidPassword():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Invalid password'
    )


def NotAllowedRoleChange():
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"You are not allowed to change your role"
    )
