import csv
import os
from typing import Any

import toml
from injector import Binder, Module, singleton
from opensearchpy import OpenSearch

from python_prj_template.driver.database import Database
from python_prj_template.utils.logger import Logger


# test database
class InMemoryDatabase(Database):
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def add(self, key: str, value: str) -> None:
        self.data[key] = value

    def update(self, key: str, value: str) -> None:
        self.data[key] = value

    def delete(self, key: str) -> None:
        del self.data[key]


class OpenSearchDriver(Database):
    def __init__(self) -> None:
        self.client: OpenSearch = OpenSearch()
        self.config: dict[str, Any] = {}
        self._log: Logger = Logger(self.__class__.__name__)

    def read_config(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            self.config = toml.load(f)
            self._log.logger.info("success " + filepath)

    def create_client(self) -> None:
        host: str = self.config["opensearch"]["host"]
        port: int = self.config["opensearch"]["port"]
        user: str = self.config["opensearch"]["user"]
        password: str = self.config["opensearch"]["password"]
        use_ssl: bool = self.config["opensearch"]["use_ssl"]
        verify_certs: bool = self.config["opensearch"]["verify_certs"]
        ssl_show_warn: bool = self.config["opensearch"]["ssl_show_warn"]
        auth = (user, password)

        client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_auth=auth,
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            ssl_show_warn=ssl_show_warn,
        )
        self.client = client

    def create_index(self, index_name: str) -> None:
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name)

    def insert_csv(self, filepath: str, index_name: str) -> None:
        id = 1
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for data in reader:
                self.client.index(index=index_name, body=data, id=id)
                id += 1

    def get(self, key):
        # TODO: implementation
        pass

    def add(self, key, value):
        # TODO: implementation
        pass

    def update(self, key, value):
        # TODO: implementation
        pass

    def delete(self, key):
        # TODO: implementation
        pass


# 依存の解決
class DataAccessModule(Module):
    def configure(self, binder: Binder) -> None:
        print(type(binder))
        if os.environ.get("test"):
            binder.bind(Database, to=InMemoryDatabase, scope=singleton)  # type: ignore
        else:
            binder.bind(Database, to=OpenSearchDriver, scope=singleton)  # type: ignore
