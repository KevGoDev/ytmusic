import logging
from typing import Optional

from flask import Blueprint, Response, request, session

from api import error_json, success_json
from models.user import User
from utils.database import db_scope
from utils.user import check_email_valid, verify_password

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register() -> tuple[Response, int]:
    if not request.json:
        return error_json("No form data")
    username: Optional[str] = request.json.get("username")
    email: Optional[str] = request.json.get("email")
    password: Optional[str] = request.json.get("password")
    confirm_password: Optional[str] = request.json.get("confirm_password")

    # check if the required fields are not empty
    if not username or username.strip() == "":
        return error_json("Username is required")
    if not email or email.strip() == "":
        return error_json("Email is required")
    if not password or password.strip() == "":
        return error_json("Password is required")
    if not confirm_password or confirm_password.strip() == "":
        return error_json("Confirm password is required")

    # check if the password and confirm_password are the same
    if password != confirm_password:
        return error_json("Passwords don't match")

    # check password strength
    if len(password) < 8:
        return error_json("Password is too short, 8 characters minimum")

    # Check if email seems valid
    if not check_email_valid(email):
        return error_json("Email is not valid")

    # create the user
    with db_scope() as db:
        user: User = User.create(db, username, email, password)
        db.commit()
        return success_json(data={"user": user.to_dict()})


@bp.post("/login")
def login() -> tuple[Response, int]:
    if not request.json:
        return error_json("No form data")
    username: Optional[str] = request.json.get("username")
    password: Optional[str] = request.json.get("password")

    # check if the required fields are not empty
    if not username or username.strip() == "":
        return error_json("Username is required")
    if not password or password.strip() == "":
        return error_json("Password is required")

    # create the user
    with db_scope() as db:
        user: Optional[User] = User.get_by_username(db, username)
        if not user or not verify_password(password.encode(), user.password):
            return error_json("Invalid username or password")
        session["user_id"] = user.id
        session["username"] = user.username
        return success_json(data={"user": user.to_dict()})


@bp.route("/logout", methods=["POST", "GET"])
def logout() -> tuple[Response, int]:
    session.clear()
    return success_json()


@bp.get("/me")
def me() -> tuple[Response, int]:
    if "user_id" not in session:
        return error_json("Not logged in")
    with db_scope() as db:
        user: Optional[User] = User.get_by_id(db, session["user_id"])
        if not user:
            logging.error("User from session not found in db, clearing session.")
            session.clear()
            return error_json("Not logged in")
        return success_json(data={"user": user.to_dict()})
