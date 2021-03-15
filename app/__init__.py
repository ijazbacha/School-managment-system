from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'admin_login'
ckeditor = CKEditor(app)




#config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltox\\bin\\wkhtmltopdf.exe')
#pdfkit.from_url('http://127.0.0.1:5000/leave_worker_pdf', 'output.pdf', configuration=config)

from app import routes, models