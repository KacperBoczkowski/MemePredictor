import os
import re
import cv2
import pytesseract

DANK_MEMES_DIR = 'dankmemes-checked'
REGULAR_MEMES_DIR = 'regularmemes-checked'
ALT_MEMES_DIR = 'newalternative-checked'

def main():
    analyze_memes_in_dir(DANK_MEMES_DIR)

def analyze_memes_in_dir(directory):
    memes = os.scandir(directory)
    for file_name in memes:
        full_path = directory + "/" + file_name.name
        print(full_path)
        meme_text = read_text_from_path(full_path)
        analyze_string(meme_text)

def analyze_string(meme_string):
    for line in meme_string.splitlines():
        line = re.sub("[^A-Za-z]+", " ", line) # remove every sign other than A-z
        line = re.sub("  ", "", line)
        line = re.sub("\n", "", line)
        line = re.sub(r'\b\w{1,3}\b', '', line) # remove every word of length 3 or shorter
        print(line)

def read_text_from_path(path):
    image = cv2.imread(path)
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    main()
