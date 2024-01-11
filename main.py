
# Importing the libraries ordered by importance
from pytube import YouTube
from pathlib import Path
from gtts import gTTS
import librosa
import librosa.display
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import YouTubeTranscriptApi
import json,xmltodict
import whisper
from moviepy.editor import VideoFileClip
import pandas as pd

# Downloading the video
def download_captions(captions: YouTube.captions, lang: str):
    """ get captions in xlm format from youtube, has words per milisecs
    
    Args:
        captions (YouTube.captions): youtube captions object
        lang (str): language to download  
    Returns:
        str: xml captions"""
    
    # if lang not in captions.keys(): try a.lang
    lang = lang if lang in captions.keys() else 'a.' + lang
    return captions[lang].xml_captions


def get_caption(video_id, lang='en'):
    """ get captions by sentences e.g 'hola esto es una prueba'[start:stop]
    
    Args:
        video_id (str): youtube video id
        lang (str, optional): language to download. Defaults to 'en'.
        
    Returns:
        list: list of dictionaries with start, duration and text of each sentence"""
    # using the srt variable with the list of dictionaries 
    # obtained by the .get_transcript() function
    srt_captions = YouTubeTranscriptApi.get_transcript(video_id, languages=(lang,), preserve_formatting=False)
    return srt_captions

def download_audio_and_caption(video_id, url='https://www.youtube.com/watch?v=', lang='en', by_words=False):
    """ download audio and captions from youtube video

    Args:
        video_id (str): youtube video id
        url (str, optional): youtube url. Defaults to 'https://www.youtube.com/watch?v='.
        lang (str, optional): language to download. Defaults to 'en'.
        by_words (bool, optional): if True download captions by words in xlm format. Defaults to False.

    Returns:
        dict: dictionary with audio path and captions"""
    url = url+video_id
    yt = YouTube(url)
    path = yt.streams.filter(only_audio=True).first().download()
    captions = download_captions(yt.captions, lang) if by_words else get_caption(video_id)
    return {yt.title: {'path': path, 'captions': captions}}


def download_captions(captions, lang):
    """get captions in xlm format from youtube, have words per milisegs"""
    # if lang not in captions.keys(): try a.lang
    lang = lang if lang in captions.keys() else 'a.' + lang
    return captions[lang].xml_captions

# funtion to get the captions from youtube video
def get_caption(video_id, lang='en'):
    """ get captions by sentences e.g 'hola esto es una prueba'[start:stop]"""
    # using the srt variable with the list of dictionaries 
    # obtained by the .get_transcript() function
    srt_captions = YouTubeTranscriptApi.get_transcript(video_id, languages=(lang,), preserve_formatting=False)
    return srt_captions

def download_audio_and_caption(video_id, url='https://www.youtube.com/watch?v=', lang='en', by_words=False):
    url = url+video_id
    yt = YouTube(url)
    path = yt.streams.filter(only_audio=True).first().download()
    captions = download_captions(yt.captions, lang) if by_words else get_caption(video_id)
    return {yt.title: {'path': path, 'captions': captions}}

#xml to json
def xml_to_json(xml):
    return json.dumps(xmltodict.parse(xml))


def get_audio_from_video(video_path, path_to_save):
  """ get audio from video and save it in the same path with the same name but .wav extension

  Args:
      video_path (str): path to video file
  """

  # Load the video clip
  video_clip = VideoFileClip(video_path)
  # Extract the audio as a new AudioClip
  audio_clip = video_clip.audio
  # Save the audio to a file (optional)
  audio_clip.write_audiofile(path_to_save, codec='pcm_s16le')
  # Close the video and audio clips
  video_clip.close()
  audio_clip.close()
