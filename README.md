pyfootballmngr
==============

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/510d01cdfb734c9e96dd65912b38d130/badge.svg)](https://www.quantifiedcode.com/app/project/510d01cdfb734c9e96dd65912b38d130)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/62f5afb25e4e45bcb487c9fde7860b84)](https://www.codacy.com/app/MarkusHackspacher/pyfootballmngr?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MarkusHackspacher/pyfootballmngr&amp;utm_campaign=Badge_Grade)

An alternative to paper-pencil method for recording results.
The program is developed on [github.com/MarkusHackspacher/pyfootballmngr](https://github.com/MarkusHackspacher/pyfootballmngr).
Feedback and contributions are welcome.

Is a fork from (sourceforge.net/p/pyfootballmngr)[http://sourceforge.net/p/pyfootballmngr].

Install
-------

The program requires [Python 2.7 or 3.x](http://www.python.org/download/) 
and [Qt4 for Python](http://www.riverbankcomputing.com/software/pyqt/download)
or [Qt5 for Python](http://www.riverbankcomputing.com/software/pyqt/download5).

    
Then you copied the source code of the program on your computer,
either [download](https://github.com/MarkusHackspacher/pyfootballmngr) the zip file of the project or download with the version control system:

```
# git clone https://github.com/MarkusHackspacher/pyfootballmngr.git
cd pyfootballmngr
```

Start with:

```
python pyfootballmngr.py
```

![Image](misc/pyfootballmngr_en.png "pyfootballmngr screenshot.")

Translation
-----------

To translate the program or make a translation in your language,
insert in the complete.pro your language code.

```
cd modules
pylupdate5 complete.pro
```

translate your language file: pyfbm_xx.ts, and produce the .ts translation files to .qm with

```
lrelease complete.pro
```

fill free to add your language in complete.pro.

![Image](misc/pyfbm_updatematch_en.png "pyfootballmngr updatematch screenshot.")

license
-------

GNU GPLv3

![Image](misc/pyfootballmngr.png "pyfootballmngr Qt4 screenshot.")

