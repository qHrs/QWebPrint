import os

# host configuration
DEBUG = True
PORT = 8080
HOST = "127.0.0.1"
ENV = 'development'
SECRET_KEY = "QWebPrint"

# upload
UPLOAD_FOLDER = os.path.curdir + os.path.sep + 'uploads' + os.path.sep
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])