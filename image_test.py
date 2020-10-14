'''
this file is mainly used for draft

'''
## libraries

'''
## CV version on hold
import pandas as pd
import cv2

## load the df & images

raw_df = pd.read_csv('../detail.csv')
raw_df.head()
label_df = pd.read_csv('../detail_labels.csv')
label_df.head()

label_img_path = '../Tmall_image'
prod_id = label_df.PROD_ID[0]
im = cv2.imread('{0}/{1}.jpg'.format(label_img_path,prod_id))
cv2.imshow('image', im); cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1)

'''
## image load (PIL version)
import pandas as pd
from PIL import Image
import numpy as np
from skimage.transform import resize
## load the df & images

raw_df = pd.read_csv('../detail.csv')
raw_df.head()
label_df = pd.read_csv('../detail_labels.csv')
label_df.head()

label_img_path = '../Tmall_image'
prod_id = label_df.PROD_ID[0]
im = Image.open('{0}/{1}.jpg'.format(label_img_path,prod_id))

valid_label = ['c','e','g']
valid_prod_list = label_df.loc[label_df['lang'].isin(valid_label),'PROD_ID']

height,width = 500,500

train_data_raw = np.empty(shape=(0,height,width,3))

for prod_id in valid_prod_list:
    im = Image.open('{0}/{1}.jpg'.format(label_img_path,prod_id))
    if im.mode != 'RGB':
        im = im.convert('RGB')
    #print(im.size)
    image_resized = im.resize((width, height),Image.ANTIALIAS)
    #print(image_resized)
    #    data = np.array(image_resized)/255 #归一化？
    temp_data = np.array(image_resized)/255 #归一化？
    temp_data = np.expand_dims(temp_data, axis=0)
    #print(temp_data.shape)
    #train_data_raw.append(temp_data)
    train_data_raw = np.concatenate((train_data_raw,temp_data))

## Keras model test

from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
# encode class values as integers
encoder = LabelEncoder()
encoded_Y = encoder.fit_transform(label_df.loc[label_df['lang'].isin(valid_label),'lang'])
# convert integers to dummy variables (one hot encoding)
train_labels = np_utils.to_categorical(encoded_Y)
print(np.shape(train_labels))

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
model = Sequential()
model.add(Conv2D(10, kernel_size=3, activation='relu'))#,input_shape=(img_rows, img_cols, 1)))
model.add(Flatten())
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy',metrics=['accuracy']) 
#train_data.shape
model.fit(train_data_raw, train_labels, validation_split=0.1, epochs=5)
#model.evaluate(test_data, test_labels, epochs=3)

## test prediction 
test_img_path = '../Aptamil 国产.png'  
test_img = Image.open(test_img_path)
if test_img.mode != 'RGB':
    test_img = test_img.convert('RGB')
#print(im.size)
test_image_resized = test_img.resize((width, height),Image.ANTIALIAS)
#print(image_resized)
#    data = np.array(image_resized)/255 #归一化？
test_data = np.array(test_image_resized)/255 #归一化？
test_data = np.expand_dims(test_data, axis=0)

model.predict(test_data,batch_size = 5)
results = model.predict(test_data)
results = np.argmax(results,axis = 1)
results = pd.Series(results,name="Label")
encoder.inverse_transform(results)