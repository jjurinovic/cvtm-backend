from fastapi import HTTPException, status


def CompanyNotFound():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Company not found!'
    )
