import httpx
import subprocess
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from models.userModel import User
from auth.oauth import get_current_user
from controller.userController import *
from controller.metrics import generate_metrics
from config.config import communication_server_ip, path_to_workflow

# Creating a router for user endpoints
user = APIRouter(prefix='/user')

@user.get("/")
async def read_root(current_user: User = Depends(get_current_user)):
    """
    Endpoint to return a welcome message. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: dict: A dictionary containing a welcome message.
    """
    return {"data": "Hello World"}

@user.post('/register')
async def create_user(request: User):
    """
    Endpoint to register a new user.
    Args: request (User): The user data for registration.
    Returns: dict: A dictionary indicating user creation status.
    Exception: HTTP Exception in case of errors.
    """
    try:
        user_id = await create_user_logic(request)
        return {"res": "created", "user_id": user_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to log in a user and return a JWT access token.
    Args: request (OAuth2PasswordRequestForm): The login form data containing username and password.
    Returns: dict: A dictionary containing the access token and token type.
    Exception: HTTPException: If the username or password is invalid.
    """
    try:
        access_token = await authenticate_user(request.username, request.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/all", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of all users.
    """
    try:
        return await get_all_users()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.get("/data_scientists", response_model=List[User])
async def get_data_scientists(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all 'Data Scientists'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of rehistered 'Data Scientists'.
    """
    try:
        return await get_users_by_type("Data Scientist")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/data_providers", response_model=List[User])
async def get_data_providers(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Data Provider'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Data Provider'.
    """
    try:
        return await get_users_by_type("Data Provider")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/data_providers_decentralised", response_model=List[User])
async def get_data_providers_decentralised(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Data Provider' with topology 'Decentralised'.
    Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Data Provider', topology 'Decentralised'.
    """
    try:
        return await get_users_by_type_topology("Data Provider", "Decentralised")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.get("/data_providers_centralised", response_model=List[User])
async def get_data_providers_centralised(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Data Provider' with topology 'Centralised'.
    Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Data Provider', topology 'Centralised'.
    """
    try:
        return await get_users_by_type_topology("Data Provider", "Centralised")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.delete("/{user_id}")
async def remove_user(user_id: str, current_user: User = Depends(get_current_user)):
    """
    Endpoint to delete a user. Requires user authentication.
    Args: user_id: User ID for deletetion, current_user (User): The current authenticated user.
    Returns: Status of deletion request
    """
    try:
        result = await delete_user(user_id, current_user)
        return {"res": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/discover_clients", response_model=List[str])
async def discover_clients(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve a list of registered clients IPs from the communication server. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[str]: A list of clients IPs.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://{communication_server_ip}:8088/discover")
            response.raise_for_status()
            data = response.json()
            client_ips = [item["client_ip"].split(":")[0] for item in data]
        return client_ips
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error communicating with the discovery server")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.post("/initiate_fl")
def initiate_fl(current_user: User = Depends(get_current_user)):
    """
    Endpoint to initiateFL and get result. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: A dictionary containing the output of the initiated FL command.
    """
    try:
        # command = ["cwltool", "hello-world.cwl"]
        # command = ["time", "cwltool", "--enable-ext", "--parallel", "decentralizedFL.cwl", "decentralized_input.yml"]
        # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path_to_workflow)
        # stdout, stderr = process.communicate()
        # logs = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", stderr.decode())
        # execution_time, metrics = generate_metrics(logs)

        command = "(time cwltool --enable-ext --parallel decentralizedFL.cwl decentralized_input.yml) &> output.log"
        subprocess.run(command, shell=True, cwd=path_to_workflow)
        output_file = os.path.join(path_to_workflow, "output.log")
        with open(output_file, "r") as output:
            logs = output.read()
        execution_time, metrics = generate_metrics(logs)
        return {"execution_time": execution_time, "metrics": metrics, "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
