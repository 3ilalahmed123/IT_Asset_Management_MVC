from db import get_db

def attemptLogin(username, password):
    db = get_db()
    query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
    user = db.execute(query, (username, password)).fetchone()

    if user:
        print("User found in database!")  # Debug message
        return {
            'user_id': user['UserID'],
            'username': user['Username'],
            'role': user['Role']
        }
    print("No matching user found.")  # Debug message
    return None
