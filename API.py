import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

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

@app.route('/api/v1/news', methods=['GET'])
def get_news():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM news')

        news = cur.fetchall()

        news_json = []
        for one_news in news:
            author_id = one_news[4]
            cur.execute(f'SELECT surname, name, patronymic, photo FROM client WHERE client_id={author_id}')
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

        cur.close()
        conn.close()

        return jsonify(news_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@app.route('/api/v1/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM news WHERE news_id={news_id}')

        news = cur.fetchone()

        if news:
            news_json = []

            author_id = news[4]
            cur.execute(f'SELECT surname, name, patronymic FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            news_json.append(
                {
                    'id': news[0],
                    'title': news[1],
                    'description': news[2],
                    'date': str(news[3]),
                    'author': f'{author[0]}.{author[1][0]}.{author[2][0]}',
                    'image_path': news[5]
                }
            )

            cur.close()
            conn.close()

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


@app.route('/api/v1/resume', methods=['GET'])
def get_resume():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM resume')

        resumes = cur.fetchall()

        resumes_json = []
        for resume in resumes:
            job_id = resume[5]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()

            resumes_json.append(
                {
                    'id': resume[0],
                    'author': f'{resume[1]} {resume[2][0]}. {resume[3][0]}.',
                    'file_path': resume[4].split('/')[-1],
                    'job_title': job[0]
                }
            )

        cur.close()
        conn.close()

        return jsonify(resumes_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }


@app.route('/api/v1/resume/<int:resume_id>', methods=['GET'])
def get_one_resume(resume_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM resume WHERE resume_id={resume_id}')

        resume = cur.fetchone()

        if resume:
            resume_json = []

            job_id = resume[5]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()

            resume_json.append(
                {
                    'id': resume[0],
                    'author': f'{resume[1]} {resume[2][0]}. {resume[3][0]}.',
                    'file_path': resume[4].split('/')[-1],
                    'job_title': job[0]
                }
            )

            cur.close()
            conn.close()

            return jsonify(resume_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {resume_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }


@app.route('/api/v1/clients', methods=['GET'])
def get_clients():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM client')

        clients = cur.fetchall()

        clients_json = []
        for client in clients:
            department_id = client[13]
            cur.execute(f'SELECT title FROM department WHERE department_id={department_id}')
            department = cur.fetchone()[0]

            job_id = client[14]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()[0]

            role_id = client[15]
            cur.execute(f'SELECT title FROM system_role WHERE system_role_id={role_id}')
            role = cur.fetchone()[0]

            clients_json.append(
                {
                    'id': client[0],
                    'FIO': f'{client[1]} {client[2][0]}. {client[3][0]}.',
                    'photo': client[6].split('/')[-1],
                    'adress': client[7],
                    'phone': client[8],
                    'email': client[9],
                    'birthday_date': str(client[10]),
                    'cabinet': client[11],
                    'dop_information': client[12],
                    'department': department,
                    'job': job,
                    'role': role
                }
            )

        cur.close()
        conn.close()

        return jsonify(clients_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@app.route('/api/v1/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM client WHERE client_id={client_id}')

        client = cur.fetchone()

        if client:
            client_json = []

            department_id = client[13]
            cur.execute(f'SELECT title FROM department WHERE department_id={department_id}')
            department = cur.fetchone()[0]

            job_id = client[14]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()[0]

            role_id = client[15]
            cur.execute(f'SELECT title FROM system_role WHERE system_role_id={role_id}')
            role = cur.fetchone()[0]

            client_json.append(
                {
                    'id': client[0],
                    'FIO': f'{client[1]} {client[2][0]}. {client[3][0]}.',
                    'photo': client[6].split('/')[-1],
                    'adress': client[7],
                    'phone': client[8],
                    'email': client[9],
                    'birthday_date': str(client[10]),
                    'cabinet': client[11],
                    'dop_information': client[12],
                    'department': department,
                    'job': job,
                    'role': role
                }
            )

            cur.close()
            conn.close()

            return jsonify(client_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {client_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@app.route('/api/v1/events', methods=['GET'])
@cross_origin()
def get_events():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM event')

        events = cur.fetchall()

        events_json = []
        for event in events:
            event_type_id = event[3]
            cur.execute(f'SELECT title FROM event_type WHERE event_type_id={event_type_id}')
            event_type = cur.fetchone()[0]

            author_id = event[4]
            cur.execute(f'SELECT surname, name, patronymic, photo '
                        f'FROM client WHERE client_id={author_id}')
            client = cur.fetchone()

            events_json.append(
                {
                    'id': event[0],
                    'title': event[1],
                    'description': event[2],
                    'event_type': event_type,
                    'author': f'{client[0]} {client[1][0]}. {client[2][0]}.',
                    'photo': client[3],
                    'image_path': event[5],
                    'date_start': str(event[6]),
                    'date_end': str(event[7])
                }
            )

        return jsonify(events_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }


@app.route('/api/v1/events/<int:event_id>', methods=['GET'])
def get_one_event(event_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM event WHERE event_id={event_id}')

        event = cur.fetchone()

        if event:
            event_json = []

            event_type_id = event[3]
            cur.execute(f'SELECT title FROM event_type WHERE event_type_id={event_type_id}')
            event_type = cur.fetchone()[0]

            author_id = event[4]
            cur.execute(f'SELECT surname, name, patronymic '
                        f'FROM client WHERE client_id={author_id}')
            client = cur.fetchone()

            event_json.append(
                {
                    'id': event[0],
                    'title': event[1],
                    'description': event[2],
                    'event_type': event_type,
                    'author': f'{client[0]} {client[1][0]}. {client[2][0]}.',
                    'image_path': event[5],
                    'date_start': str(event[6]),
                    'date_end': str(event[7])
                }
            )

            return jsonify(event_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {event_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }


@app.route('/api/v1/learnings', methods=['GET'])
def get_learnings():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT event_id, title, description, author_id, image_path, date_start, date_end '
                    'FROM event WHERE event_type_id=1')
        learnings = cur.fetchall()

        learnings_json = []
        for learning in learnings:
            author_id = learning[3]
            cur.execute(f'SELECT surname, name, patronymic FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            learnings_json.append(
                {
                    'id': learning[0],
                    'title': learning[1],
                    'description': learning[2],
                    'author': f'{author[0]} {author[1][0]}. {author[2][0]}.',
                    'image_path': learning[4],
                    'date_start': str(learning[5]),
                    'date_end': str(learning[6])
                }
            )

        return jsonify(learnings_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }


@app.route('/api/v1/learnings/<int:learning_id>')
def get_one_learning(learning_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT event_id, title, description, author_id, image_path, date_start, date_end '
                    f'FROM event WHERE event_type_id=1 AND event_id={learning_id}')

        learning = cur.fetchone()

        if learning:
            cur.execute(f'SELECT surname, name, patronymic FROM client WHERE client_id={learning[3]}')
            author = cur.fetchone()

            learning_json = [
                {
                    'id': learning[0],
                    'title': learning[1],
                    'description': learning[2],
                    'author': f'{author[0]} {author[1][0]}. {author[2][0]}',
                    'image_path': learning[4],
                    'date_start': str(learning[5]),
                    'date_end': str(learning[6])
                }
            ]

            return jsonify(learning_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {learning_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@app.route('/api/v1/news', methods=['POST'])
def add_news():
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

    return jsonify({'message': 'Новость успешно добавлена!'}), 200


if __name__ == '__main__':
    app.run(port=2345)
