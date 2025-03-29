from datetime import datetime

def user_dict(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"]
    }

def users_list(users) -> list:
    return [user_dict(user) for user in users]
