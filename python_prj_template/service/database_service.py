from injector import inject
from python_prj_template.driver.database import Database


# A class that implements business logic using a database
class DatabaseService:
    @inject
    def __init__(self, database: Database):
        self.database = database

    def get_item(self) -> str:
        return self.database.get("key1")

    def add_item(self):
        self.database.add("key1", "hoge")

    def update_item(self):
        self.database.update("key1", "aho")

    def delete_item(self):
        self.database.delete("key1")
