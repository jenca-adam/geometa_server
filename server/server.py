from flask import Flask, request, abort, Response, render_template
from werkzeug.utils import secure_filename
import gt_api
from gt_api.errors import GeotasticAPIError
import random
from . import database
from flask_cors import CORS
import uuid
import os

"""DROP = (
    {
        "id": 7726457,
        "owner": 1573548,
        "style": "streetview",
        "lat": 48.4403605385592,
        "lng": 19.796818194444,
        "mapId": 14155,
        "challengeId": 0,
        "groupId": 0,
        "code": "sk",
        "subCode": "sk-bc",
        "wikiId": 0,
        "panoId": "QsvGtGRPk1h_xzMrW1kJIw",
        "heading": 0,
        "pitch": 0,
        "zoom": 0,
        "disallowTrekker": -1,
        "imageUrl": None,
        "copyright": None,
        "hint": None,
        "photosphereData": None,
        "hideCompass": False,
        "isLandmarkTip": False,
        "sorting": 28,
        "radius": 0,
        "type": "single",
    },
)  # for now
DROP_INFO = {
    "title": "Hello, world!",
    "description": "if you see this, the server works",
    "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "image": "https://http.cat/418",
}"""
UPLOAD_DIR = "uploads"
app = Flask(__name__, static_folder="static")
app.config["UPLOAD_DIR"]=UPLOAD_DIR
CORS(app)
def is_admin(token, catch=True):
    try:
        return gt_api.user.get_user_info(token).get("communityId")==384
    except GeotasticAPIError:
        if not catch:
            raise
        return False
@app.route("/proxy/gt/<path:url>", methods=["GET", "POST"])
def gt_proxy(url):
    server = request.args.get("server", "api")
    token = request.args.get("token")
    enc = request.args.get("enc") == "true"
    if "params" in request.args:
        params = json.loads(base64.b64decode(request.args["params"]))
    else:
        params = {}
    url = f"https://{server}.geotastic.net/{url}"
    kwargs = {}
    if request.method == "POST":
        data = request.json
        if enc:
            data = {"enc": gt_api.generic.encode_encdata(data)}
        kwargs["json"] = data
    try:
        response = gt_api.generic.process_response(
            gt_api.generic.geotastic_api_request(
                url, request.method, token, params=params, **kwargs
            )
        )
    except GeotasticAPIError as e:
        return {"status": "error", "message": str(e), "response": None}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "failed to connect", "response": ""}, 503
    return {"status": "ok", "message": "", "response": response}
@app.route("/api/edit_meta", methods=["POST"])
def edit_meta():
    data = request.form
    if "token" not in data:
        return {"status":"error", "message":"No token"}
    if not is_admin(data["token"]):
        return {"status":"error", "message":"Invalid token"}
    meta = database.session.query(database.Meta).filter(database.Meta.id == int(data["id"])).first()
    if not meta:
        return {"status":"error", "message":"Invalid meta"}
    meta_data = meta.meta_data.copy()
    image = request.files.get("image")
    if image and image.filename:
        filename = secure_filename(image.filename)
        _, extension = os.path.splitext(filename)
        if extension.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            return {"status": "error", "message": "Invalid file type"}
        new_filename = os.path.join(app.config["UPLOAD_DIR"], str(uuid.uuid4())+extension)       
        image.save(new_filename)
        new_image = f"https://geometa.gtedit.tech/uploads/{new_filename}"
        meta_data["image"]=new_image
    meta_data["title"]=data.get("title", meta_data["title"])
    meta_data["description"]=data.get("desc", meta_data["description"])
    meta_data["link"]=data.get("link", meta_data["link"])
    meta.meta_data = meta_data
    database.session.commit()
    return {"status":"ok", "message":""}
@app.route("/api/fetch_drop", methods=["GET"])
def fetch_drop():
    """if "token" not in request.args:
        return {"status":"error", "message":"no token", "data":{}}, 401
    try:
        gt_api.user.get_user_info(request.args['token'])
    except GeotasticAPIError as e:
        return {"status":"error", "message":"invalid token", "data":{}}, 403"""
    drop = database.pick_random_drop()
    if drop is None:
        return {"status": "error", "message": "no drops in database", "data": {}}, 400

    return {"status": "ok", "message": "", "data": drop.to_json()}

@app.route("/api/user_status", methods=["GET"])
def user_status():
    token = request.args.get("token")
    if not token:
        return {"status":"error","message":"No token", "data":{"admin":False}}
    try:
        admin= is_admin(token, False)
    except GeotasticAPIError as e:
        return {"status":"error", "message":"Invalid token", "data":{"admin":False}}
    return {"status":"ok", "message":"", "data":{"admin":admin}} # restrict to mosquitoes for now

@app.route("/api/get_tags", methods=["GET"])
def get_tags():
    return [tag.name for tag in database.session.query(database.Tag).all()]
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", countries = database.session.query(database.Country).all(), tags = database.session.query(database.Tag).all(), metas = database.session.query(database.Meta).all())
@app.route("/login")
def login():
    return render_template("login.html")
def main():
    app.run(port=5000, debug=True)

if __name__=="__main__":
    main()
