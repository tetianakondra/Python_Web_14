from typing import List

import redis.asyncio as redis

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from sqlalchemy.orm import Session

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import Contact, User
from src.schemas import ContactResponse, ContactModel, TokenModel, UserDb, UserModel, UserResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.conf.config import settings

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as caches or databases.
    
    :return: A coroutine
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)


@router.get("/", response_model=List[ContactResponse], description='No more than 2 requests per 5 seconds', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, le=200), offset: int = 0, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.
        The limit and offset parameters are used to paginate the results.
    
    
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned to 200
    :param offset: int: Specify the offset of the first record to return
    :param db: Session: Access the database
    :param current_user: User: Get the user from the database
    :return: A list of contact objects
    """
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 2 requests per 5 seconds', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
        Args:
            contact_id (int): The id of the contact to be returned.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
        Returns:
            Contact: A single Contact object matching the given id or None if no match is found.&lt;/code&gt;
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.get("/email/", response_model=List[ContactResponse])
async def get_contact(contact_email: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by email.
    
    :param contact_email: str: Get the contact email from the url path
    :param db: Session: Access the database
    :param current_user: User: Get the user from the database
    :return: A contact object
    """
    contact = await repository_contacts.get_contact_by_email(contact_email, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.get("/first_name/", response_model=List[ContactResponse])
async def get_contact(contact_first_name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by first name.
    
    :param contact_first_name: str: Get the first name of the contact
    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts_by_first_name(contact_first_name, current_user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.get("/last_name/", response_model=List[ContactResponse])
async def get_contact(contact_last_name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by last name.
    
    :param contact_last_name: str: Pass the last name of the contact to be retrieved
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A list of contacts that match the last_name parameter
    """
    contacts = await repository_contacts.get_contacts_by_last_name(contact_last_name, current_user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_contact(days: int = 7, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a list of contacts with birthdays in the next 7 days.
        The default number of days is 7, but this can be changed by passing an integer to the function.
        If no contacts are found, it will return a 404 error.
    
    :param days: int: Get the number of days to look for contacts with birthdays
    :param db: Session: Access the database
    :param current_user: User: Get the user_id from the jwt token
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts_with_birthday(days, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 2 requests per 5 seconds', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes a ContactModel object as input and returns the newly created contact.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Access the database
    :param current_user: User: Get the user who is currently logged in
    :return: A contactmodel object
    """
    contact = await repository_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and db as parameters.
        It returns the updated contact.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Specify the id of the contact to be updated
    :param db: Session: Access the database
    :param current_user: User: Get the user who is making the request
    :return: A contactmodel
    """
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object for authentication and authorization purposes. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: None
    """
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return None
