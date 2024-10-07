from webbrowser import Error

from flask import Blueprint, jsonify, request
from db import get_connection

post_news_blueprint = Blueprint('post_news', __name__)

@post_news_blueprint.route('/api/v1/news', methods=['POST'])
def add_news():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        news = request.get_json()

        title = news['title']
        description = news['description']
        date = news['date']
        author = news['author']
        image_path = news['image_path']

        cur.execute('INSERT INTO news(title, text, date, author_id, image_path) '
                        f"VALUES('{title}', '{description}', '{date}', {author}, '{image_path}')")

        conn.commit()

        return jsonify({'message': 'News was been upload!'})
    except Error as e:
        return {
            "status": "error",
            "code": e,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()