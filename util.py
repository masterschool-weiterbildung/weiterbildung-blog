import json
from pathlib import WindowsPath

from constant_blog import RESULT, MESSAGE, PAYLOAD, ID, JSON_DATA_PATH, \
    CONTENT, AUTHOR, TITLE, LIKE

cached_data = None


def result_message(result: bool, message: str, payload) -> dict:
    """
    Construct a standardized result message dictionary.

    Parameters:
        result (bool): The result of the operation (True or False).
        message (str): A message describing the result.
        payload (dict or list): The data associated with the result.

    Returns:
        dict: A dictionary containing the result, message, and payload.
    """
    return {RESULT: result, MESSAGE: message,
            PAYLOAD: payload}


def fetch_data(file_path: WindowsPath) -> result_message:
    """
    Fetch data from a JSON file, using a cache for repeated accesses.

    Parameter:
        file_path (WindowsPath): The path to the JSON file.

    Returns:
        result_message: A standardized result message containing the result of
        the fetch operation and the data (or an error message if the fetch failed).
    """
    global cached_data

    if cached_data is None:
        cached_data = load_data(file_path)
    return cached_data


def load_data(file_path: WindowsPath) -> result_message:
    """
    Load data from a JSON file.

    Parameter:
        file_path (WindowsPath): The path to the JSON file.

    Returns:
        result_message: A standardized result message containing the result of
        the load operation and the data (or an error message if loading failed).
    """
    payload = []
    try:
        if "json" in file_path.name:
            with open(file_path, "r") as handle:
                payload = json.load(handle)
    except FileNotFoundError as e:
        return (result_message
                (False,
                 f"Error: The file was not found. {e}", []))
    except IOError:
        return (result_message
                (False,
                 "Error: Could not read the file.", []))
    except Exception as e:
        return (result_message
                (False,
                 f"An unexpected error occurred: {e}",
                 []))
    else:
        return (result_message
                (True, "File loaded successfully.",
                 payload))


def write_data(details: list[dict],
               file_path: WindowsPath) -> result_message:
    """
    Write data to a JSON file.

    Parameter:
        details (list[dict]): A list of dictionary data to be written.
        file_path (WindowsPath): The path to the JSON file.

    Returns:
        result_message: A standardized result message containing the result of
        the write operation and an appropriate message (success or error).
    """
    try:
        if "json" in file_path.name:
            with open(file_path, 'w') as handle:
                handle.write(json.dumps(details))
    except FileNotFoundError:
        return (result_message
                (False,
                 "Error: The file was not found.", []))
    except IOError:
        return (result_message
                (False,
                 "Error: Could not write to the file.",
                 []))
    except Exception as e:
        return (result_message
                (False,
                 f"An unexpected error occurred: {e}",
                 []))
    else:
        return (result_message
                (True, "File written successfully.",
                 []))


def add_author(author: dict, data: list[dict]) -> list[dict]:
    """
    Add a new author to a list of blog posts.

    Parameters:
        author (dict): A dictionary containing the author details.
        data (list[dict]): The list of existing blog posts.

    Returns:
        list[dict]: The updated list of blog posts with the new author added.
    """
    data.append(author)
    return data


def fetch_post_by_id(blog_id) -> dict:
    """
    Fetch a blog post by its unique ID.

    Parameter:
        blog_id (int): The unique ID of the blog post.

    Returns:
        dict: The blog post matching the ID, or None if not found.
    """
    blog_posts = fetch_data(JSON_DATA_PATH)[PAYLOAD]
    for post in blog_posts:
        if post[ID] == blog_id:
            return post


def delete_post(blog_id) -> result_message:
    """
    Delete a blog post by its unique ID.

    Parameter:
        blog_id (int): The unique ID of the blog post to delete.

    Returns:
        result_message: A standardized message containing the result of
        the delete operation.
    """
    blog_posts = fetch_data(JSON_DATA_PATH)[PAYLOAD]

    post = fetch_post_by_id(blog_id)

    blog_posts.remove(post)

    return write_data(blog_posts, JSON_DATA_PATH)


def update_post(post_id: int, author: str, title: str, content: str,
                like: int) -> result_message:
    """
    Update an existing blog post.

    Parameters:
        post_id (int): The unique ID of the blog post to update.
        author (str): The new author of the blog post.
        title (str): The new title of the blog post.
        content (str): The new content of the blog post.
        like (int): The like count for the blog post.

    Returns:
        result_message: A standardized message containing the result of
        the update operation.
    """
    delete_post(post_id)

    return add_post(author, title, content, like)


def add_post(author, title, content, like) -> result_message:
    """
    Add a new blog post.

    Parameters:
        author (str): The author of the new blog post.
        title (str): The title of the new blog post.
        content (str): The content of the new blog post.
        like (int): The initial like count for the blog post.

    Returns:
        result_message: A standardized message containing the result of
        the add operation.
    """
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
    """
    Build a dictionary representing a blog post.

    Parameters:
        post_id (int): The unique ID of the blog post.
        author (str): The author of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.
        like (int): The like count of the blog post.

    Returns:
        dict: A dictionary representing the blog post.
    """
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
    """
    Build a dictionary for adding a blog post without an ID or like count.

    Parameters:
        author (str): The author of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    Returns:
        dict: A dictionary containing the author, title, and content of the post.
    """
    return {
        AUTHOR: author,
        TITLE: title,
        CONTENT: content
    }


def get_last_id(blog_posts) -> int:
    """
    Retrieve the last ID from the list of blog posts and generate the next ID.

    Parameter:
        blog_posts (dict): A dictionary containing a list of blog posts.

    Returns:
        int: The next unique ID for a new blog post.
    """
    try:
        return blog_posts[PAYLOAD][-1][ID] + 1
    except IndexError:
        return 1


def get_like_id(like) -> int:
    """
    Increment the like count for a blog post.

    Parameter:
        like (int): The current like count.

    Returns:
        int: The incremented like count.
    """
    return like + 1
