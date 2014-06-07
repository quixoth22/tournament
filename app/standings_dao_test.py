import sqlite3

import pytest

import tournament_dao
import player_dao
import match_dao
import standings_dao
import config
from models import Tournament, Player, Match


class FakeG(object):
    def __init__(self):
        self.db = sqlite3.connect(config.TEST_DATABASE)
        script = open(config.SCHEMA).read()
        self.db.executescript(script)
        self.db.execute('pragma foreign_keys = ON')


@pytest.fixture
def g():
    fake_g = FakeG()
    standings_dao.g = fake_g
    match_dao.g = fake_g
    player_dao.g = fake_g
    tournament_dao.g = fake_g


def test_standings(g):
    p = Player("test player")
    p2 = Player("test player 2")
    p3 = Player("test player 3")
    player_dao.create(p)
    p.player_id = 1
    player_dao.create(p2)
    p2.player_id = 2
    player_dao.create(p3)
    p3.player_id = 3
    t = Tournament(0, '', 'T1', 'type', 0)
    tournament_dao.create(t)
    t.tournament_id = 1
    match_dao.create([p.player_id, p2.player_id], t.tournament_id)
    match_dao.create([p.player_id, p3.player_id], t.tournament_id)
    match_dao.create([p3.player_id, p2.player_id], t.tournament_id)
    match = Match(player1=p, player2=p2, match_id=1)
    match.score1 = 19
    match.score2 = 21
    match2 = Match(player1=p, player2=p3, match_id=2)
    match2.score1 = 17
    match2.score2 = 21
    match3 = Match(player1=p3, player2=p2, match_id=3)
    match3.score1 = 23
    match3.score2 = 21

    match_dao.update(match)
    match_dao.update(match2)
    match_dao.update(match3)
    standings = standings_dao.find(t.tournament_id)

    assert standings[0].name == p.fname
    assert standings[0].win == 0
    assert standings[0].loss == 2
    assert standings[1].name == p2.fname
    assert standings[1].win == 1
    assert standings[1].loss == 1
    assert standings[2].name == p3.fname
    assert standings[2].win == 2
    assert standings[2].loss == 0


def test_standings_with_ties(g):
    p = Player("test player")
    p2 = Player("test player 2")
    p3 = Player("test player 3")
    player_dao.create(p)
    p.player_id = 1
    player_dao.create(p2)
    p2.player_id = 2
    player_dao.create(p3)
    p3.player_id = 3
    t = Tournament(0, '', 'T1', 'type', 0)
    tournament_dao.create(t)
    t.tournament_id = 1
    match_dao.create([p.player_id, p2.player_id], t.tournament_id)
    match_dao.create([p.player_id, p3.player_id], t.tournament_id)
    match_dao.create([p3.player_id, p2.player_id], t.tournament_id)
    match = Match(player1=p, player2=p2, match_id=1)
    match.score1 = 19
    match.score2 = 21
    match2 = Match(player1=p, player2=p3, match_id=2)
    match2.score1 = 17
    match2.score2 = 17

    match_dao.update(match)
    match_dao.update(match2)
    standings = standings_dao.find(t.tournament_id)

    assert standings[0].name == p.fname
    assert standings[0].win == 0
    assert standings[0].loss == 1
    assert standings[0].tie == 1
    assert standings[1].name == p2.fname
    assert standings[1].win == 1
    assert standings[1].loss == 0
    assert standings[1].tie == 0
    assert standings[2].name == p3.fname
    assert standings[2].win == 0
    assert standings[2].loss == 0
    assert standings[2].tie == 1


def test_standings_with_games_not_played(g):
    p = Player("test player")
    p2 = Player("test player 2")
    p3 = Player("test player 3")
    player_dao.create(p)
    p.player_id = 1
    player_dao.create(p2)
    p2.player_id = 2
    player_dao.create(p3)
    p3.player_id = 3
    t = Tournament(0, '', 'T1', 'type', 0)
    tournament_dao.create(t)
    t.tournament_id = 1
    match_dao.create([p.player_id, p2.player_id], t.tournament_id)
    match_dao.create([p.player_id, p3.player_id], t.tournament_id)
    match_dao.create([p3.player_id, p2.player_id], t.tournament_id)

    standings = standings_dao.find(t.tournament_id)

    assert standings[0].win == 0
    assert standings[0].loss == 0
    assert standings[0].tie == 0
    assert standings[1].win == 0
    assert standings[1].loss == 0
    assert standings[1].tie == 0
    assert standings[2].win == 0
    assert standings[2].loss == 0
    assert standings[2].tie == 0
