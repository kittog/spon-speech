import whisper
import time
import librosa
import soundfile as sf
import re
import os
import click
import tgt

def write_textgrid():
    pass

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
    tg = tgt.TextGrid()


if __name__ == "__main__":
    main()
