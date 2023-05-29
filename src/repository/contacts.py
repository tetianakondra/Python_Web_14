from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.
        Args:
            limit (int): The number of contacts to return.
            offset (int): The starting point in the database from which to begin returning contacts.
            user (User): A User object representing the current logged-in user, whose contact list is being returned.
            db (Session): An SQLAlchemy Session object used for querying and updating data in our database.
    
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Get the next set of contacts when the limit is reached
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts
    """
    contacts = db.query(Contact).filter(Contact.user_id ==
                                        user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on the id of that contact.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User who owns this Contact object.
            db (Session): A connection to our database, used for querying and updating data in our tables.
    
    :param contact_id: int: Specify the id of the contact you want to retrieve
    :param user: User: Get the user_id of the current user
    :param db: Session: Access the database
    :return: The first contact found in the database that matches the user_id and id of the contact
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id ==
             user.id)).first()
    return contact


async def get_contact_by_email(contact_email: str, user: User, db: Session):
    """
    The get_contact_by_email function returns a list of contacts that match the contact_email parameter.
        The user parameter is used to filter out contacts that do not belong to the user.
        
    
    :param contact_email: str: Filter the contacts by email
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of contacts that match the email address provided
    """
    contacts = db.query(Contact).filter(
        and_(Contact.user_id == user.id, Contact.email.like(f"%{contact_email}%"))).all()
    return contacts


async def get_contacts_by_first_name(contact_first_name: str, user: User, db: Session):
    """
    The get_contacts_by_first_name function returns a list of contacts that match the first name provided.
        The function takes in a contact_first_name string and user object, and uses the database session to query for
        all contacts with matching first names. It then returns those contacts as a list.
    
    :param contact_first_name: str: Filter the contacts by first name
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts that match the search criteria
    """
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id,
                                             Contact.first_name.like(f"%{contact_first_name}%"))).all()
    return contacts


async def get_contacts_by_last_name(contact_last_name: str, user: User, db: Session):
    """
    The get_contacts_by_last_name function returns a list of contacts that match the last name provided.
        
    
    :param contact_last_name: str: Filter the contacts by last name
    :param user: User: Get the user id of the current logged in user
    :param db: Session: Access the database
    :return: A list of contacts that match the last name provided
    """
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id,
                                             Contact.last_name.like(f"%{contact_last_name}%"))).all()
    return contacts


async def get_contacts_with_birthday(days, user: User, db: Session):
    """
    The get_contacts_with_birthday function returns a list of contacts that have their birthday within the next 'days' days.
        Args:
            days (int): The number of days to look ahead for birthdays.
            user (User): The user whose contacts are being searched through.
            db (Session): A database session object used to query the database for contact information.
    
    :param days: Determine how many days in the future to look for birthdays
    :param user: User: Get the user's id from the database
    :param db: Session: Access the database
    :return: A list of contacts with birthdays in the next n days
    """
    contacts = []
    all_contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in all_contacts:
        birthday_fulldate = str(contact.birthday)
        year_month_day_birth = birthday_fulldate.split(".")
        if len(year_month_day_birth) == 3:
            for i in range(days):
                celebration_day = datetime.now() + timedelta(days=i)
                if year_month_day_birth[2] == celebration_day.day and year_month_day_birth[1] == celebration_day.month:
                    contacts.append(contact)
    return contacts


async def create(body: ContactModel, user: User, db: Session):
    """
    The create function creates a new contact in the database.
        
    
    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A contact object, but the schema expects a contactmodel
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name, phone=body.phone,
                      email=body.email, birthday=body.birthday, description=body.description, user=user)
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update function updates a contact in the database.
        
    
    :param contact_id: int: Identify the contact to be deleted
    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user's id to check if they are allowed to delete a contact
    :param db: Session: Access the database
    :return: The contact object
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    """
    The remove function removes a contact from the database.
        
    
    :param contact_id: int: Specify the contact id of the contact to be removed
    :param user: User: Get the user id from the database
    :param db: Session: Connect to the database
    :return: The contact that was deleted
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
