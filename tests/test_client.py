import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
import toml
from python_prj_template.opensearch.client import Client  # あなたのClientクラスが定義されているモジュールをインポート

class TestClient:

    @patch("python_prj_template.opensearch.client.Logger")  # Loggerをモック
    @patch("python_prj_template.opensearch.client.toml.load")  # toml.loadをモック
    def test_read_config(self, mock_toml_load, mock_logger):
        # モックのセットアップ
        mock_logger_instance = mock_logger.return_value
        mock_toml_load.return_value = {"key": "value"}

        # テスト対象のクラスのインスタンスを作成
        client = Client()

        # ファイルパスの設定
        filepath = "config.toml"

        # ファイルオープンのモック
        with patch("builtins.open", mock_open(read_data="data")):
            client.read_config(filepath)

        # toml.loadが正しく呼び出されたか確認
        mock_toml_load.assert_called_once()

        # ログの出力が正しいか確認
        mock_logger_instance.logger.info.assert_called_with(f"reading complete:{filepath}")

        # configが正しく設定されたか確認
        assert client.config == {"key": "value"}

    @patch("python_prj_template.opensearch.client.Logger")  # Loggerをモック
    @patch("python_prj_template.opensearch.client.OpenSearch")  # OpenSearchをモック
    def test_create_client_success(self, mock_opensearch, mock_logger):
        # モックのセットアップ
        mock_logger_instance = mock_logger.return_value
        mock_client = MagicMock()
        mock_client.info.return_value = {"status": "ok"}
        mock_opensearch.return_value = mock_client

        # テスト対象のクラスのインスタンスを作成
        client = Client()
        client.config = {
            "opensearch": {
                "host": "localhost",
                "port": 9200,
                "user": "admin",
                "password": "admin",
                "use_ssl": True,
                "verify_certs": True,
                "ssl_show_warn": False,
            }
        }

        # メソッドを呼び出す
        client.create_client()

        # OpenSearchが正しく呼び出されたか確認
        mock_opensearch.assert_called_with(
            hosts=[{"host": "localhost", "port": 9200}],
            http_auth=("admin", "admin"),
            use_ssl=True,
            verify_certs=True,
            ssl_show_warn=False,
        )

        # ログの出力が正しいか確認
        mock_logger_instance.logger.info.assert_any_call({"status": "ok"})
        mock_logger_instance.logger.info.assert_any_call("connect success")

        # clientが設定されているか確認
        assert client.client == mock_client

    @patch("python_prj_template.opensearch.client.Logger")  # Loggerをモック
    @patch("python_prj_template.opensearch.client.OpenSearch")  # OpenSearchをモック
    def test_create_client_failure(self, mock_opensearch, mock_logger):
        
        # テスト対象のクラスのインスタンスを作成
        client = Client()
        client.config = {
            "opensearch": {
                "host": "localhost",
                "port": 9200,
                "user": "admin",
                "password": "admin",
                "use_ssl": True,
                "verify_certs": True,
                "ssl_show_warn": False,
            }
        }
        # モックのセットアップ
        mock_opensearch.side_effect = Exception("Connection failed")

        # sys.exit(1)のモック
        with patch('sys.exit') as mock_exit:
            # メソッドを呼び出す
            client.create_client()

            # sys.exit(1)が呼び出されているか確認
            mock_exit.assert_called_once_with(1)
