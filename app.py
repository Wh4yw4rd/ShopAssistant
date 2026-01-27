from fastapi import FastAPI, HTTPException, Response, Cookie
from datetime import datetime, timedelta
import secrets

from models import LoginCredentials, CreateUser, DBUser
from security import hash, verify
from db_functions import add_user_to_db, login_user

### Session Parameters ###

# Will look to do this with Redis or database in future

sessions = {}

session_TTL = 86400  # 24 hours (in seconds)

### FastAPI App Initialization ###

app = FastAPI()

### Sample Endpoint ###

@app.get("/")
def index():
    return {"message" : "Hello World!"}


### Login/User Management Endpoints ###

@app.post("/login/")
def login(response : Response, credentials : LoginCredentials, session_id : str | None = Cookie(default=None)):
    """
    Endpoint for login and creating sessions.

    - Removes expired sessions
    - Checks for existing valid session (using session id cookie parameter)
    - Validates user credentials and creates new session if none exists
    """
    # Check if expired sessions
    invalid_sessions = []
    for session in sessions:
        if sessions[session]["created_date"] + timedelta(seconds = session_TTL) < datetime.now():
            invalid_sessions.append(session)
    
    # Remove expired sessions
    for session in invalid_sessions:
        sessions.pop(session)

    # Check for existing valid session for user
    if session_id is not None and session_id in sessions and sessions[session_id]["name"] == credentials.name:
        return {"message" : "Already logged in : " + sessions[session_id]["name"]}
    
    # Create new session
    try:
        user_record = login_user(credentials)

    # Raise error if user not found
    except ValueError as e:
        raise HTTPException(status_code = 401, detail = "Unauthorised: " + str(e))
    
    # Validate password
    if verify(credentials.password, user_record[1]):
        # Save session data to sessions dict (Will move to Redis or database in future)
        new_session = {"name" : user_record[0],
                       "admin" : user_record[2],
                       "created_date" : datetime.now()}
        session_id = secrets.token_hex(16)  # Session ID
        sessions[session_id] = new_session

        # Set session_id cookie to save login (Change secure to True in production with HTTPS)
        response.set_cookie(key = "session_id", value = session_id, max_age = session_TTL, httponly = True, secure = False, samesite = "lax")

        return {"message" : "Login successful"}
    
    # Raise error if password does not match
    else:
        raise HTTPException(status_code = 401, detail = "Unauthorised: Incorrect password")
            

@app.post("/create-user/")
def create_user(credentials : CreateUser, session_id : str | None = Cookie(default=None)):
    """
    Endpoint that allows admin users to create new users and set access level.
    """

    # Check if user in logged in
    if session_id is None or session_id not in sessions:
        raise HTTPException(status_code = 401, detail = "Unauthorized: Please login with an admin user.")
    
    # Check if user is admin
    if sessions[session_id]["admin"] is not True:
        raise HTTPException(status_code = 401, detail = "Unauthorized: Please login with an admin user.")

    # Create new user
    # Hash password for secure storage in database
    hashed_password = hash(credentials.password)

    # Create DBUser model instance for new user
    user = DBUser(
        name = credentials.name,
        password_hash = hashed_password,
        email = credentials.email)
    
    # Add user to database
    try:
        add_user_to_db(user)
    
    except Exception as e:
        # Raised error if username already exists
        if "unique_name" in str(e):
            raise HTTPException(status_code=409, detail="Username already exists")
        
        # Raise error for other database issues
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message" : "User creation successful"}


@app.post("/logout/")
def logout(response : Response, session_id : str | None = Cookie(default=None)):
    """
    Endpopint to logout user by deleting session.
    """
    # Check user is logged in
    if session_id is None or session_id not in sessions:
        raise HTTPException(status_code = 400, detail = "No user logged in.")
    
    # Remove session from sessions dict
    sessions.pop(session_id)

    # Remove session_id cookie
    response.delete_cookie(key = "session_id")

    return {"message" : "Logout successful"}


### Transaction Data Endpoints ###

@app.post("/transaction/update/")
def update_transaction(session_id : str | None = Cookie(default=None)):
    """
    Endpoint to update transaction data.
    """
    # Check user is logged in
    if session_id is None or session_id not in sessions:
        raise HTTPException(status_code = 401, detail = "Unauthorized: Please login to update transaction data.")
    
    return {"message" : "Transaction data updated successfully"}