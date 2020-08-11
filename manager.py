from flask import Flask
# from config import config

from app.urls import indexBlueprint

def createApp():
	app = Flask(__name__)
	app.register_blueprint(indexBlueprint)

	return app

app = createApp()
