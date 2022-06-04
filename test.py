import pandas as pd
from collections import Counter
import numpy as np
import scipy.stats
from scipy.stats import chisquare
import plotly.offline as py
import plotly.graph_objects as go
import csv
#放入所要分析的檔名路徑
data = pd.read_csv('local.csv', encoding = 'ANSI')
#根據想要統計的東西做分類
frequency_count = Counter(data['上課方式'])
f1 = list(frequency_count.keys())
f2 = list(frequency_count.values())
frequency_table = pd.DataFrame(zip(f1,f2),columns=['上課方式','票數'])
frequency_table = frequency_table.sort_values(by = '票數', ascending = False)
ad_name = frequency_table['上課方式'].tolist()
M_1 = data[data['性別']=='我是帥氣的男生'][data['上課方式']==ad_name[0]].shape[0]
M_2 = data[data['上課方式']==ad_name[1]][data['性別']=='我是帥氣的男生'].shape[0]
M_3 = data[data['上課方式']==ad_name[2]][data['性別']=='我是帥氣的男生'].shape[0]
M_4 = data[data['上課方式']==ad_name[3]][data['性別']=='我是帥氣的男生'].shape[0]
list1 = [M_1, M_2, M_3,M_4]
W_1 = data[data['上課方式']==ad_name[0]][data['性別']=='我是漂亮的女生'].shape[0]
W_2 = data[data['上課方式']==ad_name[1]][data['性別']=='我是漂亮的女生'].shape[0]
W_3 = data[data['上課方式']==ad_name[2]][data['性別']=='我是漂亮的女生'].shape[0]
W_4 = data[data['上課方式']==ad_name[3]][data['性別']=='我是漂亮的女生'].shape[0]
#以上都需要改成相應的選項
list2 = [W_1, W_2, W_3,W_4]
#取好你想要的名子
chi_table = pd.DataFrame(zip(list1, list2), columns=['男性', '女性'],index=[ad_name[0], ad_name[1], ad_name[2],ad_name[3]])

obs = np.array([chi_table.iloc[0,:].tolist(), 
                chi_table.iloc[1,:].tolist(),
                chi_table.iloc[2,:].tolist(),
                chi_table.iloc[3,:].tolist(),])
print(obs)
#提取p值
p_value = scipy.stats.chi2_contingency(obs, correction = False)[1]
#print(scipy.stats.chi2_contingency(obs, correction = False))
#print("p_value=",p_value)
#print(chisquare(chi_table.iloc[0,:].tolist())[1])
#print(chisquare(chi_table.iloc[1,:].tolist())[1])
#print(chisquare(chi_table.iloc[2,:].tolist())[1])
#print(chisquare(chi_table.iloc[3,:].tolist())[1])
#繪圖
fig = go.Figure()
# 男性分布圖
fig.add_trace(go.Scatter(
            x= ad_name,
            y= chi_table.iloc[:,0].tolist(),
            mode="lines+markers",
            textfont=dict(
            family="sans serif",
            size=16,
            color="royalblue"),    
            line=dict(color='royalblue', width=2),
            name = '男性'
            ))
# 女性分布圖
fig.add_trace(go.Scatter(
            x= ad_name,
            y= chi_table.iloc[:,1].tolist(),
            mode="lines+markers",
            textfont=dict(
            family="sans serif",
            size=16,
            color="firebrick"),    
            line=dict(color='firebrick', width=2),
            name = '女性'
            ))
fig.update_layout(
    title={
        'text': "<b>(他校)上課方式－性別交叉比較圖</b>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',},
    yaxis_title='票數',
    xaxis={
        'title': '上課方式',
        'tickmode': 'linear'
        },
    width=1800,
    height=960,
    font=dict(
        family="Courier New, monospace",
        size=20,
        color="lightslategrey"
    )
    )
# 產出另存png檔
fig.write_image("其他大學學生比較圖.png")
# 判斷比重
weight = []
boy=[]
girl=[]
for i in range(0,chi_table.shape[0]):
    p = chisquare(chi_table.iloc[i,:].tolist())[1]
    boy.append(scipy.stats.chi2_contingency(obs, correction = False)[3][i][0])
    girl.append(scipy.stats.chi2_contingency(obs, correction = False)[3][i][1])
    if p >= 0.05:
        weight.append('男女喜好程度相似')
    else:
        a = chi_table.iloc[i,0] # 男性消費量
        b = chi_table.iloc[i,1] # 女性消費量
        if a>b:
            weight.append('男性較喜歡')
        else:
            weight.append('女性較喜歡')            
# 將結果存至比較表中
chi_table['男女喜好'] = weight
chi_table['理論值_男']=boy
chi_table['理論值_女']=girl
#print(scipy.stats.chi2_contingency(obs, correction = False)[3][1][1])
chi_table.to_csv("他校上課方式交叉比較表.csv", encoding='ANSI')
file = open('他校上課方式交叉比較表.csv',mode='a', newline='')
writer = csv.writer(file)
writer.writerow(['卡方值',scipy.stats.chi2_contingency(obs, correction = False)[0]])
writer.writerow(['P-value',p_value])
writer.writerow(['自由度',scipy.stats.chi2_contingency(obs, correction = False)[2]])
file.close()
print('OK')
