from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from app.models import User

from . import api
from app.exceptions import ValidationError

@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email is None or email == "":
        raise ValidationError("Email ID can't be empty")
    if password is None or password == "":
        raise ValidationError("Password can't be empty")
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise ValidationError("User with given Email ID not found.")
    right_password_flag =user.verify_password(password)
    if not right_password_flag:
        raise ValidationError("User email Id or password incorrect.")
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, email=email, username = user.username)
