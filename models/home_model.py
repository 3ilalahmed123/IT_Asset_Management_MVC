from db import get_db

class Home:
    # Get My asssets table view passing in the User ID
    @staticmethod
    def get_my_assets(user_id):
        db = get_db()
        query = """
        SELECT 
            Assets.AssetID, 
            Assets.Name, 
            Assets.Type, 
            Assets.Status, 
            Loans.LoanDate, 
            Loans.LoanID,
            Loans.ReturnDate
        FROM 
            Assets
        INNER JOIN 
            Loans ON Assets.AssetID = Loans.AssetID
        WHERE 
            Loans.UserID = ? 
            AND Loans.ReturnDate IS NULL 
            AND Assets.Status IN ('Assigned', 'Service/Repair')
            AND Loans.LoanID = (
                SELECT MAX(LoansSub.LoanID)
                FROM Loans AS LoansSub
                WHERE LoansSub.AssetID = Loans.AssetID
                AND LoansSub.ReturnDate IS NULL
            )
        """
        return db.execute(query, (user_id,)).fetchall()

    # Get My previous assets table view passing in the User ID
    @staticmethod
    def get_previous_assets(user_id):
        db = get_db()
        query = """
    SELECT 
        Assets.AssetID, 
        Assets.Name, 
        Assets.Type, 
        Assets.Status, 
        Loans.LoanDate, 
        Loans.ReturnDate, 
        Loans.LoanID
    FROM 
        Assets
    INNER JOIN 
        Loans ON Assets.AssetID = Loans.AssetID
    WHERE 
        Loans.UserID = ? 
        AND Loans.ReturnDate IS NOT NULL
    """
        return db.execute(query, (user_id,)).fetchall()
    
    # Get User full name from User table view by passing in the User ID
    @staticmethod
    def get_fullname(user_id):
        db = get_db()
        query = """
    SELECT 
        Forename, 
        Surname
    FROM 
        Users
    WHERE 
        UserID = ?
    """
        row = db.execute(query, (user_id,)).fetchone()
        return row["Forename"] + " " + row["Surname"] if row else None
    
    #Get all assets which are unassigned
    @staticmethod
    def get_available_assets():
        db = get_db()
        query = """
    SELECT 
        AssetID, 
        Name, 
        Type
    FROM 
        Assets
    WHERE 
        Status = 'Unassigned'
    """
        assets = db.execute(query).fetchall()
        #print("Available Assets:", assets)  # Debugging
        return assets

    #DB update for returning a loaned asset
    @staticmethod ##Interacts with loan table
    def return_asset(asset_id, loan_id):
        db = get_db()
        query = """
            UPDATE Loans
            SET ReturnDate = CURRENT_DATE
            WHERE LoanID = ? AND AssetID = ?
        """
        
        db.execute(query, (loan_id, asset_id))
        db.execute("UPDATE Assets SET Status = 'Unassigned' WHERE AssetID = ?", (asset_id,))
        db.commit()

    #DB updates for loaning an asset to a user
    @staticmethod
    def loan_asset(asset_id, user_id):
        db = get_db()
        query = """
            INSERT INTO Loans (AssetID, UserID, LoanDate)
            VALUES (?, ?, CURRENT_DATE)
        """
        db.execute(query, (asset_id, user_id))
        db.execute("UPDATE Assets SET Status = 'Assigned' WHERE AssetID = ?", (asset_id,))
        db.commit()

    #DB update for changing asset status to 'Assigned' when a complete repair button selected by passing in the asset id
    @staticmethod
    def complete_repair(asset_id):
        db = get_db()
        query = """
            UPDATE Assets
            SET Status = 'Assigned'
            WHERE AssetID = ?
        """
        db.execute(query, (asset_id,))
        db.commit()
    
    #DB update for changing asset status to 'Service/Repair' when the Service/Repair is button selected by passing in the asset id
    @staticmethod
    def report_repair(asset_id, loan_id):
        db = get_db()
        query = """
            UPDATE Assets
            SET Status = 'Service/Repair'
            WHERE AssetID = ?
        """
        db.execute(query, (asset_id,))
        db.commit()



