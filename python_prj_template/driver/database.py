from abc import ABCMeta, abstractmethod


class Database(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abstractmethod
    def add(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def update(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key):
        raise NotImplementedError
