import pyodbc
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_connection():
    SERVER = 'localhost'
    DATABASE = 'roads_of_russia'
    USERNAME = 'sa'
    PASSWORD = '1234'
    connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                        f'SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
                        f'Trusted_Connection=yes')

    conn = pyodbc.connect(connectionString)

    return conn

@app.route('/news', methods=['GET'])
def get_news():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM news')

    news = cur.fetchall()

    news_json = []
    for one_news in news:
        author_id = one_news[4]
        cur.execute(f'SELECT surname, name, patronymic FROM client WHERE client_id={author_id}')
        author = cur.fetchone()

        news_json.append(
            {
                'id': one_news[0],
                'title': one_news[1],
                'description': one_news[2],
                'date': one_news[3],
                'author': f'{author[0]}.{author[1][0]}.{author[2][0]}'
            }
        )

    cur.close()
    conn.close()

    return jsonify(news_json)

if __name__ == '__main__':
    app.run(port=2345)
