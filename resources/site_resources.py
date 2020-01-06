from app import db
from flask import request
from flask_restful import Resource
from models.sites import Site, SiteSchema

site_schema = SiteSchema()
sites_schema = SiteSchema(many=True)

class SiteListResource(Resource):
    # Site Registration
    def post(self):
        try:
            if Site.find_by_sitename(request.json["site_name"]):
                return {'message': 'Site {} already exists'.format(request.json["username"])}

            new_site = Site(
                site_name=request.json['site_name'],
                city=request.json['city'],
                site_address=request.json['site_address'],
                longitude=request.json['longitude'],
                latitude=request.json['latitude'],
                number_of_string=request.json['number_of_string'],
                total_capacity=request.json['total_capacity']
            )

            db.session.add(new_site)
            db.session.commit()

            return {
                'message': 'Site {} was created'.format(new_site.site_name)
            }

        except:
            return {'message': 'Something went wrong'}, 500

    # Get All Sites
    def get(self):
        sites = Site.query.all()
        return sites_schema.dump(sites)

class SiteResource(Resource):
    # Get Site Data by ID
    def get(self, site_id):
        site = Site.query.get_or_404(site_id)
        return site_schema.dump(site)

    # Edit Site Data by ID
    def patch(self, site_id):
        try:
            site = Site.query.get_or_404(site_id)

            if 'site_name' in request.json:
                site.site_name = request.json['site_name']
            if 'city' in request.json:
                site.city = request.json['city']
            if 'site_address' in request.json:
                site.site_address = request.json['site_address']
            if 'longitude' in request.json:
                site.longitude = request.json['longitude']
            if 'latitude' in request.json:
                site.latitude = request.json['latitude']
            if 'number_of_string' in request.json:
                site.number_of_string = request.json['number_of_string']
            if 'total_capacity' in request.json:
                site.total_capacity = request.json['total_capacity']

            db.session.commit()
            return site_schema.dump(site)
        except:
            return {'message': 'Something went wrong'}, 500

    # Delete Site Data by ID
    def delete(self, site_id):
        site = Site.query.get_or_404(site_id)
        db.session.delete(site)
        db.session.commit()
        return 'SUCCESSFULL', 204
