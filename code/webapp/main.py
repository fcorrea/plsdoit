from app import create_app
from app.database import db_session

app = create_app()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
