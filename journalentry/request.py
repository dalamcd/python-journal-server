import sqlite3
import json
from model import JournalEntry

def get_all_entries():

	with sqlite3.connect("./dailyjournal.db") as conn:

		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			e.id,
			e.concept,
			e.entry,
			e.date,
			e.mood_id,
			m.label
		FROM journalentries e
		JOIN Mood m
			ON m.id = e.mood_id
		""")

		dataset = db_cursor.fetchall()

		entries = []

		for row in dataset:
			ent = JournalEntry(row["id"], row["concept"], row["entry"], row["date"], row["mood_id"])
			entries.append(ent.__dict__)
		
	return json.dumps(entries)

def get_single_entry(id):

	with sqlite3.connect("dailyjournal.db") as conn:
		
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			e.id,
			e.concept,
			e.entry,
			e.date,
			e.mood_id,
			m.label
		FROM journalentries e
		JOIN Mood m
			ON m.id = e.mood_id
		WHERE e.id = ?
		""", (id, ))

		data = db_cursor.fetchone()

		entry = JournalEntry(data["id"], data["concept"], data["entry"], data["date"], data["mood_id"])

	return json.dumps(entry.__dict__)

def delete_entry(id):
	with sqlite3.connect("./dailyjournal.db") as conn:

		db_cursor = conn.cursor()

		db_cursor.execute("""
			DELETE FROM journalentries
			WHERE id = ?
		""", (id, ))

def search_entries(value):
	with sqlite3.connect("./dailyjournal.db") as conn:

		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
			SELECT
				e.id,
				e.concept,
				e.entry,
				e.date,
				e.mood_id,
				m.label
			FROM journalentries e
			JOIN Mood m
				ON m.id = e.mood_id
			WHERE e.entry LIKE ?
		""", ("%" + value + "%", ))

		dataset = db_cursor.fetchall()

		entries = []

		for row in dataset:
			ent = JournalEntry(row["id"], row["concept"], row["entry"], row["date"], row["mood_id"])
			entries.append(ent.__dict__)
		
	return json.dumps(entries)

def create_entry(new_entry):
	with sqlite3.connect("./dailyjournal.db") as conn:

		db_cursor = conn.cursor()

		db_cursor.execute("""
		INSERT INTO journalentries
		VALUES (NULL, ?, ?, ?, ?)
		""", (new_entry["concept"], new_entry["entry"], new_entry["date"], new_entry["moodId"],))

		id = db_cursor.lastrowid

		new_entry['id'] = id

		return json.dumps(new_entry)

def update_entry(new_entry, id):
	with sqlite3.connect("./dailyjournal.db") as conn:

		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
			UPDATE journalentries
			SET
				concept = ?,
				entry = ?,
				date = ?,
				mood_id = ?
			WHERE id = ?
		""", (new_entry["concept"], new_entry["entry"], new_entry["date"], new_entry["moodId"], id,))

		if db_cursor.rowcount == 1:
			return True
		else:
			return False