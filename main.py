import inspect
import asyncio
import google.generativeai as genai
from gemini_key import gemini_key
from stability_key import stability_key
from eleven_key import eleven_key
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
from moviepy.editor import *
from mutagen.mp3 import MP3
import os
genai.configure(api_key=gemini_key)

import base64
import requests

import sys

model = genai.GenerativeModel("gemini-1.5-flash")
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')

def create_video(n):
    images = []
    for i in range(0, n):
        images.append(ImageClip(f"out/image_{i}.png").set_duration(15))
    image_sequence = concatenate_videoclips(images, method="compose")

    speech_length = MP3("out/speech.mp3").info.length
    speech_length = 45 if speech_length >= 45 else speech_length
    speech = AudioFileClip("out/speech.mp3").subclip(0, speech_length)

    # prompt: an apple (company) commercial style background song , 30 sec, modernistic, technological
    music = AudioFileClip("out/innovate.mp3").subclip(0, 45).volumex(0.5)

    combined_audio = CompositeAudioClip([speech.set_start(5), music.set_start(0)])

    video = image_sequence.set_audio(combined_audio)

    video.write_videofile("out/video.mp4", fps=24)

async def create_speech(script):
    female = "XB0fDUnXU5powFXDhCwa" # Charlotte
    male = "N2lVS1w4EtoT3dr4eOWO" # Callum
    CHUNK_SIZE = 1024
    url = f"https:/api.elevenlabs.io/v1/text-to-speech/6"

    client = ElevenLabs(api_key=eleven_key)

    audio = client.generate(
        text=script,
        voice="Charlotte",
        model="eleven_multilingual_v2"
    )
    save(audio, "out/speech.mp3")
    await asyncio.sleep(6)

if stability_key is None:
    raise Exception("Missing Stability API key.")

async def create_image(prompt, n):
    for i in range(0, n):
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
                        "text": f"Apple (company) commercial-style image, BUT also include a lot of {prompt}"
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

        for _, image in enumerate(data["artifacts"]):
            with open(f"./out/image_{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))
        await asyncio.sleep(6)

async def main():
    # Check if a command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <commercial_topic>")
        sys.exit(1)

    # Get the key_value from the command-line argument
    commercial_topic = sys.argv[1]
    
    script = f"make a commercial speech about {commercial_topic}, intended for about 150 sec, in the style of an Apple (the company) commercial, and include ONLY the actual lines from the narrator, not stuff like 'It was a sunny day', and also do not literally write **Narrator** whenever the narrator speaks, and do not describe the scenery ala 'closeup shot of the banana', I repeat, DO NOT DESCRIBE THE SCENERY NOR WHAT IS HAPPENING IN THE COMMERCIAL, ONLY WRITE EXACTLY WHAT THE NARRATOR SAYS"
    response = model.generate_content(script)

    print(response.text)

    n = 3

    #await create_image(commercial_topic, n)

    #await create_speech(response.text)

    create_video(n) 

asyncio.run(main())

if __name__ == "__main__":
    main()
