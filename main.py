import google.generativeai as genai
from gemini_key import gemini_key
from stability_key import stability_key
import os
genai.configure(api_key=gemini_key)

import base64
import requests

import sys

model = genai.GenerativeModel("gemini-1.5-flash")
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')

if stability_key is None:
    raise Exception("Missing Stability API key.")

def get_image(prompt):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {stability_key}"
        },
        json={
            "text_prompts": [
                {
                    f"text": "Apple commercial style image including {prompt} as the product"
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))

def main():
    # Check if a command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <commercial_topic>")
        sys.exit(1)

    # Get the key_value from the command-line argument
    commercial_topic = sys.argv[1]
    
    script = f"make a commercial speech about {commercial_topic}, intended for about 30-60 sec"
    script = "create a picture of a banana"
    response = model.generate_content(script)
    print(response.text)

    #get_image(commercial_topic)
 
# clip creation API
# video AI API
# music AI API
# text AI API
# speech AI API

'''
x = "prompt"
video = video-api-call(x)
music = audio-api-call("apple commerical")
text = text-api-call(x)
speech = speech-api-call(text)

clip = clip-creation-api(video, music, speech)
'''

if __name__ == "__main__":
    main()
