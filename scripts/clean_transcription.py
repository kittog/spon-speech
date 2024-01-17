#!/bin/python3
# -*- coding: utf-8 -*-

import click
import re
import glob

def clean_transcription(txt):
    output = open(txt,"w")
    input = open(txt)
    # didascalies
    for line in input:
        txt = re.sub("\[\w+\]", "", line)
        # pauses
        txt = re.sub("\++", "", txt)
        # mmm
        txt = re.sub("(m+h+)", "hm", txt)
        # clitiques
        txt = re.sub("c['] ", "ce", txt)
        txt = re.sub("j['] ", "je", txt)
        txt = re.sub("t['] ", "tu", txt)

    output.write(txt)
    output.close()
    input.close()

@click.command()
@click.option('--folder', type=str, help="Folder with all speakers.")
def path_to_folder(folder):
    click.echo(f"Cleaning transcriptions for all speakers in {folder}")
    return folder

def main():
    folder = path_to_folder.main(standalone_mode=False)
    speakers = glob.glob(folder + "/*")
    speaker_0 = speakers[0]
    print(speaker_0)
    files_0 = glob.glob(speaker_0 + "/*.txt")
    for file in files_0:
        print(file)
        clean_transcription(file)

if __name__ == "__main__":
    main()
