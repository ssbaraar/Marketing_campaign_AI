import streamlit as st
from database import users
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    if not token:
        return None
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"Token verification error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected token error: {e}")
        return None

def hash_password(password: str):
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str):
    return pbkdf2_sha256.verify(password, hashed_password)

def register_user(email: str, password: str, name: str):
    if users.find_one({"email": email}):
        return False, "Email already registered"
    
    hashed_password = hash_password(password)
    user = {
        "email": email,
        "password": hashed_password,
        "name": name,
        "created_at": datetime.utcnow()
    }
    users.insert_one(user)
    return True, "Registration successful"

def login_user(email: str, password: str):
    user = users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return False, "Invalid email or password"
    
    # Update last login time
    users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create token with proper encoding
    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    
    try:
        access_token = create_access_token(token_data)
        return True, {
            "token": access_token,
            "user_id": str(user["_id"]),
            "name": user["name"]
        }
    except Exception as e:
        print(f"Token creation error: {e}")
        return False, "Authentication error"

def check_auth():
    """Check if user is authenticated"""
    try:
        if "user_token" not in st.session_state:
            st.warning("Please log in to access this feature")
            st.session_state.clear()
            st.experimental_rerun()
        
        payload = verify_token(st.session_state.user_token)
        if not payload:
            st.warning("Session expired. Please log in again")
            st.session_state.clear()
            st.experimental_rerun()
        
        return payload["sub"]
    except Exception as e:
        print(f"Auth check error: {e}")
        st.session_state.clear()
        st.experimental_rerun()

def login_page():
    st.title("📧 Email Marketing Team - Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        email = st.text_input("Email", key="login_email_input")
        password = st.text_input("Password", type="password", key="login_password_input")
        
        # Add unique key to login button
        if st.button("Login", key="login_button_main"):
            success, result = login_user(email, password)
            if success:
                st.session_state.user_token = result["token"]
                st.session_state.user_id = result["user_id"]
                st.session_state.user_name = result["name"]
                st.session_state.authenticated = True
                st.success(f"Welcome back, {result['name']}!")
                st.experimental_rerun()
            else:
                st.error(result)
    
    with tab2:
        name = st.text_input("Name", key="register_name_input")
        email = st.text_input("Email", key="register_email_input")
        password = st.text_input("Password", type="password", key="register_password_input")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_input")
        
        # Add unique key to register button
        if st.button("Register", key="register_button_main"):
            if password != confirm_password:
                st.error("Passwords do not match")
            elif not name or not email or not password:
                st.error("All fields are required")
            else:
                success, result = register_user(email, password, name)
                if success:
                    st.success(result)
                    st.info("Please login with your credentials")
                else:
                    st.error(result)
