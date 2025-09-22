import json
import os
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
import post_storage
from backend.post_storage import fetch_post_by_id

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = post_storage.get_posts()
    if not posts:
        return jsonify({ "error" : "database not found."})
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
def add_post():
    # Get new post data
    new_post = request.get_json()

    # return error if new_post invalid
    if not new_post:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    # add new data to database (json file)
    title = new_post.get("title")
    content = new_post.get("content")
    post_storage.add_post(title, content)
    posts = post_storage.get_posts()
    return jsonify(posts)


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = post_storage.fetch_post_by_id(post_id)

    if post_storage.delete_post(post_id):
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})
    else:
        return jsonify({"error": f"Post with id {post_id} not found."})




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
