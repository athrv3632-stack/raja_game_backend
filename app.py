from flask import Flask, request, jsonify
from uuid import uuid4
import random, json, os

app = Flask(__name__)

STORAGE_FILE = "storage.json"
DEFAULT_POINTS = {"Raja": 1000, "Mantri": 800, "Sipahi": 500, "Chor": 0}

if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as f:
        try:
            rooms = json.load(f)
        except:
            rooms = {}
else:
    rooms = {}

def save():
    with open(STORAGE_FILE, "w") as f:
        json.dump(rooms, f, indent=2)

def new_player(name):
    return {"id": str(uuid4())[:8], "name": name, "role": None, "points": 0}

@app.route("/room/create", methods=["POST"])
def create_room():
    data = request.get_json() or {}
    name = data.get("name", "player")
    room_id = str(uuid4())[:8]
    p = new_player(name)
    p["points"] = 0
    rooms[room_id] = {
        "id": room_id,
        "players": [p],
        "assigned": False,
        "rounds": [],
        "default_points": DEFAULT_POINTS
    }
    save()
    return jsonify({"room_id": room_id, "player": p}), 201

@app.route("/room/join", methods=["POST"])
def join_room():
    data = request.get_json() or {}
    room_id = data.get("room_id")
    name = data.get("name", "player")
    if not room_id or room_id not in rooms:
        return jsonify({"error": "room not found"}), 404
    r = rooms[room_id]
    if len(r["players"]) >= 4:
        return jsonify({"error": "room full"}), 400
    p = new_player(name)
    p["points"] = 0
    r["players"].append(p)
    save()
    return jsonify({"room_id": room_id, "player": p}), 201

@app.route("/room/players/<room_id>", methods=["GET"])
def list_players(room_id):
    r = rooms.get(room_id)
    if not r:
        return jsonify({"error": "room not found"}), 404
    players = [{"id": p["id"], "name": p["name"]} for p in r["players"]]
    return jsonify({"players": players})

@app.route("/room/assign/<room_id>", methods=["POST"])
def assign_roles(room_id):
    r = rooms.get(room_id)
    if not r:
        return jsonify({"error": "room not found"}), 404
    if r["assigned"]:
        return jsonify({"message": "already assigned"}), 200
    if len(r["players"]) < 4:
        return jsonify({"error": "need 4 players to assign roles"}), 400
    roles = ["Raja", "Mantri", "Sipahi", "Chor"]
    random.shuffle(roles)
    for p, role in zip(r["players"], roles):
        p["role"] = role
        p["points"] = r["default_points"][role]
    r["assigned"] = True
    save()
    return jsonify({"message": "roles assigned"}), 200

@app.route("/role/me/<room_id>/<player_id>", methods=["GET"])
def my_role(room_id, player_id):
    r = rooms.get(room_id)
    if not r:
        return jsonify({"error": "room not found"}), 404
    for p in r["players"]:
        if p["id"] == player_id:
            return jsonify({"id": p["id"], "name": p["name"], "role": p["role"], "points": p["points"]})
    return jsonify({"error": "player not found"}), 404

@app.route("/guess/<room_id>", methods=["POST"])
def submit_guess(room_id):
    data = request.get_json() or {}
    player_id = data.get("player_id")
    guessed_id = data.get("guessed_id")
    r = rooms.get(room_id)
    if not r:
        return jsonify({"error": "room not found"}), 404
    guesser = next((p for p in r["players"] if p["id"] == player_id), None)
    if not guesser:
        return jsonify({"error": "player not found"}), 404
    if guesser["role"] != "Mantri":
        return jsonify({"error": "only Mantri can submit guess"}), 403
    chor = next((p for p in r["players"] if p["role"] == "Chor"), None)
    if not chor:
        return jsonify({"error": "chor missing"}), 400
    correct = (chor["id"] == guessed_id)
    mantri = guesser
    sipahi = next((p for p in r["players"] if p["role"] == "Sipahi"), None)
    if correct:
        mantri["points"] += 50
        if sipahi:
            sipahi["points"] += 50
        chor["points"] -= 100
        result = "correct"
    else:
        chor["points"] += 150
        result = "wrong"
    r["rounds"].append({
        "guesser": mantri["id"],
        "guessed": guessed_id,
        "correct": correct
    })
    save()
    return jsonify({"result": result, "correct_chor_id": chor["id"]}), 200

@app.route("/result/<room_id>", methods=["GET"])
def result(room_id):
    r = rooms.get(room_id)
    if not r:
        return jsonify({"error": "room not found"}), 404
    out = [{"id": p["id"], "name": p["name"], "role": p["role"], "points": p["points"]} for p in r["players"]]
    return jsonify({"players": out, "rounds": r["rounds"]})

@app.route("/leaderboard/<room_id>", methods=["GET"])
def leaderboard(room_id):
    r = rooms.get(room_id)
    if not r:
        return jsonify({"error": "room not found"}), 404
    board = sorted([{"name": p["name"], "points": p["points"]} for p in r["players"]], key=lambda x: -x["points"])
    return jsonify({"leaderboard": board})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

