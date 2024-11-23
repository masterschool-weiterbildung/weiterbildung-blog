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
