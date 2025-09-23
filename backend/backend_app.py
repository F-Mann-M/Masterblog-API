import json
import os
from flask import Flask, jsonify, request, url_for, render_template
from flask_cors import CORS


import post_storage
from backend.post_storage import fetch_post_by_id

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """ Gets all posts form json and returns as json object"""
    posts = post_storage.get_posts()
    if not posts:
        return jsonify({ "error" : "database not found."})
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
def add_post():
    """
    Takes in a POST request with title and content
    adds new post to database
    """

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
    """ Takes in post id and deletes post form json"""
    if post_storage.delete_post(post_id):
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})
    else:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    """
    Takes in post ID and gets json object (title, content).
    Updates post with post_id in database
    and returns updated database as json object
    """
    # Get Data
    updated_post = request.get_json()

    # return error if json object invalid
    if not updated_post:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    title = updated_post.get("title")
    content = updated_post.get("content")

    # Update database
    post_storage.update_post(title, content, post_id)
    if not post_storage.fetch_post_by_id(post_id):
        return jsonify( {"error": f"Post with ID {post_id} not found"})

    posts = post_storage.get_posts()
    return jsonify(posts)

@app.route("/api/posts/search", methods=["GET"])
def search_post():
    """Takes in search query (title, content). Goes through post title and content and returns search results"""
    title = request.args.get("title")
    content = request.args.get("content")

    posts = post_storage.get_posts()

    search_results = []

    for post in posts:
        if title and title.lower() in post["title"].lower():
            search_results.append(post)
        if content and content.lower() in post["content"].lower():
            search_results.append(post)
    if search_results:
        return jsonify(search_results)
    else:
        return jsonify({"message" : "nothing found :("})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)


