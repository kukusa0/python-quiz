import requests
import json
import sqlite3

url = "http://api.mediastack.com/v1/news?access_key=c3ef337e8ed8e4ed1c5c5086480ef2ed"
r = requests.get(url)
result = r.json()

data = result["data"]

#

file = open("news.json", "w", encoding="utf-8_sig")
file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

#

conn = sqlite3.connect("news.sqlite")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS news
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                author VARCHAR (100),
                title VARCHAR (200),
                description VARCHAR (500),
                image VARCHAR (500),
                language VARCHAR (100),
                country VARCHAR (100)''')

#

db_data = []

for i in data:
    info = {
        "author": i["data"],
        "title": i["title"],
        "description": i["description"],
        "image": i["image"],
        "language": i["language"],
        "country": i["country"]
    }

query = "INSERT INTO news (author, title, description, image, language, country) VALUES (?, ?, ?, ?, ?, ?)"
cursor.executemany(query, db_data)
conn.commit()

conn.close()
