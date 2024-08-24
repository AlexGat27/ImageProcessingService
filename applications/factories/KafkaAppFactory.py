from applications.factories import BaseAppFactory
from ApplicationEnums import AppNames

class KafkaAppFactory(BaseAppFactory):

    def create_app(type: str):
        if type == AppNames.ADMIN:
            pass
        elif type == AppNames.GEOSYSTEM:
            pass
        elif type == AppNames.UNITY:
            pass