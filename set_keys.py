import json
import os

resource_group = "tweet2flash-rg"
functionapp_name = "tweet2flash-api"

with open("local.settings.json") as f:
    keys = json.load(f)["Values"]
    openai_key = keys["OPENAI_API_KEY"]
    twitter_token = keys["TWITTER_BEARER_TOKEN"]
    exa_api = keys["EXA_API"]

# settings_flags = f"--settings OPENAI_API_KEY={openai_key} TWITTER_BEARER_TOKEN={twitter_token}"
settings_flags = f"--settings EXA_API={exa_api}"
command = f'az functionapp config appsettings set --name {functionapp_name} --resource-group {resource_group} {settings_flags}'

# print(command)
os.system(command)