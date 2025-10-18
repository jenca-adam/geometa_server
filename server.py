from flask import Flask, request, abort, Response
import gt_api
from gt_api.errors import GeotasticAPIError
import random
DROP = {'id': 7726457, 'owner': 1573548, 'style': 'streetview', 'lat': 48.4403605385592, 'lng': 19.796818194444, 'mapId': 14155, 'challengeId': 0, 'groupId': 0, 'code': 'sk', 'subCode': 'sk-bc', 'wikiId': 0, 'panoId': 'QsvGtGRPk1h_xzMrW1kJIw', 'heading': 0, 'pitch': 0, 'zoom': 0, 'disallowTrekker': -1, 'imageUrl': None, 'copyright': None, 'hint': None, 'photosphereData': None, 'hideCompass': False, 'isLandmarkTip': False, 'sorting': 28, 'radius': 0, 'type': 'single'} # for now
app = flask.Flask(__name__)

@app.route("/fetch_drop", methods = ["GET"])
def fetch_drop(url):
    if "token" not in request.args:
        return {"status":"error", "message":"no token", "data":{}}, 401
    try:
        gt_api.user.get_user_info(request.args['token']) 
    except GeotasticAPIError as e:
        return {"status":"error", "message":"invalid token", "data":{}}, 403
    return {"status":"ok", "message":"", "data":{"drop":DROP}}
