#!/usr/bin/python3

from collections import defaultdict
from sqlite3 import connect
from typing import Any


def sql_execute(dbname: str) -> list[Any]:
    con = connect(f"file:{dbname}?mode=ro", uri=True)
    cur = con.cursor()
    cur.execute(
        """
select REPLACE(ContentID, 'file:///mnt/onboard/', ''),
    Annotation,
    Text
from Bookmark
where Text is not null
    OR Annotation is not null;
"""
    )
    return cur.fetchall()


def clean_name(name: str) -> str:
    """
    Drucker, Peter F_/Effective Executive, The - Peter F. Drucker.epub#(3)OEBPS/text/9780062574350_Introduction.xhtml#_idParaDest-5
    ->
    Effective Executive, The - Peter F. Drucker.epub
    """
    name = name.split("#")[0]
    return name.split("/")[1]


if __name__ == "__main__":
    DB_NAME = "KoboReader.sqlite"
    rows = [
        {"name": clean_name(i[0]), "note": i[1], "text": i[2]}
        for i in sql_execute(DB_NAME)
    ]
    notes = defaultdict(list)
    for row in rows:
        notes[row["name"]].append((row["note"], row["text"]))
    # format markdown
    print("# Kobo annotation export")
    for name in notes:
        print(f"\n## {name}\n")
        for note in notes[name]:
            if note[0]:
                print(f"**{note[0]}**\n")
            print(note[1])
            print()

