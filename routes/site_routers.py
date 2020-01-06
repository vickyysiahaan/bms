from app import app
from resources import site_resources
from flask_restful import Api

api = Api(app)

# Site RESOURCE
api.add_resource(site_resources.SiteListResource, '/sites')
api.add_resource(site_resources.SiteResource, '/sites/<int:site_id>')
