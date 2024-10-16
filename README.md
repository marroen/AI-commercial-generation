Steps:

1. Ensure you have python version 3.10 or above BEFORE running any pip installs (recommend pyenv for python version management)

2. Run `pip install -r requirements.txt`

3. Follow this to install google-generativeui and to create a key:
https://ai.google.dev/gemini-api/docs/quickstart?lang=python

4. Once you have the key, run `python integrate_gemini_key.py [key_value]` to integrate your Gemini key with the environment

5. Create a stability.ai key: https://platform.stability.ai/account/keys

6. Once you have it run `python integrate_stability_key.py [key_value]`

7. Create an account at https://elevenlabs.io/ and create an API key

8. Once you have the key, run `python integrate_eleven_key.py [key_value]`

9. Run `python main.py -t [commercial_topic]`, like `python main.py -t banana`

10. You can also customize it (run python main.py --help for info):

-g if you want to generate new AI content, or else it looks for existing

-n to specify how many images to generate for the video
