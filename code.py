# -*- coding: utf-8 -*-
#卡号
file1=open("文件地址/rd_no","r")
card=[]
for line in file1.readlines():
    words=line.split('\t')
    #tmp2=''.join(tmp)
    card.append(words[1].strip())    
file1.close()

#给出卡号标签，存放到index中  处理之后的标签和原数据粘贴到一起，也可以用dataframe字段拼接实现
file2=open("文件地址/card_all.txt","r")
file3=open("文件地址/index.txt","w")
count1=0
count=0
for line in file2.readlines():
    index=0
    term=line.strip().split('\t')
    tmp=term[0]
    if tmp in card:
        index=1
        count1+=1
    count+=1
    file3.write(str(index)+'\n')
file2.close()
file3.close()

########################计算相关性##########################
import pandas as pd
from scipy.stats import spearmanr
from scipy.stats import f_oneway
from scipy.stats import pearsonr

file4=pd.read_csv("/Users/didi/Desktop/index.txt",sep='\t',encoding='utf-8') 
#（1）获取列名称
file5=open("文件地址/index.txt","r")
col_name=[]
for line in file5.readlines(1):
    words=line.strip().split('\t')
    col_name=words
file5.close()

#data0=file4
#index=[]
#for i in range(1,7498):
#    if file4['借贷标记'][i]=='no data':
#        index.append(i)
#        data0.drop(0,axis=i,inplace=True)

#（2）两个分类型变量 计算斯皮尔曼相关系数
'''
因子化
c = ['A','A','A','B','B','C','C','C','C']
category = pd.Categorical(c)
category.labels
斯皮尔曼相关系数
from scipy.stats import spearmanr
ca=pd.Categorical(file4["卡等级"])
ca1=pd.Categorical(file4["y"])
spearmanr(ca1.codes,ca.codes).correlation
#交叉列联表
pd.crosstab(file4["y"],file4["卡等级"],margins=True)
pd.crosstab(ca1.labels,ca.labels)
'''

cate=['借贷标记','卡等级','卡性质','卡名称','发卡行']

y=pd.Categorical(file4["y"])
for i in cate:
    ca = pd.Categorical(file4[i])
    cor = spearmanr(y.codes,ca.codes).correlation
    pvalue = spearmanr(y.codes,ca.codes).pvalue
    print(i+'\t'+str(cor)+'\t'+str(pvalue))
    
#（3）分类和数值变量  计算f统计量，该统计量越大说明两者相关程度越高

'''
f检验示例，需要删除数据中的null和缺失值
for i in range(7498):
    if file4['得分'][i]=='null':
        file4['得分'][i]=None
d1=file4[file4['y'] == 0]['得分'].dropna()
d2=file4[file4['y'] == 1]['得分'].dropna()
args=[d1,d2]
f,p=f_oneway(*args)
print(f,p)
'''


for item in col_name[2:]:
    if item not in cate:
        for i in range(1,7498):
            target=file4[item][i]
            if str(target) == 'nan' or target == 'null':
                file4[item][i] = None
        d0=file4[file4['y'] == 0][item].dropna()
        d1=file4[file4['y'] == 1][item].dropna()
        args1=[d0,d1]
        f,p=f_oneway(*args1)
        print(item+'\t'+str(f)+'\t'+str(p))

#（4）两个连续变量  计算皮尔逊相关系数
'''
tmp1=[]
tmp2=[]
for i in range(1,7498):
    target=file4['得分'][i]
    if str(target) != 'nan' and target != None:
        tmp1.append(float(file4['y'][i]))
        tmp2.append(float(target))
pearsonr(tmp1,tmp2)
'''

file6=open("/Users/didi/Desktop/corr1.txt","w")
for item in col_name[2:]:
    if item not in cate:
        tmp1=[]
        tmp2=[]
        for i in range(1,7498):
            target=file4[item][i]
            if str(target) != 'nan' and target != None and target != 'null':
                tmp1.append(float(file4['y'][i]))
                tmp2.append(float(target))
        cor=pearsonr(tmp1,tmp2)[0]
        p_value=pearsonr(tmp1,tmp2)[1]                
        file6.write(item+'\t'+str(cor)+'\t'+str(p_value)+'\n')

file6.close()
