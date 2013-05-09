takenote
========

Command line tool to automates creation and organization of my notes during
work day

Usage
-----

When executed takenote will launch the current editor (defined by environmental
variable EDITOR and defaulting to 'vim') with today's note file. If today's
note file is not found it will be created and populated with the contents of
the most recent date's note file before being launched in EDITOR.

The note file name format as well as the directory they are stored in can be
configured.
