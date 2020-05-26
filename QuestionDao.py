import sqlite3
from os import path

DB_FILE = "questions.db"

DEFAULT_DATA = """CREATE TABLE "questions" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"question"	TEXT NOT NULL,
	"answer"	TEXT NOT NULL,
	"difficulty"	INTEGER,
	"category"	TEXT,
	"question_number"	INTEGER NOT NULL
);"""

class QuestionDao:
    def __init__(self, db_file):
        reset = False
        if not path.exists(db_file):
            open(db_file, "w").close()
            reset = True

        self.db = sqlite3.connect(db_file)

        if reset:
            self.db.cursor().execute(DEFAULT_DATA).close()
            self.db.commit()

        self.close = self.db.close

    def add_item(self, question, answer, category, question_number, difficulty=None):
        c = self.db.cursor()
        c.execute("INSERT INTO questions VALUES (null, ?, ?, ?, ?, ?)", (question, answer, difficulty, category, question_number))
        c.close()
        self.db.commit()

    def read(self, query, *args):
        c = self.db.cursor()
        c.execute(query, args)

        out = list(c.fetchall())
        c.close()
        return out

    def get_all(self):
        return self.read("SELECT * FROM questions")

    def get_all_category(self, category):
        return self.read("SELECT * FROM questions WHERE category IS ?", category)

    def get_n_category(self, category, n):
        return self.read("SELECT * FROM questions WHERE category IS ? ORDER BY RANDOM()", category)[0:n]

    def get_item(self, id):
        return self.read("SELECT * FROM questions WHERE id IS ?", id)[0]

    def get_categories(self):
        return [x[0] for x in self.read("SELECT DISTINCT (category) from questions")]