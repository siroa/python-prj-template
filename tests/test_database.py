import pytest
from injector import Injector

from python_prj_template.driver.opensearch_driver import DataAccessModule
from python_prj_template.service.database_service import DatabaseService


# Pretreatment
@pytest.fixture
def setup():
    injector = Injector(modules=[DataAccessModule()])
    service = injector.get(DatabaseService)
    return service


def test_get_item(setup):
    service = setup
    service.add_item()
    item = service.get_item()
    assert item == "hoge"


def test_update_item(setup):
    service = setup
    service.add_item()
    service.update_item()
    item = service.get_item()
    assert item == "aho"


def test_delete_item(setup):
    service = setup
    service.add_item()
    service.delete_item()
    item = service.get_item()
    assert item is None
