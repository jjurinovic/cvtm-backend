from fastapi import HTTPException, status


def InvalidPassword():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Invalid password'
    )


def InvalidCredentials():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Invalid credentials'
    )


def NoValidCredentials():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
