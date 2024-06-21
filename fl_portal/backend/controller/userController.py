from typing import List
from fastapi import HTTPException, status
from auth.hashing import Hash
from auth.jwttoken import create_access_token
from bson import ObjectId
from config.config import db
from schemas.userSchemas import serializeDict, serializeList
from models.userModel import User

async def get_all_users() -> List[dict]:
    """
    Get all users from the database and serialize them into a list of dictionaries.
    Returns: List[dict]: A list of all user documents serialized as dictionaries.
    Exception: Incase of any errors.
    """
    try:
        users = db.find()
        return serializeList(users)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def create_user_logic(user_data) -> str:
    """
    Create a new user in the database with hashed password.
    Args: user_data: username, password, type, group, topology and email.
    Returns: str: The ID of the newly created user.
    Exception: Incase of any errors.
    """
    try:
        hashed_pass = Hash.bcrypt(user_data.password)
        user_object = dict(user_data)
        user_object["password"] = hashed_pass
        user_id = db.insert_one(user_object).inserted_id
        return str(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def authenticate_user(username, password) -> str:
    """
    Authenticate a user by verifying the username and password.
    Args: username and password.
    Returns: str: A JWT access token if authentication is successful.
    Exception: HTTPException: If the user is not found or if the password is incorrect.
    """
    try:
        user = db.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user found with this {username} username')
        if not Hash.verify(user["password"], password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong Username or password')
        access_token = create_access_token(data={"sub": user["username"]})
        return access_token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_users_by_type(user_type: str) -> List[dict]:
    """
    Get users from the database based on their type and serialize them into a list of dictionaries.
    Args: user_type: "Data Provider" and "Data Scientist".
    Returns: List[dict]: A list of user documents of the specified type serialized as dictionaries.
    """
    try:
        users = db.find({"type": user_type})
        return serializeList(users)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_users_by_type_topology(user_type: str, user_topology: str) -> List[dict]:
    """
    Get users from the database based on their type, topology and serialize them into a list of dictionaries.
    Args: user_type: "Data Provider" and "Data Scientist".
    Returns: List[dict]: A list of user documents of the specified type serialized as dictionaries.
    """
    try:
        users = db.find({"type": user_type, "topology": user_topology})
        return serializeList(users)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_user(user_id: str, current_user: User) -> str:
    """
    Delete a user, Requires user authentication.
    Args: user_id: to delete, current_user (User): The current authenticated user.
    Returns: Status of deletion request
    """
    try:
        result = db.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return "User deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
