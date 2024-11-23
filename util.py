import json
from pathlib import Path, WindowsPath

PACKAGE_STATIC = "static"

PACKAGE_DATA = "data"

PACKAGE_JSON_FILE = "data.json"

JSON_DATA_PATH = Path(
    __file__).parent / PACKAGE_STATIC / PACKAGE_DATA / PACKAGE_JSON_FILE

RESULT = "result"
MESSAGE = "message"
PAYLOAD = "payload"

ID = "id"
AUTHOR = "author"
TITLE = "title"
CONTENT = "content"

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


def write_data(details: dict,
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


def update_post(post_id: int, author: str, title: str, content: str):
    delete_post(post_id)

    return add_post(author, title, content)


def add_post(author, content, title):
    blog_posts = fetch_data(JSON_DATA_PATH)
    updated_blog_posts = add_author(
        build_dict(get_last_id(blog_posts), author,
                   title, content),
        blog_posts[PAYLOAD])

    return write_data(updated_blog_posts, JSON_DATA_PATH)


def build_dict(id: int,
               author: str,
               title: str,
               content: str) -> dict:
    return {
        ID: id,
        AUTHOR: author,
        TITLE: title,
        CONTENT: content
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
    return blog_posts[PAYLOAD][-1][ID] + 1
