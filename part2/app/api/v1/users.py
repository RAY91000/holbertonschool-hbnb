from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Define user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'place_list': fields.List(fields.String, description='List of places owned by the user')
})

# Create new user or list users
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {**new_user.to_dict(), 'place_list': new_user.place_list}, 201
    
    @api.response(200, 'User list retrieved')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [{**user.to_dict(), 'place_list': user.place_list} for user in users], 200

# Retrieve, update, or delete a specific user
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {**user.to_dict(), 'place_list': user.place_list}, 200
    
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        updated_data = api.payload
        user = facade.update_user(user_id, updated_data)
        if not user:
            return {'error': 'User not found'}, 404
        return {**user.to_dict(), 'place_list': user.place_list}, 200
    
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        success = facade.delete_user(user_id)
        if success:
            return {'message': 'User deleted successfully'}, 200
        return {'error': 'User not found'}, 404

