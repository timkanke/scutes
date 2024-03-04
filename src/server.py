import os

from waitress import serve
from dotenv import load_dotenv

from scutes.wsgi import application


load_dotenv()  # take environment variables from .env

if __name__ == '__main__':
    serve(application, host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'))
