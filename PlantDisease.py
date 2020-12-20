import numpy as np
import pickle
import cv2
import datetime
import tkinter
import tkinter.filedialog
from tkinter import *
from tkinter import filedialog
from keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Sequential


f = open( "database.txt" )
lines = iter(f.readlines())
f.close()
default_image_size = tuple((256, 256))


def openFile():
        global filepath
        filepath = filedialog.askopenfilename()
        img = PhotoImage(file=filepath)
        canvas.create_image(30,20, anchor=NW, image=img)
        mainloop()
        
def analyze():
        global desease
        model_pickle = open("C:\\Users\\Admin\\Desktop\\BasicOpenCv\\cnn_model.pkl", 'rb')
        model = pickle.load(model_pickle)
        label_encoder = open("C:\\Users\\Admin\\Desktop\\BasicOpenCv\\label_transform.pkl", 'rb')
        label_transformer = pickle.load(label_encoder)
        imgpath = filepath
        imar = convert_image_to_array(imgpath)
        npimagelist = np.array([imar], dtype=np.float16) / 225.0

        pred = model.predict(npimagelist)
        result = label_transformer.inverse_transform(pred)
        desease = result[0].replace("_"," ")
        print(desease)
        for line in lines:
            line = line.strip()
            if line == desease:
                    topicD.config(text="Desease :")
                    deseaseLabel.config(text=line)
                    topicP.config(text="Plant name :")
                    plantLabel.config(text=next(lines).strip())
                    topicC.config(text="How to treat :")
                    cureLabel.config(text=next(lines).strip())   
                    window.mainloop()         
                    break
        
def convert_image_to_array(image_dir):
          try:
                    image = cv2.imread(image_dir)
                    if image is not None :
                              image = cv2.resize(image, default_image_size)
                              return img_to_array(image)
                    else :
                              return np.array([])
          except Exception as e:
                    print(f"Error : {e}")
                    return None

                
window = Tk()
window.title("Plant Disease")
canvas = Canvas(window, width = 300, height = 300)
canvas.grid(row=2, column=3)
canvas.pack()  
label = Label(text="Choose file location")
label.pack()
button = Button(text="Open" , command=openFile)
button.pack()
button = Button(text="analyze plant" , command=analyze)
button.pack()

topicD = Label()
topicD.pack()
deseaseLabel = Label()
deseaseLabel.pack()
topicP = Label()
topicP.pack()
plantLabel = Label()
plantLabel.pack()
topicC = Label()
topicC.pack()
cureLabel = Label()
cureLabel.pack()

window.mainloop()
