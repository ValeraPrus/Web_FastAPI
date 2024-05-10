from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_name function returns a list of contacts that match the given parameters.

    :param email: The user email for get.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: A single user object or none.
    :rtype: User | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: Validate the request body.
    :type body: UserSchema
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: Identify the user in the database.
    :type user: User
    :param token: Specify that the token parameter can be a string or none.
    :type token: str | None
    :param db: Pass the database session to the function.
    :type db: Session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.

    :param email: Get the user by email.
    :type email: str
    :param db: Pass the database session into the function.
    :type db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar_url(email: str, url: str | None, db: Session) -> User:
    """
    The update_avatar_url function updates the avatar url of a user.

    :param email: Specify the user's email address.
    :type email: str
    :param url: Specify that the url parameter can either be a string or none.
    :type url: str | None
    :param db: Pass the database session to the function.
    :type db: Session
    :return: A user object.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
