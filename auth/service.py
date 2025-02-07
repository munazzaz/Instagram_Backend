# bussiness logic

from fastapi import Depends
from .schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime
from .models import User

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # hashing password
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256" #encoding our jwt
TOKEN_EXPIRE_MINS = 60 * 24 * 30 # 30 Days

# check for existing user
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(User).filter(User.email == email).first()
    return db_user

# create access token
async def create_access_token(username: str, id: int):
    encode = {"sub": username, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")
        if datetime.fromtimestamp(expires) < datetime.now(): # I ADDED TYPE
            return None
        if username is None or id is None: 
            return None
        return db.query(User).filter(User.id == id).first()
    except JWTError:
        return None
    
# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# create user
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email = user.email.lower().strip(),
        username = user.username.lower().strip(),
        hashed_password = bcrypt_context.hash(user.password),
        dob = user.dob or None,
        gender = user.gender or None,
        bio = user.bio or None,
        location = user.location or None,
        profile_pic = user.profile_pic or None,
        name = user.name or None
    )
    db.add(db_user)
    db.commit()
    return db_user

# authentication
async def authenticate(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user

# # update user
# async def update_user(db: Session, db_user: User, user_update: UserUpdate):
#     db_user.bio = user_update.bio or db_user.bio
#     db_user.name = user_update.name or db_user.bio
#     db_user.dob = user_update.dob or db_user.bio
#     db_user.gender = user_update.gender or db_user.bio
#     db_user.location = user_update.location or db_user.bio
#     db_user.profile_pic = user_update.profile_pic or db_user.bio

#     db.commit()






# # update user
# async def update_user(db: Session, db_user: User, user_update: UserUpdate):
#     if user_update.bio is not None:
#         db_user.bio = user_update.bio
#     if user_update.name is not None:
#         db_user.name = user_update.name
#     if user_update.dob is not None:
#         db_user.dob = user_update.dob
#     if user_update.gender is not None:
#         db_user.gender = user_update.gender
#     if user_update.location is not None:
#         db_user.location = user_update.location
#     if user_update.profile_pic is not None:
#         db_user.profile_pic = user_update.profile_pic

#     db.commit()
#     db.refresh(db_user)
#     return db_user




# update user
# async def update_user(db: Session, db_user: User, user_update: UserUpdate):
#     db_user.bio = user_update.bio or db_user.bio
#     db_user.name = user_update.name or db_user.name
#     db_user.dob = user_update.dob or db_user.dob
#     db_user.gender = user_update.gender or db_user.gender
#     db_user.location = user_update.location or db_user.location
#     db_user.profile_pic = user_update.profile_pic or db_user.profile_pic

#     db.commit()
#     db.refresh(db_user)  # Add this line to refresh the updated user data
#     return db_user  # Return the updated user

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# update user
async def update_user(db: Session, db_user: User, user_update: UserUpdate):
    logging.debug(f"Current db_user state before update: {db_user}")
    logging.debug(f"Incoming update data: {user_update}")

    # Update only the fields that are provided
    if user_update.bio is not None:
        db_user.bio = user_update.bio
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.dob is not None:
        db_user.dob = user_update.dob
    if user_update.gender is not None:
        db_user.gender = user_update.gender
    if user_update.location is not None:
        db_user.location = user_update.location
    if user_update.profile_pic is not None:
        db_user.profile_pic = user_update.profile_pic

    db.commit()
    db.refresh(db_user)  # Refresh to get the latest state from the DB

    logging.debug(f"Updated db_user state after commit: {db_user}")

    return db_user


# from fastapi import Depends
# from sqlalchemy.orm import Session

# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from datetime import timedelta, datetime

# from .models import User
# from .schemas import UserCreate, UserUpdate

# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # hasing password
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"  # encoding our jwt
# TOKEN_EXPIRE_MINS = 60 * 24 * 30  # 30 days


# # check for existing user
# async def existing_user(db: Session, username: str, email: str):
#     db_user = db.query(User).filter(User.username == username).first()
#     if db_user:
#         return db_user
#     db_user = db.query(User).filter(User.email == email).first()
#     return db_user


# # create access token
# async def create_access_token(username: str, id: int):
#     encode = {"sub": username, "id": id}
#     expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
#     encode.update({"exp": expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# # get current user from token
# async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         id: str = payload.get("id")
#         expires: datetime = payload.get("exp")
#         if datetime.fromtimestamp(expires) < datetime.now():
#             return None
#         if username is None or id is None:
#             return None
#         return db.query(User).filter(User.id == id).first()
#     except JWTError:
#         return None


# # get user from user id
# async def get_user_from_user_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()


# # create user
# async def create_user(db: Session, user: UserCreate):
#     db_user = User(
#         email=user.email.lower().strip(),
#         username=user.username.lower().strip(),
#         hashed_password=bcrypt_context.hash(user.password),
#         # dob=user.dob or None,
#         # gender=user.gender or None,
#         # bio=user.bio or None,
#         # location=user.location or None,
#         # profile_pic=user.profile_pic or None,
#         # name=user.name or None,
#     )
#     db.add(db_user)
#     db.commit()

#     return db_user


# # authentication
# async def authenticate(db: Session, username: str, password: str):
#     db_user = db.query(User).filter(User.username == username).first()
#     if not db_user:
#         print("no user")
#         return None
#     if not bcrypt_context.verify(password, db_user.hashed_password):
#         return None
#     return db_user


# # update user
# async def update_user(db: Session, db_user: User, user_update: UserUpdate):
#     db_user.bio = user_update.bio or db_user.bio
#     db_user.name = user_update.name or db_user.bio
#     db_user.dob = user_update.dob or db_user.bio
#     db_user.gender = user_update.gender or db_user.bio
#     db_user.location = user_update.location or db_user.bio
#     db_user.profile_pic = user_update.profile_pic or db_user.bio

#     db.commit()