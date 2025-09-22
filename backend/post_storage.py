import json
import os


def load_file(file_path):
    """loads json and returns as list of dicts. If there is no json yet of file is empty return empty list"""
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist")
        return []

    with open(file_path, "r") as handel:
        try:
            posts = json.load(handel)
            if not isinstance(posts, list):
                print("Data have to be a list of dictionaries")
            return posts
        except TypeError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError:
            print(f"Error: Can not decode {file_path}")
            return []

def get_posts():
    """loads jason and returns list of dicts of the posts"""
    posts = load_file("data/post_data.json")
    if not posts:
        print("Database empty.")
        posts = []
    return posts


def get_new_post_id():
    """ Goes through all dicts of a list and looks for the highest id. Returns new id."""
    posts = get_posts()
    if posts:
        return max(post["id"] for post in posts) + 1
    else:
        return 1  # if no posts yet return id 1


def add_post(title, content):
    """load json, add new post along with author, title, content"""
    post_id = get_new_post_id()
    posts = get_posts()
    new_post_dict = {"id": post_id, "title": title, "content": content}
    posts.append(new_post_dict)
    write_file(posts)


def delete_post(post_id):
    """ takes in post id and deletes dictionary with this id"""
    posts = get_posts()
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
    write_file(posts)


def fetch_post_by_id(post_id):
    """ takes in an id and returns associated dictionary (post)."""
    posts = get_posts()
    for post in posts:
        if post["id"] == post_id:
            return post


def update_post(title, content, post_id):
    """ takes in author, title, content and id and updates post with id"""
    posts = get_posts()
    for post in posts:
        if post["id"] == post_id:
            post["title"] = title
            post["content"] = content

    write_file(posts)



def write_file(file):
    with open("data/post_data.json", "w", encoding='utf-8') as handel:
        json.dump(file, handel, ensure_ascii=False, indent=4)