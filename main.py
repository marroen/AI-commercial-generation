import inspect
import pathlib
import argparse
import asyncio
import os
import base64
import requests
import sys

# API imports
import google.generativeai as genai
from gemini_key import gemini_key
from stability_key import stability_key
from eleven_key import eleven_key
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
from moviepy.editor import *
from mutagen.mp3 import MP3

if gemini_key is None:
    raise Exception("Missing Gemini API key.")
elif stability_key is None:
    raise Exception("Missing Stability API key.")
elif eleven_key is None:
    raise Exception("Missing ElevenLabs API key.")

# Configure keys
genai.configure(api_key=gemini_key)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
eleven_client = ElevenLabs(api_key=eleven_key)

def create_video(n):

    # Load image(s)
    images = []
    for i in range(0, n):
        image = ImageClip(f"out/image_{i}.png").set_duration(15).set_position('center')
        
        if i == 0:
            image = image.fx(vfx.fadein, 1)
        elif i == n-1:
            image = image.fx(vfx.fadeout, 1)
        images.append(image)
    image_sequence = concatenate_videoclips(images, method="compose")

    # Create speech
    speech_length = MP3("out/speech.mp3").info.length
    speech_length = 45 if speech_length >= 45 else speech_length
    speech = AudioFileClip("out/speech.mp3").subclip(0, speech_length)

    # Load music
    # prompt: an apple (company) commercial style background song , 30 sec, modernistic, technological
    music = AudioFileClip("out/innovate.mp3").subclip(0, 45).volumex(0.5)

    # Prepare and write videofile
    combined_audio = CompositeAudioClip([speech.set_start(5), music.set_start(0)])
    video = image_sequence.set_audio(combined_audio)
    video.write_videofile("out/video.mp4", fps=24)

async def create_speech(script):

    audio = eleven_client.generate(
        text=script,
        voice="Charlotte", # Callum for male
        model="eleven_multilingual_v2"
    )
    save(audio, "out/speech.mp3")
    await asyncio.sleep(6)

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

    parser = argparse.ArgumentParser(description="AI Commercial Generator.")
    parser.add_argument('-t', "--topic"   , dest="commercial_topic", required=True,  type=str, help="The commercial topic.")
    parser.add_argument('-g', "--generate", dest="should_generate" , required=False, action='store_true', help="Whether to generate new content or to look for existing content for the video. WARNING: this will use credits from the AI APIs.")
    parser.add_argument('-n',               dest="n",                required=False, type=int, help="The number of images to produce for the video, with each image being on-screen for 15 sec. WARNING: ensure you have enough ElevenLabs credits.")
    parser.set_defaults(should_generate=False)
    parser.set_defaults(n=3)

    args = parser.parse_args()
    commercial_topic = args.commercial_topic
    n = args.n

    commercial_length = n * 60
    
    script = f"make a commercial speech about {commercial_topic}, intended for about {commercial_length} sec, in the style of an Apple (the company) commercial, and include ONLY the actual lines from the narrator, not stuff like 'It was a sunny day', and also do not literally write **Narrator** whenever the narrator speaks, and do not describe the scenery ala 'closeup shot of the banana', I repeat, DO NOT DESCRIBE THE SCENERY NOR WHAT IS HAPPENING IN THE COMMERCIAL, ONLY WRITE EXACTLY WHAT THE NARRATOR SAYS"

    if args.should_generate:
        response = gemini_model.generate_content(script)
        print(response.text)
        await create_image(commercial_topic, n)
        await create_speech(response.text)

    create_video(n) 

asyncio.run(main())

if __name__ == "__main__":
    main()
