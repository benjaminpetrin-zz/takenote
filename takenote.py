#!/usr/bin/env python

"""

    This script launches todays notes in the editor. If today's note file has
    not yet been created, it starts by copying yesterday's (or most recent) notes.
    Notes are stored in a configurable directory with a configurable name format.

    TODO
        Warn if can't find previous note file

"""

import os
import shutil
from subprocess import call
import datetime
import argparse

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

def noteFileNameBeforeDate(date):
    """
        Returns filename and date for most recent notefile before the date passed in
    """

    day_delta = datetime.timedelta(days = 1)
    last_note_file_name = None
    max_tries = 30
    try_count = 0

    while try_count < max_tries and last_note_file_name is None:
        date = date - day_delta
        last_note_file_name = noteFileNameForDayIfExists(date)
        try_count = try_count + 1

    return (last_note_file_name, date)

def createNoteFileForDay(date):
    """
        Creates and returns a new note file for this day Stating with the contents of
        the most recent note file
    """
    new_file_name = noteFileNameForDate(date)
    old_file_name, _ = noteFileNameBeforeDate(date)

    if old_file_name is not None:
        shutil.copy(old_file_name, new_file_name)

    return new_file_name

def main():

    parser = argparse.ArgumentParser(description='Manage and edit notes')
    parser.add_argument('-n', dest='notes_to_skip', metavar='N', type=int, default=0, help='Edit the Nth youngest note, default is 0 (today).')
    args = parser.parse_args()

    os.chdir(note_dir)
    today = datetime.date.today()

    if args.notes_to_skip == 0:
        note_file_name = noteFileNameForDayIfExists(today)
        if note_file_name is None:
            note_file_name = createNoteFileForDay(today)
    else:
        note_file_name = None
        notes_to_skip = args.notes_to_skip
        date = today
        while notes_to_skip > 0:
            note_file_name, date = noteFileNameBeforeDate(date)
            notes_to_skip -= 1

    openNoteFile(note_file_name)

if __name__ == "__main__":
    main()
