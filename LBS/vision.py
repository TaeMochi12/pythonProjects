import cv2
import os
import io
import numpy as np
from google.cloud import vision  # cloud api
from google.cloud import translate_v2  # cloud api
import tkinter as tk
from tkinter import filedialog
from google.cloud import texttospeech_v1  # cloud api
from deep_translator import GoogleTranslator
from langdetect import detect
from mutagen.mp3 import MP3


def deskew(cvImage):  # takes an opencv image as input
    image = cvImage.copy()  # creating a copy of the image
    # converting the image into grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)  # inverting the grayscale image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[
        1]  # binary image
    coords = np.column_stack(np.where(thresh > 0))
    # finding the angle of rotation to deskew the image
    angle = cv2.minAreaRect(coords)[-1]
    if angle > 45:
        angle = 90-angle
    elif angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    # applying the rotation using a rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated  # returning the deskewed image as a numpy array


# sharpening image using image smoothening by gaussian blur and the pixels are fixed accordingly
def noise_removal(image):
    blur = cv2.GaussianBlur(image, (0, 0), sigmaX=33, sigmaY=33)
    divide = cv2.divide(image, blur, scale=255)
    output_gaus = cv2.GaussianBlur(divide, (5, 5), 0)
    sharpened = cv2.addWeighted(image, 1.5, output_gaus, -0.5, 0)
    return sharpened


def langs():

    # reads the language support file by opening it
    lang_file = open("language_support.txt", "r")

    # takes the target language as input from user
    target_language = input("enter the name of language(like: Hindi): ")
    str = " "
    while (str):  # searches the entered language in file
        str = lang_file.readline()
        l = str.split()
        if target_language in l:
            return l[len(l)-1]


def openfile():
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_json_file/translator-346404-9fadb5fe6cc1.json'#cloud vision
    client = vision.ImageAnnotatorClient()

    extensions = ("*.jpg", "*.png", "*.jpeg")  # extensions of the image
    filepath = filedialog.askopenfilename(title="Choose The Image", filetypes=(  # opens a file dialog to let the user select the image of one of above extnsns
        ("images", extensions), ("all files", "*.*")))

    # joins the file path with the selected file
    file_path = os.path.join(filepath)

    with io.open(file_path, 'rb') as image_file:  # and read the contents of file
        content = image_file.read()

    # creates a vision.Image object from the contents of the selected file
    image = vision.Image(content=content)
    # passing image to google api's document_text_detection method to extract text
    response = client.document_text_detection(image=image)

    Text = response.full_text_annotation.text
    print(Text)  # printing the extracted text on console
    # using langdetect library to detect the language of extracted text
    souce_lang = detect(Text)

    # translate

    # using opencv library to read the selected file
    file = cv2.imread(filepath)
    new_img = deskew(file)  # deskewing the selected image file
    new_img = cv2.bitwise_not(new_img)
    # image processing ------
    noise = noise_removal(new_img)  # removing noise

    height = noise.shape[0]  # resizing the image
    width = noise.shape[1]
    if height > 1000 or width > 1000:
        height = 400
        width = 400
        dsize = (width, height)
        output = cv2.resize(noise, dsize)
    else:
        height = height+int((noise.shape[0]/100)*30)
        width = width+int((noise.shape[1]/100)*30)
        dsize = (width, height)
        output = cv2.resize(noise, dsize)
    # displaying the processed image in a new window
    cv2.imshow("image", output)

    target_lang = langs()  # prompts the user to select target lang
    translated_text = GoogleTranslator(  # using googletranslator method of deep translator library we translate the extracted text into target lang
        source=souce_lang, target=target_lang).translate(text=Text)
    print(translated_text)  # printing the translated text on console

    # text to Speech
    # initializing a texttospeech client to interact with the API
    client_1 = texttospeech_v1.TextToSpeechClient()
    # result is synthesisinput object..text to be synthesised is stored in translated_text
    result = texttospeech_v1.SynthesisInput(text=translated_text)

    voice1 = texttospeech_v1.VoiceSelectionParams(  # voice1 is voiceselectionparams obj..specifies the lang and gender of voice
        language_code=target_lang,
        ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech_v1.AudioConfig(  # specifies the encoding of the audio file
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )
    response = client_1.synthesize_speech(  # it sends a request to the api to synthesize the text
        input=result,
        voice=voice1,
        audio_config=audio_config
    )

    # it opens a file called temporary.mp3 and stores the synthesized speech content into it
    with open('audio/Temporary.mp3', 'wb') as output1:
        output1.write(response.audio_content)

    os.system("start audio/Temporary.mp3")  # it plays the audio
    # while(True):
    key = input("enter the key q: ")
    if key == 'q':
        os.remove("audio/Temporary.mp3")
        # if we press q then we can store the audio in the desired named audio file
        name = input("enter the audio file name: ")
        with open('audio/'+name+'.mp3', 'wb') as output1:
            output1.write(response.audio_content)
            # break
    else:  # otherwise the audio file gets deleted
        os.remove("audio/Temporary.mp3")
        # break


root = tk.Tk()  # to trigger the opening of file dialog window
root.withdraw()
openfile()
