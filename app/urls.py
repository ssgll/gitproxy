from app import indexBlueprint

from app.views.index import indexView, proxyView

indexBlueprint.add_url_rule('/', None, indexView, methods=["POST", "GET"])
indexBlueprint.add_url_rule('/<path:u>', None, proxyView, methods=["POST", "GET"])
