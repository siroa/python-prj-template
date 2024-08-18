from injector import Injector

from python_prj_template.driver.opensearch_driver import DataAccessModule
from python_prj_template.service.database_service import DatabaseService

if __name__ == "__main__":
    # 依存関係の登録
    injector = Injector(modules=[DataAccessModule()])
    # injector.getの引数に依存注入が必要なクラスを指定
    service = injector.get(DatabaseService)
    service.add_item()
    items = service.get_item()
    print(items)
