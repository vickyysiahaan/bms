from app import app
from resources import user_resources
from flask_restful import Api

api = Api(app)

# USER RESOURCE
api.add_resource(user_resources.UserListResource, '/users')
api.add_resource(user_resources.UserResource, '/users/<int:user_id>')

# USER AUTHENTICATION
api.add_resource(user_resources.UserLogin, '/login')
api.add_resource(user_resources.UserLogoutAccess, '/logout/access')
api.add_resource(user_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_resources.TokenRefresh, '/token/refresh')
api.add_resource(user_resources.SecretResource, '/secret')

