from flask import Flask, request, send_file, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')  

@app.route('/generate', methods=['POST'])
def generate_video():
    prompt = request.form.get('prompt')
    subprocess.run(['python', 'main.py', '-t', prompt])
    return send_file('static/video.mp4', mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
