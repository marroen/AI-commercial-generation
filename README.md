
Steps:
1. Ensure you have python version 3.10 or above BEFORE running any pip installs (recommend pyenv for python version management)
2. run `pip install --upgrade google-api-python-client`

3. https://ai.google.dev/gemini-api/docs/quickstart?lang=python
Follow this to install google-generativeui and to create a key
4. Once you have the key, run `python integrate_gemini_key.py [key_value]` to integrate your Gemini key with the environment
5. Create a stability.ai key: https://platform.stability.ai/account/keys
6. Once you have it run `python integrate_stability_key.py [key_value]`
7. Run `python main.py [commercial_topic]`, like `python main.py banana`
