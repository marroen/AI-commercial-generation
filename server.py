import sys
print(sys.executable)

from flask import Flask, request, send_file, send_from_directory
import subprocess
import os


app = Flask(__name__)

# Define the path to the directory where the video is stored
OUT_DIR = 'out'

# Serve the video files from the /out directory
@app.route('/out/<path:filename>')
def serve_video(filename):
    return send_from_directory(OUT_DIR, filename)

@app.route('/')
def index():
    return send_file('index.html')  # Make sure index.html is in the correct path

@app.route('/generate', methods=['POST'])
def generate_video():
    prompt = request.form.get('prompt')

    # Construct the command with -g for content generation
    command = [sys.executable, 'main.py', '-t', prompt, '-g']

    # Run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return f"Error generating video: {str(e)}", 500

    # After generating the video, return the video file
    if os.path.exists('out/video.mp4'):
        return send_file('out/video.mp4', mimetype='video/mp4')
    else:
        return "Video generation failed", 500

if __name__ == '__main__':
    app.run(debug=True)
