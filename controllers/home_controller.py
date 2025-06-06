from flask import Blueprint, render_template, session, request, jsonify
from models.home_model import Home

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    user_id = session.get('user_id')
    sessionUsername = Home.get_fullname(user_id)
    sessionRole = session.get('role')
    # Fetch data from Home Model
    my_assets = Home.get_my_assets(user_id)
    previous_assets = Home.get_previous_assets(user_id)
    available_assets = Home.get_available_assets()
    #return render_template('home.html', assets=assets, loans=loans)
    #print(my_assets, previous_assets,available_assets)

    return render_template(
        'home.html',
        username=sessionUsername,
        role = sessionRole,
        my_assets=my_assets,
        previous_assets=previous_assets,
        available_assets=available_assets
    )

@home_bp.route('/handle-action', methods=['POST'])
def handle_action():
    try:
        # Get data from request
        data = request.get_json()
        action_type = data.get('actionType')
        asset_id = data.get('assetId')
        loan_id = data.get('loanId', None)

        # Depending on action type run corresponding function from model
        if action_type == 'return':
            Home.return_asset(asset_id, loan_id)
        elif action_type == 'repair':
            Home.report_repair(asset_id, loan_id)
        elif action_type == 'complete-repair':
            Home.complete_repair(asset_id)
        elif action_type == 'loan':
            user_id = session.get('user_id')
            Home.loan_asset(asset_id, user_id)
        else:
            return jsonify({"message": "Invalid action type."}), 400

        return jsonify({"message": f"Action '{action_type}' completed successfully."}), 200

    except Exception as e:
        return jsonify({"message": f"Error processing action: {e}"}), 500

