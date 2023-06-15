from fastapi import APIRouter, Form, File, HTTPException
from app.service.auth import authenticate_user, create_access_token

router = APIRouter()

@router.post("/signin/")
async def sign_in(username: str = Form(...), password: str = Form(...)):
    """
    Sign-in route for user authentication.

    Parameters:
    - username: The username for authentication.
    - password: The password for authentication.

    Returns:
    - A dictionary containing the access_token and token_type.
    """
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}