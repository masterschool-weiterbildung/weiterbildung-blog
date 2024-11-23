import json
from pathlib import WindowsPath

from constant_blog import RESULT, MESSAGE, PAYLOAD, ID, JSON_DATA_PATH, \
    CONTENT, AUTHOR, TITLE, LIKE

cached_data = None


def result_message(result: bool, message: str, payload) -> dict:
    return {RESULT: result, MESSAGE: message,
            PAYLOAD: payload}


def fetch_data(file_path: WindowsPath) -> result_message:
    global cached_data

    if cached_data is None:
        cached_data = load_data(file_path)
    return cached_data


def load_data(file_path: WindowsPath) -> result_message:
    payload = []
    try:
        if "json" in file_path.name:
            with open(file_path, "r") as handle:
                payload = json.load(handle)
    except FileNotFoundError as e:
        return (result_message
                (False,
                 f"Error: The file was not found. {e}", ""))
    except IOError:
        return (result_message
                (False,
                 "Error: Could not read the file.", ""))
    except Exception as e:
        return (result_message
                (False,
                 f"An unexpected error occurred: {e}",
                 ""))
    else:
        return (result_message
                (True, "File loaded successfully.",
                 payload))


def write_data(details: list[dict],
               file_path: WindowsPath) -> result_message:
    try:
        if "json" in file_path.name:
            with open(file_path, 'w') as handle:
                handle.write(json.dumps(details))
    except FileNotFoundError:
        return (result_message
                (False,
                 "Error: The file was not found.", ""))
    except IOError:
        return (result_message
                (False,
                 "Error: Could not write to the file.",
                 ""))
    except Exception as e:
        return (result_message
                (False,
                 f"An unexpected error occurred: {e}",
                 ""))
    else:
        return (result_message
                (True, "File written successfully.",
                 ""))


def add_author(author: dict, data: list[dict]):
    data.append(author)
    return data


def fetch_post_by_id(blog_id):
    blog_posts = fetch_data(JSON_DATA_PATH)[PAYLOAD]
    for post in blog_posts:
        if post[ID] == blog_id:
            return post


def delete_post(blog_id):
    blog_posts = fetch_data(JSON_DATA_PATH)[PAYLOAD]

    post = fetch_post_by_id(blog_id)

    blog_posts.remove(post)

    return write_data(blog_posts, JSON_DATA_PATH)


def update_post(post_id: int, author: str, title: str, content: str,
                like: int):
    delete_post(post_id)

    return add_post(author, title, content, like)


def add_post(author, title, content, like) -> dict:
    blog_posts = fetch_data(JSON_DATA_PATH)
    updated_blog_posts = add_author(
        build_dict(get_last_id(blog_posts), author,
                   title, content, like),
        blog_posts[PAYLOAD])

    return write_data(updated_blog_posts, JSON_DATA_PATH)


def build_dict(post_id: int,
               author: str,
               title: str,
               content: str,
               like: int) -> dict:
    return {
        ID: post_id,
        AUTHOR: author,
        TITLE: title,
        CONTENT: content,
        LIKE: like
    }


def build_to_add_dict(
        author: str,
        title: str,
        content: str) -> dict:
    return {
        AUTHOR: author,
        TITLE: title,
        CONTENT: content
    }


def get_last_id(blog_posts) -> int:
    try:
        return blog_posts[PAYLOAD][-1][ID] + 1
    except IndexError:
        return 1


def get_like_id(like) -> int:
    return like + 1
