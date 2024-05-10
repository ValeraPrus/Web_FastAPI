from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import extract, and_

from src.database.models import Contact, User
from src.schemas import ContactResponse


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts that match the given parameters.


    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contacts_by_name(name: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_name function returns a list of contacts that match the given parameters.


    :param name: The name of contact for get.
    :type name: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """
    return db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).all()


async def get_contacts_by_surname(surname: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_surname function returns a list of contacts that match the given parameters.


    :param surname: The surname of contact for get.
    :type name: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contacts]
    """
    return db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).all()


async def get_contacts_nearest_7_days_birthday(user: User, db: Session) -> List[Contact]:

    today = datetime.now().date()
    cday7 = today + timedelta(days=7)

    if today.month == 12:

        return db.query(Contact).filter(
            (
                (extract('month', Contact.birthday) >= today.month)
                | ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day))
                | ((extract('month', Contact.birthday) == 1) & (today.month == 12))
                & Contact.user_id == user.id
            )
            &
            (
                (extract('month', Contact.birthday) > cday7.month)
                | ((extract('month', Contact.birthday) == cday7.month) & (extract('day', Contact.birthday) <= cday7.day))
                | ((extract('month', Contact.birthday) == 1) & (cday7.month == 1) & (extract('day', Contact.birthday) <= cday7.day))
                & Contact.user_id == user.id
            )
        ).all()

    else:

        return db.query(Contact).filter(
            (
                (extract('month', Contact.birthday) > today.month)
                | ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day))
                & Contact.user_id == user.id
            )
            &
            (
                (extract('month', Contact.birthday) < cday7.month)
                | ((extract('month', Contact.birthday) == cday7.month) & (extract('day', Contact.birthday) <= cday7.day))
                & Contact.user_id == user.id
            )
        ).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function returns a contact from the database.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    res = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return res


async def get_contact_by_email(email: int, user: User, db: Session) -> Contact:
    """
    The get_contact_by_email function takes an email address and returns the user associated with that email.


    :param email: Specify the email address of the user to retrieve.
    :type email: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A single user object or none.
    :rtype: Contact | None
    """
    res = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()
    return res


async def create_contact(body: ContactResponse, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone,
                      birthday=body.birthday, additional=body.additional, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactResponse, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact that was removed.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
