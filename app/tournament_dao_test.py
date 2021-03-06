import pytest
import sqlite3

import tournament_dao
import config
from models import Tournament

class FakeG(object):
    def __init__(self):
        self.db = sqlite3.connect(config.TEST_DATABASE)
        script = open(config.SCHEMA).read()
        self.db.executescript(script)
        self.db.execute('pragma foreign_keys = ON')

@pytest.fixture
def g():
    fG = FakeG()
    tournament_dao.g = fG

def test_create_tournament(g):
    t = Tournament(0,description='test-tourn')

    created_t = tournament_dao.create(t)

    assert t.description == created_t.description
    assert created_t.start_date != None
    assert created_t.id == 1

def test_create_and_find_tournament(g):
    t = Tournament(0,description='test-tourn')

    tournament_dao.create(t)
    retreived_t = tournament_dao.find(1)

    assert retreived_t.description == t.description

def test_create_and_delete_tournament(g):
    t = Tournament(0,description='test-tourn')
    tournament_dao.create(t)
    retreived_t = tournament_dao.find(1)
    id = retreived_t.id

    tournament_dao.delete(id)
    all_tournaments = tournament_dao.find_all()

    assert all_tournaments == []

def test_begin_tournament(g):
    t = Tournament(0,description='test-tourn')
    t = tournament_dao.create(t)

    tournament_dao.update_status(t.id, 1)
    retreived_t = tournament_dao.find_all_by_status(1)

    assert retreived_t[0].description == t.description
    assert retreived_t[0].status == 1

def test_find_all_new_tournaments(g):
    t = Tournament(0,description='test-tourn')
    t2 = Tournament(0,description='test-tourn-2')
    tournament_dao.create(t)
    tournament_dao.create(t2)

    tourns = tournament_dao.find_all_by_status(0)

    assert len(tourns) == 2
    assert tourns[0].description == t.description
    assert tourns[1].description == t2.description


def test_complete_tournament(g):
    t = Tournament(0,description='test-tourn')
    t = tournament_dao.create(t)

    tournament_dao.update_status(t.id, 2)
    retreived_t = tournament_dao.find_all_by_status(2)

    assert retreived_t[0].description == t.description
    assert retreived_t[0].status == 2
