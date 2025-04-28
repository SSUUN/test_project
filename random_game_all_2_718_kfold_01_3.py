
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
import datetime
import time
import os
import gc
import random
random.seed(2025)
#gc.collect()
glo_v=globals().keys()


# x , y , [1, 1, 0.5, 0.5, 0.5] , {0:1500,1:300} , 2025 
def date_selecter(ns,samp,seed):

    #x=np.load("ppp/open/datas/data_31/x_ml_987_no_pca_min_max.npy")
    
    ax=[]
    ay=[] 
    ax_t=[]
    ay_t=[]
    for j in range(6):

        dx=[]
        dy=[]
        dx_t=[]
        dy_t=[]
        # 1 file silec
       
        nx=np.load(f"ppp/open/datas/data_32/x_{j}.npy")
        ny=np.load(f"ppp/open/datas/data_32/y_{j}.npy")
        lens = nx.shape[0]
        print("load_data",lens)
        for i in range(5):
            np.random.seed(seed+i+j)
            
            # class choice
            idx=np.where(ny==i)[0]
            
            idx1=np.random.choice(idx,size=int(len(idx)*(ns[i]*0.8)),replace=False,)
            # time is fucking over so this test_train_split 
            lks=int(len(idx)*(ns[i]*0.2))
            gs=list(set(idx)-set(idx1))
            if len(gs)>=lks:
                lks=len(gs)
            idx2=np.random.choice(gs, size=lks,replace=False,)

            dx.append(nx[idx1])
            dy.append(ny[idx1])

            dx_t.append(nx[idx2])
            dy_t.append(ny[idx2])

        # 1m
        #print(dy.shape,)
        ax.append(np.vstack(dx))
        ay.append(np.hstack(dy))
        ax_t.append(np.vstack(dx_t))
        ay_t.append(np.hstack(dy_t))

    del nx, ny,dx,dy,idx1,idx2
    gc.collect()
    #adasyn = ADASYN(sampling_strategy=samp, random_state=0)  #{0:1500,1:300}
    #x , y= adasyn.fit_resample(np.vstack(ax), np.hstack(ay))
    x=np.vstack(ax)
    y=np.hstack(ay)
    x_te=np.vstack(ax_t)
    y_te=np.hstack(ay_t)
    del ax,ay,ax_t,ay_t
    gc.collect()
    print(x.shape,y.shape,x_te.shape,y_te.shape)
    print(np.unique(y,return_counts=True))
    print(np.unique(y_te,return_counts=True))
    #del ax,ay
    return  x, x_te, y, y_te




    
fkn2=200
fkn=0
sudco=0.8
ffa=1
while True:
    if not os.path.exists(f"ppp/open/models3_5_5_all_{fkn2}"):
        os.mkdir(f"ppp/open/models3_5_5_all_{fkn2}")
    for n4s in [1] :
        for n3s in [1]:
            for n2s in [1]:
                for n1s in [1]:
                    for n0s in [1]:
                        dsd={0:int(906) ,1: int(298)}
                        try:
                            x_tr, x_te, y_tr, y_te = date_selecter([n0s, n1s, n2s, n3s, n4s], dsd, fkn2)

                            x_tr = xgb.DMatrix(x_tr, label=y_tr)
                            x_te = xgb.DMatrix(x_te, label=y_te)
                            watchlist = [(x_tr, 'train'), (x_te, 'eval')]
                            for kima in [6]:
                                for subcol in [sudco]:
                                    params = {
                                            'objective': 'multi:softprob',
                                            'max_delta_step': 1,
                                            'num_class': 5,
                                            'learning_rate': 0.08,
                                            'max_depth': kima,
                                            'random_state': fkn2,
                                            'tree_method': 'gpu_hist',
                                            'predictor': 'gpu_predictor',
                                            'device': 'cuda',
                                            'sub_sample': subcol,
                                            'colsample_bytree': subcol,
                                            'eval_metric': 'mlogloss',
                                            'max_bin':512,
                                            'gamma':0
                                        }
                                    
                                    print(params)
                                    print(datetime.datetime.now())
                                    xgb_model = xgb.train(
                                        params=params,
                                        dtrain=x_tr,
                                        num_boost_round=40000,
                                        evals=watchlist,
                                        early_stopping_rounds=50,
                                        callbacks=[xgb.callback.TrainingCheckPoint(f'ppp/open/models3_5_5_all_{0}', interval=2000)],
                                        verbose_eval=30
                                    )

                                    y_pred = xgb_model.predict(x_te)
                                    y_pred = y_pred.argmax(axis=1)
                                    flflfl=f1_score(y_te,y_pred ,average="macro")
                                    print(f1_score(y_te,y_pred ,average="macro"))
                                    print(f1_score( y_te,y_pred,average=None))
                                    print(confusion_matrix( y_te,y_pred))

                                    pq1=str(n4s)[-1]+str(n3s)[-1]+str(n2s)[-1]+str(n1s)[-1]+str(n0s)[-1]
                                    xgb_model.save_model(f"ppp/open/models3_5_5_all_{100}/xgb_an_{fkn2}_{fkn}_{25}_{pq1}_{kima}_{str(subcol).replace('.','')}_{str(flflfl).replace('.','')[:4]}.model")
                                    # 모델 저장
                                    #models.append(xgb_model)
                                    fkn+=1
                                    
                                    print(datetime.datetime.now(),pq1)
                            fkn2+=100
                            del y_pred,flflfl,x_tr, y_tr, x_te, y_te,xgb_model,pq1,params,watchlist
                            gc.collect()
                            time.sleep(2)
                        except Exception as e:
                            #for gk in globals():
                                #if gk not in glo_v:
                                    #del globals()[gk]
                                    #gc.collect()
                            xgb_model.save_model(f"ppp/open/models3_5_5_all_{fkn2}/modelsError.model")
                            print("ERROR",e)





