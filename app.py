from flask import Flask, jsonify, request
import re
import json
import threading
import time
from get import get_mp3_download_link

app = Flask(__name__)

download_cache = {}  # Our in-memory cache

# Optionally load from file at startup
try:
    with open('cache.json', 'r') as f:
        download_cache = json.load(f)
    print('Cache loaded from file:', download_cache)  # Debug print
except FileNotFoundError:
    print('Cache file not found')  # Debug print

@app.route("/get_download_link", methods=["GET"])
def api_get_link():
    video_url = request.args.get("video_url")

    if not video_url:
        return jsonify({"error": "Missing 'video_url' parameter"}), 400 

    youtube_id = video_url.split("=")[-1]
    new_video_url = "https://y2meta.app/en/youtube/" + youtube_id

    # Cache Check (with Cleanup)
    if youtube_id in download_cache:
        print('Found youtube_id in cache:', youtube_id)  # Debug print
        now = time.time()
        if now - download_cache[youtube_id]['timestamp'] > 360:  
            print('Removing youtube_id from cache:', youtube_id)  # Debug print
            del download_cache[youtube_id] 
        else:
            print('Returning cached download link for youtube_id:', youtube_id)  # Debug print
            return jsonify({"download_link": download_cache[youtube_id]['link']})

    # Fetch download link (replace with your get_mp3_download_link logic)
    try:
        download_link = get_mp3_download_link(new_video_url)  # Your Selenium function from get.py
        print('Fetched download link:', download_link)  # Debug print
        download_cache[youtube_id] = {'link': download_link, 'timestamp': time.time()}
        print('Added youtube_id to cache:', youtube_id)  # Debug print
        return jsonify({"download_link": download_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

def save_cache():
    with open('cache.json', 'w') as f:
        json.dump(download_cache, f)
    print('Cache saved to file')  # Debug print

threading.Timer(300, save_cache).start()  # Save cache every 5 minutes

if __name__ == "__main__":
    app.run(host="0.0.0.0")