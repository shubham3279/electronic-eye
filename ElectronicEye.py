import cv2
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.models import model_from_json

try:
    if K.backend() == 'theano':
        K.set_image_data_format('channels_first')
    else:
        K.set_image_data_format('channels_last')
except AttributeError:
    if K._BACKEND == 'theano':
        K.set_image_dim_ordering('th')
    else:
        K.set_image_dim_ordering('tf') 


json_file = open('model_final.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_final.h5")



def ElelctronicEye(Img):


    img = cv2.imread(Img,cv2.IMREAD_GRAYSCALE)
    #kernel = np.ones((3,3),np.uint8)

    #erosion = cv2.erode(img,kernel,iterations = 3)
    #dilation = cv2.dilate(img,kernel,iterations = 1)
    #img=dilation
    if img is not None:
        #images.append(img)
        img = ~img
        _,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ctrs,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w=int(28)
        h=int(28)
        train_data=[]
        #print(len(cnt))
        rects=[]
        for c in cnt :
            x,y,w,h= cv2.boundingRect(c)
            rect=[x,y,w,h]
            rects.append(rect)
        #print(rects)
        bool_rect=[]
        for r in rects:
            l=[]
            for rec in rects:
                flag=0
                if rec!=r:
                    if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
                        flag=1
                    l.append(flag)
                if rec==r:
                        l.append(0)
            bool_rect.append(l)
        #print(bool_rect)
        dump_rect=[]
        for i in range(0,len(cnt)):
            for j in range(0,len(cnt)):
                if bool_rect[i][j]==1:
                    area1=rects[i][2]*rects[i][3]
                    area2=rects[j][2]*rects[j][3]
                    if(area1==min(area1,area2)):
                        dump_rect.append(rects[i])
        #print(len(dump_rect)) 
        final_rect=[i for i in rects if i not in dump_rect]
        #print(final_rect)
        for r in final_rect:
            x=r[0]
            y=r[1]
            w=r[2]
            h=r[3]
            im_crop =thresh[y:y+h+10,x:x+w+10]
                

            im_resize = cv2.resize(im_crop,(28,28))
            im_resize=np.reshape(im_resize,(1,28,28))
            train_data.append(im_resize)

        components = []
        for i in range(len(train_data)):
            train_data[i]=np.array(train_data[i])
            train_data[i]=train_data[i].reshape(1,28,28,1)
            result = np.argmax(loaded_model.predict(train_data[i]), axis= -1)
            
            if(result[0]==0):
                components.append('Capacitor')
            if(result[0]==1):
                components.append('Diodes')
            if(result[0]==2):
                components.append('Inductor')
            if(result[0]==3):
                components.append('LED')
            if(result[0]==4):
                components.append('Op-Amp')
            if(result[0]==5):
                components.append('Resistor')
            if(result[0]==6):
                components.append('Switch')
            if(result[0]==7):
                components.append('Transformer')
            if(result[0]==8):
                components.append('Transistor')

        components_final = components
    
    return components_final
        
        
        
