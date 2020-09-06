'''
this file is mainly used for draft

'''
## libraries
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
## load