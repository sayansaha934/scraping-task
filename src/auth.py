import jwt
from fastapi import Request,HTTPException

SECRET_KEY = "8cce4ab79941c96c491f325c4a0c26ed"
ALLOWED_EMAILS = ["ssahadev2024@gmail.com"]
# TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbF9pZCI6InNzYWhhZGV2MjAyNEBnbWFpbC5jb20ifQ.9ZO3lmEIgpI1wv3PIkzCg26q_PLp1pvr9vbVzqeBNGQ"
def encode(data):
    # Create the JWT token with the data and expiration time
    encoded_token = jwt.encode(
        payload=data,
        key=SECRET_KEY,
        algorithm="HS256",  # HMAC SHA-256 algorithm for signing the token
    )

    return encoded_token


def decode(token):
    try:
        # Decode the JWT token using the secret key
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_data
    except jwt.exceptions.DecodeError:
        raise jwt.exceptions.DecodeError
    
def authenticate(request:Request):
    decoded_data = decode(request.headers.get('authorization'))
    if decoded_data.get("email_id") not in ALLOWED_EMAILS:
        raise HTTPException(status_code=403, detail="Unauthorized")