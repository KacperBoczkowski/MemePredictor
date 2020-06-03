import os
import re
import cv2
import pytesseract
import pickle

DANK_MEMES_DIR = 'dankmemes-checked'
REGULAR_MEMES_DIR = 'regularmemes-checked'
ALT_MEMES_DIR = 'newalternative-checked'

def main():
    names_words_dict = dict()
    analyze_memes_in_dir(DANK_MEMES_DIR, names_words_dict)
    analyze_memes_in_dir(REGULAR_MEMES_DIR, names_words_dict)
    analyze_memes_in_dir(ALT_MEMES_DIR, names_words_dict)
    file_handle = open("names_words_dict.pkl", "wb")
    pickle.dump(names_words_dict, file_handle)
    file_handle.close()

def analyze_memes_in_dir(directory, names_words_dict):
    memes = os.scandir(directory)
    for file_name in memes:
        full_path = directory + "/" + file_name.name
        print("Filename: %s" %(full_path))
        meme_text = read_text_from_path(full_path)
        analyze_string(meme_text, full_path, names_words_dict)

def analyze_string(meme_string, full_path, dictionary):
    for line in meme_string.splitlines():
        line = re.sub("[^A-Za-z]+", " ", line) # remove every sign other than A-z
        line = re.sub(r'\b\w{1,3}\b', '', line) # remove every word of length 3 or shorter
        if len(line) != 0 and not line.isspace():
            dictionary[full_path] = line.split()
    if not full_path in dictionary:
        dictionary[full_path] = ""

def read_text_from_path(path):
    image = cv2.imread(path)
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    main()
