# -*- coding: utf-8 -*-
"""hal.py
A demonstration of machine intelligence for Tom Sachs Studio.

HAL is, right now, a speaking chatbot. Audition is handled locallly by OpenAI's Whisper, text is
sent to OpenAI's GPT-3 to generate a response, which is then translated into decently realistic
speech using AWS Polly.

This is a practicing of sympathetic magic. We can and must expand our minds from MGI.
"""

MARK_1_ENDEAVOR = """  __  __            _      _____
 |  \/  | __ _ _ __| | __ |_   _|       ___ _  _ ___  ___   ___   _____  ___
 | \  / |/ _` | '__| |/ /   | |        | __| \| |   \| __| /_\ \ / / _ \| _ \\
 | |\/| | (_| | |  |   <   _| |_   _   | _|| .` | |) | _| / _ \ V / (_) |   /
 |_|  |_|\__,_|_|  |_|\_\ |_____| |_|  |___|_|\_|___/|___/_/ \_\_/ \___/|_|_\\"""

HAL_1000 = """
 ██╗  ██╗ █████╗ ██╗          ██╗ ██████╗  ██████╗  ██████╗
 ██║  ██║██╔══██╗██║         ███║██╔═████╗██╔═████╗██╔═████╗
 ███████║███████║██║         ╚██║██║██╔██║██║██╔██║██║██╔██║
 ██╔══██║██╔══██║██║          ██║████╔╝██║████╔╝██║████╔╝██║
 ██║  ██║██║  ██║███████╗     ██║╚██████╔╝╚██████╔╝╚██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚═╝ ╚═════╝  ╚═════╝  ╚═════"""

TOM_SACHS = """
 A demonstration of machine consciousness.      .#+=:                      .:
                                               .*   =#.                   ++=#.
  =+#%*++++++:                                 =*    %-                  +*  **
 #  * #+                                        #- .#*                  .%:  %=
 +=:  -%-     .=+-   ::.                        :%+#=                   =%. ++      .#:
       ##   .=%=:*%++=#*  -+.  :=+-       ::     #%+      ..     .=**+  +%.*=        ##*.
     .-#%*+=*%====%+  +#:#-*%.*+ .%:      :*= .=#=.*=    *==#  -*+:     +%#**+#:  -  %..*-
    *#: #=  =#   :%.  :%%+ :%%+   **        +%%#.  .%+  =+  %-=%-    .:*#%%+  :#  +**+   #-
   -%.  #=  :%-.-*:    #+   -=    =#       +=:+.    #%  -#=*=:-=*++**+=: %#    +*-=*+*=--#=
    -++**    :==-                              *:+##%.    ..              =-     ::.    ..
"""

# Load libraries necessary for print_with_delay
from time import sleep
import numpy as np


def print_with_delay(text, delay=None):
	if not delay:
		delay = 0
		# delay = 1.2 * np.random.random()
	sleep(delay)
	print(text)

# Print boot texts
print(MARK_1_ENDEAVOR)
print_with_delay(HAL_1000, delay=0.4)
print_with_delay(TOM_SACHS, delay=0.4)

##################
# LOAD LIBRARIES #
##################
print("\033[33mLoading libraries...\033[0m")
# Load system libraries
import io
import os
import subprocess
import sys
from pathlib import Path
from contextlib import closing
print_with_delay("  System libraries loaded")

# Load third-party libraries
import openai
import soundfile as sf
import speech_recognition as sr
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
print_with_delay("  Audition libraries loaded")
print_with_delay("  Speech libraries loaded")
print_with_delay("  Cognition libraries loaded")

############
# AUDITION #
############
print_with_delay("\033[33mConfiguring auditory systems...\033[0m")

# Put temporarily recorded audio for Whisper to decode here.
tmp_path = Path(".tmp.wav")

# Mic input settings
print_with_delay("  Initializing microphone")
r = sr.Recognizer()
r.energy_threshold = 300
r.pause_threshold = 0.8
r.dynamic_energy_threshold = False

# Audition implementation
print_with_delay("  Loading speech recognition into memory")
def transcribe_audio(fp):
	command = f"audition/main -m audition/models/ggml-base.en.bin -f {fp} -otxt"
	subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	with open(f"{fp}.txt", "r") as f:
		return f.read().strip()

##########
# SPEECH #
##########
print_with_delay("\033[33mConfiguring speech systems...\033[0m")

# Configure AWS Polly
print_with_delay("  Spinning up neural voice engine")
session = Session()
polly = session.client("polly")
print_with_delay("  Readying output")
def tts(text):
	# Request speech synthesis
	try:
		response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Kevin", Engine="neural")
	except (BotoCoreError, ClientError) as error:
		print(error)
		sys.exit(-1)

	# Access the audio stream from the response
	if "AudioStream" in response:
		with closing(response["AudioStream"]) as stream:
			output = ".response.mp3"
			try:
				with open(output, "wb") as f:
					f.write(stream.read())
			except IOError as error:
				print(error)
				sys.exit(-1)
			play_command = f"sleep 0.05 && ffplay -nodisp -autoexit {output}"
			subprocess.run(play_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	else:
		print("Could not stream audio")
		sys.exit(-1)

#############
# COGNITION #
#############
print_with_delay("\033[33mConfiguring congition systems...\033[0m")

# Load environmental variables
load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')

# Connect to GPT-3
print_with_delay("  Bringing frontal cortex online")
completion = openai.Completion()

# Initial GPT-3 prompt
print_with_delay("  Resetting memory to base state")
chat_log = """The following is a transcript of a conversation between a human and a fully consious machine intelligence named HAL reliably passes the turing test. HAL always answers questions truthfully and fully and is fully aware of its own existence.

Human: Hello.
HAL: Hello.
"""

def query(question, chat_log):
	"""Query GPT-3 with chat log as prompt."""
	prompt = f'{chat_log}Human: {question}\nHAL:'
	response = completion.create(prompt=prompt, engine="davinci", stop=["Human:","Humans:", "HAL:"],
			temperature=0.95, top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
			max_tokens=150)
	answer = response.choices[0].text.strip()
	return answer

print_with_delay("\nConiguration complete")

with sr.Microphone(sample_rate=16000) as source:
	print("\033[32mALL SYSTEMS GO\033[0m")
	print("\nTRANSCRIPT:\n")

	# Get speech and process after breaks
	while True:
		# Record and save audio prompts
		audio = r.listen(source)
		data = io.BytesIO(audio.get_wav_data())
		y, sr = sf.read(data)
		sf.write(tmp_path, y, sr)

		# Transcribe audio to text
		result = transcribe_audio(tmp_path).replace("Sacks", "Sachs").replace("Sax", "Sachs")
		print(result)

		# Handle specific command prompts
		if "terminate" in result.lower():
			tts("Taking all systems offline.")
			break
		
		# Get response from GPT-3
		response = query(result, chat_log)
		print(">>>", response)

		# Speak response
		tts(response)

		# Append to working memory
		chat_log += f"Human: {result}\nHAL:{response}"

# Remove temporary paths
tmp_path.unlink()
Path(".tmp.wav.txt").unlink()
Path(".response.mp3").unlink()
