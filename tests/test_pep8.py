# -*- coding: utf-8 -*-

# pyfootballmngr

# Copyright (C) <2015> Markus Hackspacher

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

import unittest
import pep8


class TestCodeFormat(unittest.TestCase):
    """
    Test of the code format
    """

    def test_pep8_conformance(self):
        """Test that code conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['pyfootballmngr.py',
                                        'tests/test_pep8.py',
                                        'modules/main.py',
                                        'modules/datahandler.py',
                                        'modules/gui/main_window.py',
                                        'modules/gui/dialogs/new_match.py',
                                        'modules/gui/dialogs/new_player.py',
                                        'modules/gui/dialogs/update_match.py',
                                        'modules/gui/dialogs/update_player.py',
                                        ])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
