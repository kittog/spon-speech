#!/bin/python3
# -*- coding: utf-8 -*-

# transcription
import whisper
import time
# audio
import librosa
import soundfile as sf
from pydub import AudioSegment
# texgrid
from praatio import textgrid
from praatio.utilities.constants import Interval
# misc
import re
import os
from pathlib import Path
# arg parser
import click

@click.command()
@click.option("--wav", type=str, help="Path to audio file that needs transcriptions.")
def path_to_audio(wav):
    click.echo(f'Transcribing {wav}...')
    return wav

def main():
    wav = path_to_audio.main(standalone_mode=False)
    # load whisper model
    model = whisper.load_model("medium")
    results = model.transcribe(wav)
    # write transcriptions to textgrid file
    tg = textgrid.Textgrid()
    tier_name = Path(wav).stem
    entries = []
    for seg in results['segments']:
        entries.append((seg['start'], seg['end'], seg['text']))
    intr = textgrid.IntervalTier(name=tier_name, entries=entries)
    tg.addTier(intr)
    tg.save(f"../{tier_name}.TextGrid")

if __name__ == "__main__":
    main()
