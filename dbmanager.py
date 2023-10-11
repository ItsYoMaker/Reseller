import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        urlname TEXT,
        url TEXT,
        sub INTEGER
    )
''')


def get_url(urlname):
    cursor.execute('SELECT url FROM data WHERE urlname = ?', (urlname,))

    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 'https://www.kufar.by/l/r~minsk'
def get_urlname(url):
    cursor.execute('SELECT urlname FROM data WHERE url = ?', (url,))

    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 'неизвестно'
def add_url(urlname, url):
    cursor.execute('INSERT INTO data (urlname, url) VALUES (?, ?)',
                   (urlname, url))
    conn.commit()
def delete_url(urlname):
    cursor.execute('DELETE FROM data WHERE urlname = ?',(urlname,))
    conn.commit()
def set_sub(sub):
    cursor.execute('UPDATE data SET sub = ?', (sub))
    conn.commit()

def get_list_of_urls():
    try:

        cursor.execute(f"SELECT url FROM data")

        column_values = [row[0] for row in cursor.fetchall()]

        return column_values

    except sqlite3.Error as e:
        print("Ошибка SQLite:", e)