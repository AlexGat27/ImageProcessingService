from flask import Flask
from abc import abstractmethod, ABC

class BaseFlask(ABC):
    def __init__(self, name: str):
        self.app = Flask(name)
    
    @abstractmethod
    def register_routes(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def run(self, port: int, debug=True):
        self.register_routes()
        self.app.run(port=port, debug=debug)
