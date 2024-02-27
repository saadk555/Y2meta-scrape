from flask import Flask, jsonify, request
import re 
from get import get_mp3_download_link 

app = Flask(__name__)

@app.route("/get_download_link", methods=["GET"])
def api_get_link():
    video_input = request.args.get("video_url") 

    if not video_input:
        return jsonify({"error": "Missing 'video_url' parameter"}), 400 

    # Assume input is in the format: {video_id}?si=...
    video_id_pattern = r"(.+)\?si="  
    match = re.search(video_id_pattern, video_input)

    if match:
        youtube_id = match.group(1)  
        new_video_url = "https://y2meta.app/en/youtube/" + youtube_id

        try:
            download_link = get_mp3_download_link(new_video_url)
            return jsonify({"download_link": download_link})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 
    else:
        return jsonify({"error": "Invalid input format. Expecting only the video ID and query parameters"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0") 
