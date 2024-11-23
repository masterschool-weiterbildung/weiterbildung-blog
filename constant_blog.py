from pathlib import Path

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
LIKE = "like"
