# app_factory.py
from abc import ABC, abstractmethod

class BaseAppFactory(ABC):

    @abstractmethod
    def create_app(self, type: str):
        pass