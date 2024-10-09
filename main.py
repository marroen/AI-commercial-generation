import google.generativeai as genai
from key import key
import os
genai.configure(api_key=key)

import sys

model = genai.GenerativeModel("gemini-1.5-flash")

def main():
    # Check if a command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <commercial_topic>")
        sys.exit(1)

    # Get the key_value from the command-line argument
    commercial_topic = sys.argv[1]
    
    script = f"make a commercial speech about {commercial_topic}, intended for about 30-60 sec"
    response = model.generate_content(script)
    print(response.text)

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
