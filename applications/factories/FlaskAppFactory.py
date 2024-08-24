from applications.factories import BaseAppFactory
from applications.flask import AdminFlask, GeosystemFlask, UnityFlask
from applications.ApplicationEnums import AppNames

class FlaskAppFactory(BaseAppFactory):

    def create_app(self, type):
        if type == AppNames.ADMIN:
            return AdminFlask()
        elif type == AppNames.GEOSYSTEM:
            return GeosystemFlask()
        elif type == AppNames.UNITY:
            return UnityFlask()
        else:
            raise ValueError(f"Unknown app type: {type}")
