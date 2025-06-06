from db import get_db
from collections import OrderedDict #To add RecordOrder field

class Asset:
    # Get All Assets for management menu
    @staticmethod
    def get_all_assets():
        db = get_db()
        return db.execute("SELECT * FROM Assets").fetchall()
    
    #Get Asset details by ID, returns asset details as dictionary to add RecordOrder field
    @staticmethod
    def get_asset_by_id(asset_id):
        db = get_db()
        row = db.execute("SELECT * FROM Assets WHERE AssetID = ?", (asset_id,)).fetchone()
        if row:
            return OrderedDict([ 
            ("RecordOrder", "AssetID|Name|Type|Status"),  
            ("AssetID", row["AssetID"]),
            ("Name", row["Name"]),
            ("Type", row["Type"]),
            ("Status", row["Status"])
            ])
        return None
    
    #Create Asset using the passed in data
    @staticmethod
    def add_asset(data):
        db = get_db()
        query = """
            INSERT INTO Assets (Name, Type, Status)
            VALUES (?, ?, ?)
        """
        db.execute(query, (data['Name'], data['Type'], data['Status']))
        db.commit()
        
    #Update Asset using Asset ID and passed in data
    @staticmethod
    def update_asset(asset_id, data):
        db = get_db()
        query = """
            UPDATE Assets
            SET AssetID = ?, Name = ?, Type = ?, Status = ?
            WHERE AssetID = ?
        """
        db.execute(
            query,
            (data['AssetID'], data['Name'], data['Type'], data['Status'], asset_id)
        )
        db.commit()
        
   
#Delete Asset by ID
    @staticmethod
    def delete_asset(asset_id):
        db = get_db()
        query = "DELETE FROM Assets WHERE AssetID = ?"
        db.execute(query, (asset_id,))
        db.commit()

   


