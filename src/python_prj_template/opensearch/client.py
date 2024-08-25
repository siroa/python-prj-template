import toml
from opensearchpy import OpenSearch
from python_prj_template.logger.logger import Logger
from typing import Any
import sys

class Client:
    def __init__(self) -> None:
         self.client: OpenSearch = OpenSearch()
         self._log: Logger = Logger(self.__class__.__name__)
         self.config: dict[str, Any] = {}


    def read_config(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            self.config = toml.load(f)
            self._log.logger.info("reading complete:" + filepath)

    def create_client(self) -> None:
        host: str = self.config["opensearch"]["host"]
        port: int = self.config["opensearch"]["port"]
        user: str = self.config["opensearch"]["user"]
        password: str = self.config["opensearch"]["password"]
        use_ssl: bool = self.config["opensearch"]["use_ssl"]
        verify_certs: bool = self.config["opensearch"]["verify_certs"]
        ssl_show_warn: bool = self.config["opensearch"]["ssl_show_warn"]
        auth = (user, password)

        try:
            client = OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth=auth,
                use_ssl=use_ssl,
                verify_certs=verify_certs,
                ssl_show_warn=ssl_show_warn,
            )
            self._log.logger.info(client.info())
            self._log.logger.info("connect success")
            self.client = client
        except Exception as e:
            self._log.logger.error(e)
            sys.exit(1)
