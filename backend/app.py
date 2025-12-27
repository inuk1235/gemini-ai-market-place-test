from flask import Flask, jsonify, request

from scraper import search_marketplace

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def search() -> tuple:
    data = request.get_json(force=True)
    keyword = data["keyword"]
    location = data["location"]
    radius_km = data["radiusKm"]

    listings = search_marketplace(keyword, location, radius_km)
    # Placeholder: replace with last-seen diffing in a real datastore.
    new_listings = listings

    return jsonify({"newListings": new_listings}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
