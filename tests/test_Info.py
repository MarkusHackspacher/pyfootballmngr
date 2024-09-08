# -*- coding: utf-8 -*-

# pyfootballmngr

# Copyright (C) <2024> Markus Hackspacher

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

"""Test the dialog module LottoSimuDialog
"""

from unittest import TestCase

from modules.main import Main


class TestMain(TestCase):
    def setUp(self):
        """Creates the QApplication instance"""

        super(TestMain, self).setUp()
        self.app = Main('de')

    def tearDown(self):
        """Deletes the reference owned by self"""
        del self.app
        super(TestMain, self).tearDown()

    def test_onInfo(self):
        self.app.on_info(True)

    def test_on_example_data(self):
        self.app.on_example_data()
