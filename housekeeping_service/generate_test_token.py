import jwt
from datetime import datetime, timedelta, UTC

# This matches the dummy key in your docker-compose.yml
SECRET_KEY = "dummy_key_for_testing"

def generate_demo_token(user_id: str = "housekeeping_admin"):
    """
    Generates a dummy JWT for manual testing in Swagger UI.
    """
    payload = {
        "sub": user_id,
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + timedelta(hours=24),
        "roles": ["admin", "staff"]
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

if __name__ == "__main__":
    token = generate_demo_token()
    print("\n--- Demo JWT Token ---")
    print(token)
    print("----------------------\n")
    print("Copy the token string above and paste it into the 'Authorize' box in Swagger UI.")
