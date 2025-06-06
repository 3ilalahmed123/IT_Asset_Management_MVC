from db import get_db
#Return the account if the username and password match
def attempt_login(username, password):
    db = get_db()
    try:
        query = "SELECT UserID, Username, Role FROM Users WHERE Username = ? AND Password = ?"
        user = db.execute(query, (username, password)).fetchone()

        if user:
            return {
                "user_id": user["UserID"],
                "username": user["Username"],
                "role": user["Role"]
            }
        return None
    except Exception as e:
        print(f"Error signing in user: {e}")
        return None
    

#Create user and return
def register_user(forename, surname, username, password):
    db = get_db()
    try:
        query = """
        INSERT INTO Users (Forename, Surname, Username, Password, Role)
        VALUES (?, ?, ?, ?, 'Regular')
        """
        db.execute(query, (forename, surname, username, password))
        db.commit()
        user = db.execute("SELECT UserID, Username, Role FROM Users WHERE Username = ?", (username,)).fetchone()
        if user:
            return {
                "user_id": user["UserID"],
                "username": user["Username"],
                "role": user["Role"]
            }
        return None
    except Exception as e:
        print(f"Error registering user: {e}")
        return None


