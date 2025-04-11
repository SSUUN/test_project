import pandas as pd
import os
#import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
import numpy as np
#plt.rcParams['font.family'] ='Malgun Gothic'
#plt.rcParams['axes.unicode_minus'] =False
import datetime 
print(datetime.datetime.now())


path1=os.listdir("ppp/open/train/")
data=1

aaa=0
for j in path1:    
    a=os.listdir(f"ppp/open/train/{j}")
    p=[]
    
    pp=[]
    for i in a[:1]:
        p=pd.read_parquet(f"ppp/open/train/{j}/{i}").drop("기준년월",axis=1)
        data=pd.merge(data,p,on="ID",how="inner") if j!="1.회원정보" else p
        
        print(len(data.columns))
del p

idx=data[data["Segment"].apply(lambda x: x=="A" or x=="B")].index
#idx=data[data["Segment"].apply(lambda x: x!="E")].index
idx2=data[data["Segment"].apply(lambda x: x=="E" )].index
idx2=np.random.choice(idx2,size=320342,replace=False,)
idx3=data[data["Segment"].apply(lambda x: x=="D" )].index
idx3=np.random.choice(idx3,size=58207,replace=False)
idx4=data[data["Segment"].apply(lambda x: x=="C" )].index
idx4=np.random.choice(idx4,size=21265,replace=False)
idx=np.concatenate([idx,idx2,idx3,idx4])
data=data.iloc[idx]
print(len(idx))
path1=os.listdir("ppp/open/train/")
#data=1
data2=10
aaa=0
for j in path1:    
    a=os.listdir(f"ppp/open/train/{j}")
    p=[]
    
    pp=[]
    for i in a:
        
        p=(pd.read_parquet(f"ppp/open/train/{j}/{i}").drop("기준년월",axis=1))
        p=p.iloc[idx]
        #print(len(p))
        pp.append(p)
    #print(len(pd.concat(pp).columns))
    #pd.concat(pp)
    data2=pd.concat([data2,pd.concat(pp).drop("ID",axis=1)],axis=1) if aaa==1 else pd.concat(pp)
    print(len(data2.columns))
    aaa=1
    pp=[]
    #print(len(data2))
    #print(i,j)  
del p 
del pp
del idx,idx2,idx3,idx4
data=pd.concat([data,data2],ignore_index=True)
del data2
print(data["Segment"].value_counts())
print(datetime.datetime.now())

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.decomposition import PCA

#data["Segment"]=data["Segment"].apply(lambda x: 1 if x=="B" else 0)
led={}
for i in data.columns:
    le = LabelEncoder()
    if data[i].dtype=='O':
        data[i]=le.fit_transform(data[i])
        led[i]=le


y=data["Segment"]
x=data.drop(["ID","Segment"],axis=1)

#x=x.fillna(method="mean",axis=1)

fid=x.mean()
x = x.fillna(x.mean())
        
del data

pca = PCA(n_components=40)
x = pd.DataFrame(pca.fit_transform(x))
mi=x.min()
ma=x.max()
x=((x-mi)/(ma-mi))
x=x.fillna(0)
print(datetime.datetime.now())

import os
import pickle

num=max(list(map(lambda x: int(x.split("_")[-1]),os.listdir("ppp/open/datas"))))+1
os.mkdir(f'ppp/open/datas/data_{num}')

np.save(f'ppp/open/datas/data_{num}/all_pca_40_x', x)
y.to_csv(f"ppp/open/datas/data_{num}/all_pca_40_y.csv",encoding="utf-8-sig",index=False)
fid.to_csv(f"ppp/open/datas/data_{num}/all_pca_40_fid.csv",encoding="utf-8-sig",index=False)

mi.to_csv(f"ppp/open/datas/data_{num}/all_mi.csv",encoding="utf-8-sig",index=False)
ma.to_csv(f"ppp/open/datas/data_{num}/all_ma.csv",encoding="utf-8-sig",index=False)


for i,j in zip(["encoder","pca"],[led,pca]):
    with open(f"ppp/open/datas/data_{num}/all_{i}.pickle","wb") as fw:
        pickle.dump(j,fw)
        
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
tf.random.set_seed(2025)
np.random.seed(2025)
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import time
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix

'''
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:  # gpu가 있다면, 용량 한도를 5GB로 설정
  tf.config.experimental.set_virtual_device_configuration(gpus[0], 
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=6*1024)])
'''
# 오토인코더 모델 정의
max_len=len(y[y==4])
def build_autoencoder(input_dim):
    input_layer = layers.Input(shape=(input_dim,))
    
    # 인코더
    encoded = layers.Dense(1024, activation='relu')(input_layer)
    encoded = layers.Dense(512, activation='relu')(encoded)
    encoded = layers.Dense(256, activation='relu')(encoded)
    latent_space = layers.Dense(200, activation='relu')(encoded)  # 잠재 공간 벡터
    
    # 디코더
    decoded = layers.Dense(256, activation='relu')(latent_space)
    decoded = layers.Dense(512, activation='relu')(decoded)
    decoded = layers.Dense(1024, activation='relu')(decoded)
    output_layer = layers.Dense(input_dim, activation='sigmoid')(decoded)  # 원본 차원으로 복원
    
    autoencoder = models.Model(input_layer, output_layer)
    encoder = models.Model(input_layer, latent_space)  # 인코더 부분만 별도 모델로
    
    autoencoder.compile(optimizer='adam', loss='mse')  
    
    return autoencoder, encoder

