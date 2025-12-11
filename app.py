from src.main.server.server import create_app
from src.models.mysql.settings.mysql_model import db


app = create_app()

with app.app_context():
    db.create_all()

app.run(port=3000, debug=True, host='0.0.0.0')
