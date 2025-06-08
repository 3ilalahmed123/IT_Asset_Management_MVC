from flask import Blueprint, render_template, session, request, jsonify
from models.user_model import User
from models.asset_model import Asset
from models.loan_model import Loan

management_bp = Blueprint('management', __name__)


#Function to ensure user is an Admin
def admin_required():
    if session.get('role') != 'Admin':
        return jsonify({"error": "Unauthorized access"}), 403
    return None

# Route for /management, get data from models and pass to management.html
@management_bp.route('/')
def index():
    auth_check = admin_required() # Check if user is admin
    if auth_check: return auth_check  # Deny access if not admin
    users = User.get_all_users()
    assets = Asset.get_all_assets()
    loans = Loan.get_all_loans()
    return render_template('management.html', users=users, assets=assets, loans=loans)


#API for record retreival
@management_bp.route('/get-record/<record_type>/<int:record_id>', methods=['GET'])
def get_record(record_type, record_id):
    auth_check = admin_required() # Check if user is admin
    if auth_check: return auth_check  # Deny access if not admin
    # For record type get the record from the respective model
    try:
        if record_type.lower() == "user":
            record = User.get_user_by_id(record_id)  # Fetch record using User model
        elif record_type.lower() == "asset":
            record = Asset.get_asset_by_id(record_id)  # Fetch record using Asset model
        elif record_type.lower() == "loan":
            record = Loan.get_loan_by_id(record_id)  # Fetch record using Loan model
        else:
            return jsonify({"message": "Invalid record type."}), 400 #Throw error if no matching record type

        if record:
            return jsonify(record), 200
        return jsonify({"message": "Record not found."}), 404 #Throw error if no record

    except Exception as e:
        return jsonify({"message": f"Error fetching record: {e}"}), 500
    
#API for record update
@management_bp.route('/update-record/<record_type>/<int:record_id>', methods=['POST'])
def update_record(record_type, record_id):
    auth_check = admin_required() # Check if user is admin
    if auth_check: return auth_check  # Deny access if not admin
    try:
        # Get record data from request body
        record_data = request.get_json()
        # For record type update the record from the respective model
        if record_type.lower() == "user":
            User.update_user(record_id, record_data)  # Update record using User model
        elif record_type.lower() == "asset":
            Asset.update_asset(record_id, record_data) # Update record using Asset model
        elif record_type.lower() == "loan":
            Loan.update_loan(record_id, record_data) # Update record using Loan model
        else:
            return jsonify({"message": "Invalid record type."}), 400 #Throw error if no matching record type
        return jsonify({"message": f"{record_type.capitalize()} record updated successfully."}), 200
    except Exception as e: #Catch any exception and return error
        return jsonify({"message": f"Error updating record: {e}"}), 500

#API for record creation
@management_bp.route('/add-record/<record_type>', methods=['POST'])
def add_record(record_type):
    auth_check = admin_required() # Check if user is admin
    if auth_check: return auth_check  # Deny access if not admin
    try:
        # Get record data from the request body
        record_data = request.get_json()

        # For record type add the record using the respective model
        if record_type.lower() == "user":
            User.add_user(record_data) # Add record using User model
        elif record_type.lower() == "asset":
            Asset.add_asset(record_data) # Add record using User model
        elif record_type.lower() == "loan":
            Loan.add_loan(record_data) # Add record using User model
        else:
            return jsonify({"message": "Invalid record type."}), 400 #Throw error if no matching record type
        return jsonify({"message": f"{record_type.capitalize()} record added successfully."}), 201
    except Exception as e: #Catch any exception and return error
        return jsonify({"message": f"Error adding record: {e}"}), 500

#API for record deletion
@management_bp.route('/delete-record/<record_type>/<int:record_id>', methods=['POST'])
def delete_record(record_type, record_id):
    auth_check = admin_required() # Check if user is admin
    if auth_check: return auth_check  # Deny access if not admin
    try:
        # For record type delete the record using the respective model
        if record_type.lower() == "user":
            User.delete_user(record_id) # Delete record using User model
        elif record_type.lower() == "asset":
            Asset.delete_asset(record_id) # Delete record using User model
        elif record_type.lower() == "loan":
            Loan.delete_loan(record_id) # Delete record using User model
        else:
            return jsonify({"message": "Invalid record type."}), 400 #Throw error if no matching record type

        return jsonify({"message": f"{record_type.capitalize()} record deleted successfully."}), 200
    except Exception as e: #Catch any exception and return error
        return jsonify({"message": f"Error deleting record: {e}"}), 500
    



