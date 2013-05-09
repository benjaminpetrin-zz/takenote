#!/usr/bin/env python

"""

    This script launches todays notes in the editor. If today's note file has
    not yet been created, it starts by copying yesterday's (or most recent) notes.
    Notes are stored in a configurable directory with a configurable name format.

    TODO
        Allow jumping into yesterday's note with an arg, or the notes directory
        Warn if can't find previous note file

"""

import os
import shutil
from subprocess import call
import datetime

# Configuration
note_dir = "/Users/bpetrin/Documents/work_logs/"
note_name_format = "%Y-%m-%d.txt"

def noteFileNameForDate(date):
    """
        Return the filename for a note for a given date Regardless of whether this file
        actually exists on disk
    """
    return date.strftime(note_name_format)

def openNoteFile(note_file_name):
    """ Launches the note file in the user's editor """
    editor = os.environ.get('EDITOR','vim')
    call([editor, note_file_name])

def noteFileNameForDayIfExists(date):
    """ Returns the note file for this date, else None """
    potential_file_name = noteFileNameForDate(date)
    try:
        with open(potential_file_name): pass
    except IOError:
        potential_file_name = None

    return potential_file_name

def createNoteFileForDay(date):
    """
        Creates and returns a new note file for this day stating with the contents of
        the most recent note file
    """
    new_file_name = noteFileNameForDate(date)

    # we need to locate the last note file that was written. This may be
    # yesterday or it may be some time ago (due to weekend or vacation)

    day_delta = datetime.timedelta(days = 1)
    last_note_file_name = None
    max_tries = 30
    try_count = 0

    while try_count < max_tries and last_note_file_name is None:
        try_count = try_count + 1
        date = date - day_delta
        last_note_file_name = noteFileNameForDayIfExists(date)

    if last_note_file_name is not None:
        # copy the last note contents to this one
        shutil.copy(last_note_file_name, new_file_name)

    return new_file_name

def main():
    os.chdir(note_dir)
    today = datetime.date.today()

    note_file_name = noteFileNameForDayIfExists(today)
    if note_file_name is None:
        note_file_name = createNoteFileForDay(today)

    openNoteFile(note_file_name)

if __name__ == "__main__":
    main()
