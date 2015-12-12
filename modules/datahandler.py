#!/usr/bin/env python
# coding: utf-8

# pyfootballmngr

# Copyright (C) <2012-2015> Markus Hackspacher

# This file is part of pyfootballmngr.

# pyfootballmngr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyfootballmngr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyfootballmngr.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import datetime
import itertools


class Datahandler(object):
    """
    data management
    """
    def __init__(self, path):
        """class init

        @type path: string
        @return: none
        """
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """create tables with a id"""
        c = self.connection.cursor()
        c.execute(
            "create table if not exists users "
            "(id INTEGER PRIMARY KEY, name text, "
            "reg timestamp, last timestamp)")
        c.execute(
            "create table if not exists matches "
            "(id INTEGER PRIMARY KEY, pid1 integer, pid2 integer, team1 text, "
            "team2 text, goals1 integer, goals2 integer, date timestamp)")
        self.connection.commit()
        c.close()

    def insert_user(self, name):
        """Save the name in database

        :param name:
        :return:
        """
        try:
            name_utf8 = unicode(name)
        except:
            name_utf8 = name
        c = self.connection.cursor()
        c.execute("insert into users values (NULL, ?, ?, ?)", (name_utf8,
                  datetime.datetime.now().strftime("%d.%m.20%y"), None))
        self.connection.commit()
        c.close()

    def update_user(self, id, name, last=None):
        """Update user in the database

        :param id:
        :param name:
        :param last:
        :return:
        """
        c = self.connection.cursor()
        if last:
            c.execute("update users set name=?, last=? where id=?", (
                      name, last, id, ))
        else:
            c.execute("update users set name=? where id=?", (name, id, ))
        self.connection.commit()
        c.close()

    def delete_user(self, id):
        """Delete user in the database

        :param id:
        :return:
        """
        c = self.connection.cursor()
        c.execute("delete from users where id=?", (id, ))
        c.execute("delete from matches where pid1=? or pid2=?", (id, id, ))
        self.connection.commit()
        c.close()

    def get_users(self, id=None):
        """get user from the database

        :param id:
        :return:
        """
        c = self.connection.cursor()
        if id:
            c.execute("select name from users where id=?", (id, ))
        else:
            c.execute("select * from users")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def get_user_names(self):
        """get user names from the database

        :return:
        """
        c = self.connection.cursor()
        c.execute("select name from users")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def insert_match(self, id1, id2, team1, team2, goals1, goals2, date):
        """ insert match in the database

        :param id1:
        :param id2:
        :param team1:
        :param team2:
        :param goals1:
        :param goals2:
        :param date:
        :return:
        """
        try:
            team1_utf8 = unicode(team1)
        except:
            team1_utf8 = team1
        try:
            team2_utf8 = unicode(team2)
        except:
            team2_utf8 = team2
        c = self.connection.cursor()
        c.execute(
            "insert into matches values(NULL, ?, ?, ?, ?, ?, ?, ?)",
            (id1, id2, team1_utf8, team2_utf8, goals1, goals2, date))
        self.connection.commit()
        c.close()

    def update_match(self, id, id1, id2, team1, team2, goals1, goals2, date):
        """update match in the database

        :param id:
        :param id1:
        :param id2:
        :param team1:
        :param team2:
        :param goals1:
        :param goals2:
        :param date:
        :return:
        """
        c = self.connection.cursor()
        c.execute(
            "update matches set pid1=?, pid2=?, team1=?, team2=?, "
            "goals1=?, goals2=?, date=? where id=?",
            (id1, id2, team1, team2, goals1, goals2, date, id))
        self.connection.commit()
        c.close()

    def delete_match(self, id):
        """delete match in the database

        :param id:
        :return:
        """
        c = self.connection.cursor()
        c.execute("delete from matches where id=?", (id,))
        self.connection.commit()
        c.close()

    def get_matches(self, id=None):
        """get match from the database

        :param id:
        :return:
        """
        c = self.connection.cursor()
        if id:
            c.execute("select * from matches where pid1=? or pid2=?", (id, id))
        else:
            c.execute("select * from matches")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def get_diff(self, id):
        """get difference from the database

        :param id:
        :return:
        """
        c = self.connection.cursor()

        c.execute("select goals1, goals2 from matches where pid1=?", (id,))
        self.connection.commit()
        first = c.fetchall()

        c.execute("select goals1, goals2 from matches where pid2=?", (id,))
        self.connection.commit()
        sec = c.fetchall()
        c.close()

        pos = sum([a for a, b in first]) + sum([b for a, b in sec])
        neg = sum([b for a, b in first]) + sum([a for a, b in sec])

        return pos - neg

    def get_fav_team(self, id):
        """get favorite team from the database

        :param id:
        :return:
        """
        c = self.connection.cursor()
        c.execute("select team1 from matches where pid1=?", (id,))
        self.connection.commit()
        first = c.fetchall()

        c.execute("select team2 from matches where pid2=?", (id,))
        self.connection.commit()
        sec = c.fetchall()
        c.close()

        team_count = {}

        for t1, t2 in itertools.izip_longest(first, sec):
            team_count[t1] = team_count.get(t1, 0) + 1
            team_count[t2] = team_count.get(t2, 0) + 1

        team_count.pop(None)
        m = max(team_count.values())

        for k, v in team_count.items():
            if v == m:
                return k[0]

    def get_teams(self):
        """get teams from the database

        :return:
        """
        c = self.connection.cursor()
        c.execute("select team1, team2 from matches")
        self.connection.commit()
        data = c.fetchall()

        teams = []

        for t1, t2 in data:
            if t1 not in teams:
                teams.append(t1)
            if t2 not in teams:
                teams.append(t2)
        return sorted(teams)

    def close(self):
        """close connection of database"""
        self.connection.close()
