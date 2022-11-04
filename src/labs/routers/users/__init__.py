""" User related routes to manage accounts

This should only be accessible to admin users, and are endpoints
used to manage user accounts. For the template application this
was built to test out the initial CRUD features.
"""
from datetime import datetime
from uuid import UUID
from typing import List
from http import HTTPStatus

from fastapi import APIRouter, Depends,\
    HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models import User
from ...schema import UserResponse, UserRequest

router = APIRouter(tags=["user"])

@router.get(
    "", 
    summary="Query users between limits",
    response_model=List[UserResponse],
    status_code=HTTPStatus.OK
)
async def get_users_with_limits(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session)
):
    users = await User.get_all_in_range(
        session,
        offset=offset,
        limit=limit
    )
    return users

@router.get(
    "/infinite", 
    summary="Get all users",
    response_model=List[UserResponse],
    status_code=HTTPStatus.OK
)
async def get_users(
    next_id: UUID = None,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get(
    "/{id}", 
    summary="Get a particular user",
    response_model=UserResponse,
    status_code=HTTPStatus.OK
)
async def get_user_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    """ Get a user by their id 
    
    
    """
    user = await User.get(session, id)
    if not user:
        raise HTTPException(404, "User not found")

    return user

@router.delete(
    "/{id}", 
    summary="Delete a particular user",
    status_code=HTTPStatus.NO_CONTENT
)
async def delete_user(
    id: UUID,
    session: AsyncSession = Depends(get_async_session),
    status_code=HTTPStatus.NO_CONTENT
):
    """ Delete a user from the database

    The endpoint will look to see if the user exists, and if so
    will attempt to delete the user from the database and
    return a 204 response. If the user does not exist, a 404
    """
    user = await User.get(session, id)
    if not user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            "User not found"
        )

    result = await User.delete(session, id)
    if not result:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "Unable to delete user"
        )    

@router.patch(
    "/{id}", 
    summary="Update a particular user",
    response_model=UserResponse,
    status_code=HTTPStatus.ACCEPTED
)
async def update_user(
    id: UUID,
    user_request: UserRequest,
    session: AsyncSession = Depends(get_async_session)
):
    user = await User.get(session, id)
    if not user:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            "User not found"
        )

    user = await User.update(
        session,
        id,
        **user_request.dict()
    )

@router.post(
    "", 
    summary="Create a new user",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED
)
async def create_user(
    user_request: UserRequest,
    session: AsyncSession = Depends(get_async_session),
):
    """ Creates a new user based on
    
    """
    user = await User.get_by_email_or_mobile(
        session,
        user_request.email,
        user_request.mobile
    )
    if user:
        raise HTTPException(
            HTTPStatus.CONFLICT,
            "User already exists"
        )

    user = await User.create(
        session,
        **user_request.dict()
    )

    return user
