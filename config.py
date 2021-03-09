import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-well-never-thing-that'
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REMEMBER_COOKIE_DURATION = timedelta(hours=4)

    ENTRY_PER_PAGE = 100

    # set optional bootswatch theme
    #FLASK_ADMIN_SWATCH = 'cerulean'

    #config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    #pdfkit.from_url('http://127.0.0.1:5000/leave_worker_pdf', 'output.pdf', configuration=config)
