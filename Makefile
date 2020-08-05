tests.apkg: db.sqlite3
	python3 -m dgt_tests anki

db.sqlite3:
	python3 -m dgt_tests crawl
