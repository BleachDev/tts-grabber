# TTS-Grabber
Quick thing i made about a year ago to download any text with any tts voice, over 630 voices to choose from currently.

It will split the input into multiple files every 1500 words or so to not hit any cutoff limits from TTS providers.

## Usage:  
Edit `input.txt` to change the text to synthesize.

You can run just `tts.py` without any parameters to open the voice selector with default settings.  

#### Parameters
```
PARAMETER           TYPE  DESCRIPTION
-v, -voice          Int   Sets the voice id to use.  
-s, -speed          Int   Sets the TTS voice speed (in percent).  
-vol, -volume       Int   Changes the TTS volume (in decibels).  
-pp, -period-pause  Flt   Sets how long the TTS should pause for at periods (in seconds).  
-cp, -comma-pause   Flt   Sets how long the TTS should pause for at commas (in seconds).  
-lp, -line-pause    Flt   Sets how long the TTS should pause for at newlines (in seconds).
```

Example with parameters:  
`tts.py -v 184 -s 100 -vol 0 -pp 1 -cp 0.5 -lp 2`

###### absolutely no api abuse here
