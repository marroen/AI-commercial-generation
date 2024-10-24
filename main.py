import inspect
import pathlib
import argparse
import asyncio
import os
import base64
import requests
import sys
import re
import glob
from random import randrange

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

# configure keys
genai.configure(api_key=gemini_key)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")
engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
eleven_client = ElevenLabs(api_key=eleven_key)

def create_video(n):

    # create speech
    speech_length = MP3("out/speech.mp3").info.length
    speech = AudioFileClip("out/speech.mp3") # .subclip(0, speech_length)

    # set video duration based on speech length
    video_duration = speech_length + 7

    # load music
    # prompt: an apple (company) commercial style background song , 30 sec, modernistic, technological
    # other prompts for other songs included adding tags like explorative, mysterious, orchestral, and removing the length requirement
    song_id = randrange(3)+1
    music = AudioFileClip("out/song_" + str(song_id) + ".mp3").subclip(0, video_duration).volumex(0.5)

    # load image(s)
    images = []
    for i in range(0, n):
        image = ImageClip(f"out/image_{i}.png").set_duration(video_duration/n).set_position('center')
        
        if i == 0:
            image = image.fx(vfx.fadein, 1)
        elif i == n-1:
            image = image.fx(vfx.fadeout, 1)
        images.append(image)
    image_sequence = concatenate_videoclips(images, method="compose")

    # prepare and write videofile
    combined_audio = CompositeAudioClip([speech.set_start(5), music.set_start(0)])
    video = image_sequence.set_audio(combined_audio)
    video.write_videofile("out/video.mp4", fps=24)

def create_vid2():
    # create speech
    speech = AudioFileClip("out/speech.mp3")
    speech_length = MP3("out/speech.mp3").info.length
    # set video duration based on speech length
    target_duration = speech_length + 7

    videos = glob.glob("out/videos/*.mp4")
    i = 0
    duration = 0
    seq = []
    while (i < len(videos) and duration < target_duration):
        clip = VideoFileClip(videos[i])
        seq.append(clip)
        duration += clip.duration
        i += 1

    video_sequence = concatenate_videoclips(seq, method="compose")

    # slow down clips if length of video is too short
    if video_sequence.duration < target_duration:
        factor = video_sequence.duration / target_duration
        video_sequence = video_sequence.fx(vfx.speedx, factor)

    # load music
    # prompt: an apple (company) commercial style background song , 30 sec, modernistic, technological
    # other prompts for other songs included adding tags like explorative, mysterious, orchestral, and removing the length requirement
    song_id = randrange(3) + 1
        
    music = AudioFileClip("out/song_" + str(song_id) + ".mp3").subclip(0, target_duration).volumex(0.5)

    # prepare and write videofile
    combined_audio = CompositeAudioClip([speech.set_start(5), music.set_start(0)])
    video = video_sequence.set_audio(combined_audio)

    video.fx(vfx.fadeout, 1)
    video.write_videofile("out/video_2.mp4", fps=24)


async def create_speech(script):

    speaker_id = randrange(2)
    audio = eleven_client.generate(
        text=script,
        voice= "Charlotte" if speaker_id == 0 else "Callum",
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
                        "text": f"{prompt} made by Apple (company)",
                        "weight": 1
                    },
                    {
                        "text": f"photorealistic, fujifilm 4k, (apple logo), usb port, wires, plugged in",
                        "weight": 0.7
                    },
                    {
                        "text": f"Ugly, bad faces, nsfw, worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch, no {prompt}",
                        "weight": -1
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
    parser.add_argument('-t', "--topic"   , dest="commercial_topic", required=False,  type=str, help="The commercial topic.")
    parser.add_argument('-n',               dest="n",                required=False, type=int, help="The number of images to produce for the video. WARNING: ensure you have enough ElevenLabs credits.")
    parser.add_argument('-g', "--gui",      dest="gui",              required=False, action='store_true', help="Used only internally by the website GUI.")

    parser.set_defaults(gui=False)
    parser.set_defaults(n=5)

    args = parser.parse_args()
    commercial_topic = args.commercial_topic
    n = args.n
    gui = args.gui

    if commercial_topic == None:
        print(f"Generating video only")
        create_vid2()

    else:
        yes_or_no = input("This will cost credits. Are you sure you want to proceed? (y/n): ").strip()

        if yes_or_no == 'y' or gui:
            commercial_length = n * 40

            script = f"make a commercial speech about {commercial_topic}, intended for about {commercial_length} sec, in the style of an Apple (the company) commercial, and include ONLY the actual lines from the narrator, not stuff like 'It was a sunny day', and also do not literally write **Narrator** whenever the narrator speaks, and do not describe the scenery ala 'closeup shot of the banana', I repeat, DO NOT DESCRIBE THE SCENERY NOR WHAT IS HAPPENING IN THE COMMERCIAL, ONLY WRITE EXACTLY WHAT THE NARRATOR SAYS"

            response = gemini_model.generate_content(script)
            processed_text = re.sub("\(.*?\)|\[.*?\]", "", response.text)
            print(processed_text)

            await create_image(commercial_topic, n)
            await create_speech(processed_text)
            create_video(n)

asyncio.run(main())

if __name__ == "__main__":
    main()
