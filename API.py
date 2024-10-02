from flask import Flask
from flask_cors import CORS

from GET.get_clients import get_clients_blueprint
from GET.get_event_types import get_event_types_blueprint
from GET.get_events import get_events_blueprint
from GET.get_learnings import get_learnings_blueprint
from GET.get_news import get_news_blueprint
from GET.get_resume import get_resume_blueprint

from POST.post_event import post_event_blueprint
from POST.post_news import post_news_blueprint

app = Flask(__name__)

CORS(app)

app.register_blueprint(get_news_blueprint)
app.register_blueprint(get_resume_blueprint)
app.register_blueprint(get_clients_blueprint)
app.register_blueprint(get_learnings_blueprint)
app.register_blueprint(get_event_types_blueprint)
app.register_blueprint(get_events_blueprint)

app.register_blueprint(post_news_blueprint)
app.register_blueprint(post_event_blueprint)

if __name__ == '__main__':
    app.run(port=2345)
