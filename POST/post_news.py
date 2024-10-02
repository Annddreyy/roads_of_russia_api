from flask import Blueprint, jsonify, request
from db import get_connection

post_news_blueprint = Blueprint('post_news', __name__)

@post_news_blueprint.route('/api/v1/news', methods=['POST'])
def add_news():
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
        cur.commit()

        cur.close()
        conn.close()

        return jsonify({'message': 'News was been upload!'}), 200
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }