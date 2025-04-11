from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
import datetime 
import numpy as np
import os
import pandas as pd
import warnings
# 경고창 숨기기
warnings.filterwarnings(action = 'ignore')
# x , y, 데이터 가져오기 
x = pd.DataFrame(np.load('ppp/open/datas/data_6/all_pca_40_x.npy'))
y = pd.read_csv('ppp/open/datas/data_6/all_pca_40_y.csv')["Segment"]

# x,y 가져오기 

#model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=20, random_state = 312,tree_method="hist", device="cuda")#verbosity=2, verbosity

x_file = os.listdir(f'ppp/open/AE_data_01/AE_x/')
y_file = os.listdir(f'ppp/open/AE_data_01/AE_y/')

su=1
print(len( x_file),len( y_file))
for xx, yy in zip(x_file, y_file):
    
    a_x = np.load(f'ppp/open/AE_data_01/AE_x/{xx}')
    a_y = np.load(f'ppp/open/AE_data_01/AE_y/{yy}')
    print(xx)
    print(yy)
    '''
    if su==1:
        
        model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=20, random_state = 312,tree_method="hist", device="cuda",)#verbosity=2, verbosity
    else:
        model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=20, random_state = 312,tree_method="hist", device="cuda",xgb_model=model)#verbosity=2, verbosity
    '''
    if su==1:
        
        model = XGBClassifier(n_estimators=200,
                              learning_rate=0.01,
                              max_depth=10,
                              random_state = 312,
                              tree_method="hist",
                              device="cuda",
                              n_jobs=-1,
                              subsample=0.6,
                              colsample_bytree=0.8,
                              reg_alpha=0.6,
                              )#verbosity=2, verbosity
        model.fit(a_x, a_y)
    else:
        #model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=10, random_state = 312,tree_method="hist", device="cuda")#verbosity=2, verbosity
        model.fit(a_x, a_y,xgb_model=model)
        
    #model.fit(a_x, a_y)
    y_pred = model.predict(x) 
    gp=int(f1_score(y, y_pred,average='macro')*100)
    print(f1_score(y,y_pred, average=None))
    print(confusion_matrix(y,y_pred ))
    
    model.save_model(f"ppp/open/AE_data_01/AE_model/xgb_200_6_all_pca_40_f1_{gp}_op_{su}.model")
    su+=1
    print(f" num : {su}, f1_score : {gp}, time : {datetime.datetime.now()}")
    print()