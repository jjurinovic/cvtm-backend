from fastapi import HTTPException, status


def AddressNotFound():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Address not found!'
    )
