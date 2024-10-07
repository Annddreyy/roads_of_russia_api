from flask import Blueprint, jsonify
from db import get_connection

get_news_blueprint = Blueprint('news', __name__)

@get_news_blueprint.route('/api/v1/news', methods=['GET'])
def get_news():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM news')

        news = cur.fetchall()

        news_json = []
        for one_news in news:
            author_id = one_news[4]
            cur.execute(f'SELECT surname, name, patronymic, photo '
                        f'FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            news_json.append(
                {
                    'id': one_news[0],
                    'title': one_news[1],
                    'description': one_news[2],
                    'date': str(one_news[3]),
                    'author': f'{author[0]}.{author[1][0]}.{author[2][0]}',
                    'photo': author[3],
                    'image_path': one_news[5]
                }
            )

        return jsonify(news_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()

@get_news_blueprint.route('/api/v1/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM news WHERE news_id={news_id}')

        news = cur.fetchone()

        if news:
            author_id = news[4]
            cur.execute(f'SELECT surname, name, patronymic '
                        f'FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            news_json = {
                'id': news[0],
                'title': news[1],
                'description': news[2],
                'date': str(news[3]),
                'author': f'{author[0]}.{author[1][0]}.{author[2][0]}',
                'image_path': news[5]
            }

            return jsonify(news_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {news_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()