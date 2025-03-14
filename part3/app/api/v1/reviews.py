from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        if place.get('owner_id') == current_user:
            return {'error': 'You cannot review your own place'}, 400
        reviews_for_place = facade.get_reviews_by_place(review_data['place_id'])
        if any(r['user_id'] == current_user['id'] for r in reviews_for_place):
            return {'error': 'You have already reviewed this place'}, 400
        new_review = facade.create_review(review_data)
        if not new_review:
            return {'error': 'Invalid input data'}, 400
        return new_review, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review['user_id'] != current_user:
            return {'error': 'Unauthorized action'}, 403
        review_data = api.payload
        updated_review = facade.update_review(review_id, review_data)
        if not updated_review:
            return {'error': 'Review not found or invalid data'}, 404
        return updated_review, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review['user_id'] != current_user:
            return {'error': 'Unauthorized action'}, 403
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


# Impossible to have /api/v1/places/<place_id>/reviews
# without changing the other routes and changing
# the reviews namespace path (not the best practice)
# or moving this to the places review could work to keep
# @api.route('/places/<place_id>/reviews') as /api/v1/places/<place_id>/reviews
@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'No reviews found for this place'}, 404
        return reviews, 200