xaep=[]
yaep=[]
# 모델 빌드
for i in range(5):
    
    xxx=x.loc[y[y==i].index]#[:10000]
    ep=[60,100,5,4,2][i]
    bh=[20,16,64,128,256][i]
    kj=max_len+int(max_len*0.1)
    nn=kj-len(xxx)
    #nn=100000
    #ep=[100,100,100,100,100][i]
    #bh=[8,8,8,8,8][i]
    #ep=10
    input_dim = xxx.shape[1]  # 데이터의 열 수
    autoencoder, encoder = build_autoencoder(input_dim)


    # 예시로 랜덤 데이터를 생성 (실제 데이터로 교체해야 함)
    
    

    X_train = xxx.values  

    # 오토인코더 학습
    autoencoder.fit(X_train, X_train, epochs=ep, batch_size=bh)
    # 잠재 공간에서 샘플링
    latent_vectors = encoder.predict(X_train,batch_size=64)

    # 약간의 노이즈를 추가하여 새로운 샘플 생성
    '''
    def generate_new_samples(latent_vectors, num_samples):
        noise_factor = 0.1
        if i==0:
            noise_factor=0.08
        elif i==2:
            noise_factor=0.05
        elif i==3:
            noise_factor=0.08
            
        new_latent_vectors = []
        for _ in range(num_samples):
            noise = np.random.normal(0, noise_factor, latent_vectors.shape[1])
            new_latent_vector = latent_vectors[np.random.choice(latent_vectors.shape[0])] + noise
            new_latent_vectors.append(new_latent_vector)
        new_latent_vectors = np.array(new_latent_vectors)
        
        return new_latent_vectors
    new_latent_vectors=generate_new_samples(latent_vectors,nn)
    
    
     # 약간의 노이즈를 추가하여 새로운 샘플 생성
    '''
    def generate_new_samples(latent_vectors, num_samples):
        
        noise_factor = 0.1
        if i==0:
            noise_factor=0.11
        elif i==1:
            noise_factor=0.11
        elif i==2:
            noise_factor=0.11    
        elif i==3:
            noise_factor=0.11
        elif i==4:
            noise_factor=0.1

        
        noise = np.random.normal(0, noise_factor, (num_samples,latent_vectors.shape[1]))
        new_latent_vectors = latent_vectors[np.random.choice(latent_vectors.shape[0], num_samples)]+noise
        
        return new_latent_vectors
    
    new_latent_vectors=generate_new_samples(latent_vectors,nn)
    # 디코더 부분만 따로 모델로 정의

    decoder_input = layers.Input(shape=(200,))  
    decoder_layer = autoencoder.layers[-4](decoder_input)
    decoder_layer = autoencoder.layers[-3](decoder_layer)  
    decoder_layer = autoencoder.layers[-2](decoder_layer)  
    decoder_layer = autoencoder.layers[-1](decoder_layer)  
    decoder = models.Model(decoder_input, decoder_layer)

    # 잠재 벡터로부터 복원된 데이터 생성
    augmented_data = decoder.predict(new_latent_vectors,batch_size=64)

    # 중복된 데이터 제거
    augmented_data_unique = np.unique(augmented_data, axis=0)  # 중복 제거
    print(augmented_data_unique.shape)
    xaep.append(augmented_data_unique)
    yaep+=[i]*nn

    
    
print(datetime.datetime.now())

tr=np.vstack(xaep)#.shape
np.save(f'ppp/open/datas/data_{num}/all_pca_40_AE_x', tr)
np.save(f'ppp/open/datas/data_{num}/all_pca_40_AE_y', np.array(yaep))
x123=np.vstack([x.values,tr])
y123=np.concatenate([y.values,np.array(yaep)])
del x,y,tr,yaep,xaep


model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=20, random_state = 312,tree_method="hist", device="cuda",verbosity=2 ,)#verbose = True, verbosity

# 모델 학습
#model.fit(x1, y1)
#model.fit(tr, yaep)
model.fit(x123, y123)


#y_pred = model.predict(x_te) 
print(datetime.datetime.now())

model.save_model(f"ppp/open/datas/data_{num}/xgb_200_20_011_all_pca_40_f1_op.model")

#print(f1_score(y_pred, y_te,average="macro"))
#print(f1_score(y_te,y_pred, average=None))
#print(confusion_matrix(y_te,y_pred ))
# 35 minutes

import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


path1=os.listdir("ppp/open/test/")
data=1
for j in path1:
    
    a=os.listdir(f"ppp/open/test/{j}")
    p=[]
    
    for i in a[:1]:
        p=pd.read_parquet(f"ppp/open/test/{j}/{i}").drop("기준년월",axis=1)
        data=pd.merge(data,p,on="ID",how="inner") if j!="1.회원정보" else p
        
        print(j,i)
    



from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.decomposition import PCA

#data["Segment"]=data["Segment"].apply(lambda x: 1 if x=="B" else 0)
#led={}
for i in data.columns:
    if data[i].dtype=='O':
        if i=="ID":
            continue
        data[i]=led[i].transform(data[i])


#y=data["Segment"]
x=data.drop(["ID"],axis=1)

#x=x.fillna(method="mean",axis=1)
x=x.fillna(fid)
#x=x.fillna(x.mean())#
        
#pca = PCA(n_components=40)
x = pd.DataFrame(pca.transform(x))
#mi=x.min()
#ma=x.max()
x=((x-mi)/(ma-mi))
x=x.fillna(0)

pred=model.predict(x)

print(np.unique(pred,return_counts=True))


p1=pd.read_csv("ppp/open/sample_submission.csv")
p1
val=dict(zip((0,1,2,3,4),list("ABCDE")))
p1["Segment"]=pred
p1["Segment"]=p1["Segment"].apply(lambda x:val[x])

p1.to_csv("ppp/open/sample_submission_pca40_all_xgb_200_op.csv",index=False,encoding="utf-8-sig")
print(datetime.datetime.now())

