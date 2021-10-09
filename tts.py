import functools
import requests
import textwrap
import os.path
import json
import sys

data = []
lastUsed = {}

def compare(dic1, dic2):
    s1 = dic1["language"] + dic1["gender"] + dic1["name"]
    s2 = dic2["language"] + dic2["gender"] + dic2["name"]

    if s1 > s2:
        return 1
    elif s2 > s1:
        return -1
    else:
        return 0

if len(sys.argv) == 2 and sys.argv[1].lower().startswith("-h"):
    print(
"""TTS-Grabber v1.0 @ https://github.com/BleachDrinker420/TTS-Grabber

PARAMETER           TYPE  DESCRIPTION
-h, -help           ---   Shows the help info.
-v, -voice          Int   Sets the voice id to use.
-s, -speed          Int   Sets the TTS voice speed (in percent).
-vol, -volume       Int   Changes the TTS volume (in decibels).
-pp, -period-pause  Flt   Sets how long the TTS should pause for at periods (in seconds).
-cp, -comma-pause   Flt   Sets how long the TTS should pause for at commas (in seconds).
-lp, -line-pause    Flt   Sets how long the TTS should pause for at newlines (in seconds).

To see a list of the voices available, run the script without the -v parameter.""")
    sys.exit()
    

arg_voice = -1
arg_speed = 100
arg_volume = 0
arg_period_pause = -1
arg_comma_pause = -1
arg_line_pause = -1

_loop = 1
while _loop <= len(sys.argv) - 2:
    try:
        arg = sys.argv[_loop].lower()
        if arg == "-v" or arg == "-voice":
            arg_voice = int(sys.argv[_loop + 1])
        elif arg == "-s" or arg == "-speed":
            arg_speed = int(sys.argv[_loop + 1])
        elif arg == "-vol" or arg == "-volume":
            arg_volume = float(sys.argv[_loop + 1])
        elif arg == "-pp" or arg == "-period-pause":
            arg_period_pause = float(sys.argv[_loop + 1])
        elif arg == "-cp" or arg == "-comma-pause":
            arg_comma_pause = float(sys.argv[_loop + 1])
        elif arg == "-lp" or arg == "-line-pause":
            arg_line_pause = float(sys.argv[_loop + 1])
    except:
        print("error > " + sys.argv[_loop] + " | " + sys.argv[_loop + 1])
        pass
    _loop += 2

if os.path.isfile("lastused.json"):
    with open('lastused.json', encoding='utf-8') as f:
        lastUsed = json.loads(f.read())

with open('data.json', encoding='utf-8') as f:
    js_data = json.loads(f.read())

for id_, entry in js_data.items():
    data.append(entry)

data.sort(key=functools.cmp_to_key(compare))

if arg_voice == -1:
    print("ID   LANGUAGE                GENDER  NAME                TYPE")
    for i in range(len(data)):
        print(
            (" " * (3 - len(str(i + 1)))) + str(i + 1)
            + ": " + data[i]["language"] + (" " * (24 - len(data[i]["language"])))
            + data[i]["gender"] + (" " * (8 - len(data[i]["gender"])))
            + data[i]["name"] + (" " * (20 - len(data[i]["name"])))
            + data[i]["voiceType"][0])

    if lastUsed != {}:
        print("...........................................................")
        print("  0: " + lastUsed["language"] + (" " * (24 - len(lastUsed["language"])))
            + lastUsed["gender"] + (" " * (8 - len(lastUsed["gender"])))
            + lastUsed["name"] + (" " * (20 - len(lastUsed["name"])))
            + lastUsed["voiceType"][0])

    print("...........................................................")
    arg_voice = int(input("Choose voice: "))

if arg_voice == 0:
    voice = lastUsed
else:
    voice = data[arg_voice - 1]

if arg_period_pause >= 0:
    ttsText = ttsText.replace(".", ".<break time=\"" + str(ppause) + "s\"/>")
    print("Setting Period Pause To " + str(ppause))

if arg_comma_pause >= 0:
    ttsText = ttsText.replace(",", ",<break time=\"" + str(cpause) + "s\"/>")
    print("Setting Comma Pause To " + str(cpause))

if arg_line_pause >= 0:
    ttsText = ttsText.replace("\n", "\n<break time=\"" + str(lpause) + "s\"/>")
    print("Setting Newline Pause To " + str(lpause))

print("Using Input File (input.txt)")
with open('input.txt', encoding='utf-8') as f:
    ttsText = "".join(f.readlines())

#ttsText = ttsText.replace("\r", "").replace("\n", " ")
ttsTextSplit = textwrap.wrap(ttsText, 1500)
ttsTextLen = len(ttsTextSplit)

with open("lastused.json", "w") as f:
        f.write(json.dumps(voice))

for i in range(ttsTextLen):
    params = {
        "globalSpeed": str(arg_speed) + "%",
        "globalVolume": ("+" if arg_volume >= 0 else "") + str(arg_volume) + "dB",
        "chunk": "<speak><p>" + ttsTextSplit[i] + "</p></speak>",
        "narrationStyle": "regular",
        "platform": "landing_demo",
        "ssml": "<speak><p>" + ttsTextSplit[i] + "</p></speak>",
        "userId": "5pe8l4FrdbczcoHOBkUtp0W37Gh2",
        "voice": voice["value"]
    }
    
    print("Seding request.. [" + str(i + 1) + "/" + str(ttsTextLen) + "]")
    req = requests.post("https://play.ht/api/transcribe", data=params)
    response = json.loads(req.content)

    head = requests.head(response["file"])
    filesize = head.headers.get('content-length', -1)
    print("Getting file.. [" + str(i + 1) + "/" + str(ttsTextLen) + "] (" + str(round(float(filesize) / 1024, 2)) + " KB)")

    filename = "_" + voice["name"] + "-" + str(response["created_at"]) + "-" + str(i + 1) + ".mp3"
    with open(filename, "wb") as f:
        f.write(requests.get(response["file"]).content)

    print("Saved to " + filename)
