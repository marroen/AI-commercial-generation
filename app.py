from flask import Flask, request, jsonify
import asyncio
import os

# Import the existing functions from your script
from main import create_image, create_video, create_speech

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get('prompt')
    n = data.get('n', 5)  # Default to 5 images if not provided

    # Generate content using existing functions
    try:
        # Create images and speech
        asyncio.run(create_image(prompt, n))
        # Optionally create speech if needed
        # asyncio.run(create_speech(f"Commercial for {prompt}"))
        
        # Create video based on the generated images
        create_video(n)

        # Return paths to the generated video
        video_path = '/out/video.mp4'

        return jsonify({
            'status': 'success',
            'video_url': video_path
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
