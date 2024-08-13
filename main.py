import logging
from flask import Flask, jsonify, send_file
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# List all JSON files in the base directory
@app.route("/files", methods=["GET"])
def list_files():
    files = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".json")]
    logging.debug(f"Files found: {files}")
    return jsonify(files)

# Serve the content of a selected JSON file
@app.route("/files/<filename>", methods=["GET"])
def get_file(filename):
    logging.debug(f"Request for file: {filename}")
    if os.path.isfile(filename) and filename.endswith(".json"):
        return send_file(filename)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080, debug=True)
    except Exception as e:
        logging.error(f"Error starting application: {e}")

