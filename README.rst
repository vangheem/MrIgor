Sublime Text 3 plugin for mr.igor
=================================

MrIgor is a Sublime Text 3 plugin for mr.igor.

mr.igor is an extension to pyflakes (a static code analysis tool for Python),
that will learn where you import things from, and then automatically fill in missing imports from the place they are most often imported.


Prerequisits
============

Install mr.igor on your system::

  $ pip install mr.igor


Installation
============

Using Package Control
---------------------

  * Open Sublime Text Command Pallete and type "install" with no quotes
  * Select "Install Package" from the dropdown box
  * Type "MrIgor" with no quotes, select it and press <ENTER>

Using git
---------

Go to your Sublime Text 3 packages directory and clone the repo::

  git clone https://github.com/tisto/MrIgor


Usage
=====

If you save a Python file in Sublime Text, "igor --reap" will be run to reap the contents of the file (adding the imports of that file to mr.igor's
database).

Use CMD+SHIFT+I to run the current file through mr.igor to add missing imports.


Credits
=======

This package is based on the Sublime Text 2 'SublimeTextIgorPlugin' by Martin
Aspeli.

https://github.com/optilude/SublimeTextIgorPlugin
