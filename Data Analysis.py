#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# 新用户的下载及购买数据
data1=pd.read_excel(r'C:\Users\23691\AnacondaProjects\DADA_DATE\EXCEL CASE.xlsx',sheet_name='数据1')
# 新用户的标签
data2=pd.read_excel(r'C:\Users\23691\AnacondaProjects\DADA_DATE\EXCEL CASE.xlsx',sheet_name='数据2')
data1.head()


# In[3]:


data2.head()


# install_date:用户下载日期；
# user_id:用户id
# theme:购买页渠道
# storefront_view_time：浏览购买页的时间
# storefront_operation：在购买页的操作
# product_type：购买页对应的商品种类
# storefront_operation_time：在购买页的操作对应时间

# # 第一部分 面试测试题

# ### 1、整体的购买转化率(购买成功的人数/下载人数)

# In[4]:


data1.describe()


# In[5]:


load=data1.groupby(['install_date'])['user_id'].count().reset_index()
success=data1.groupby(['install_date','storefront_operation'])['user_id'].count().unstack().reset_index()
success_load=pd.merge(load,success,on='install_date')
success_load['购买转化率%']=success_load['purchase_success']/ success_load['user_id']*100
success_load


# In[6]:


from pyecharts import Line
line0=Line('购买转化率趋势图','目前4天内转化率相对稳定，且平均值为0.95')
line0.add('转化率%',success_load['install_date'].astype(str),success_load['购买转化率%'],mark_line=['average'],
          xaxis_name='日期',xaxis_pos='right',yaxis_name='单位：%',yaxis_name_gap=35)
line0


# ### 2、渠道的购买转化率

# In[7]:


success_theme=((data1.loc[data1['storefront_operation']=='purchase_success'].groupby(['install_date','theme'])['user_id'].count())
            /data1.groupby(['install_date','theme'])['user_id'].count()*100).unstack().reset_index()
success_theme


# In[8]:


line1=Line('各渠道购买转化率趋势图','Coach的购买转化率最高')
line1.add('Coach',success_theme['install_date'].astype(str),success_theme['Coach'])
line1.add('Data',success_theme['install_date'].astype(str),success_theme['Data'])
line1.add('General',success_theme['install_date'].astype(str),success_theme['General'])
line1.add('Plan',success_theme['install_date'].astype(str),success_theme['Plan'])
line1.add('Tutorial',success_theme['install_date'].astype(str),success_theme['Tutorial'])
line1.add('Video Workout',success_theme['install_date'].astype(str),success_theme['Video Workout'])
line1.add('GPS',success_theme['install_date'].astype(str),success_theme['GPS'],xaxis_name='日期',
          yaxis_name='单位：%',yaxis_name_gap=30,legend_orient='vertical',legend_pos='right') #yaxis_name_pos='end'
line1


# ### 3、用户第二多的标签及该标签用户的购买转化率

# In[9]:


data2.describe()


# ##### 用户第二多的标签

# In[10]:


# 将含有多值的列进行拆分，通过stack（）进行变换，并通过index的设置完成
num1=data2['user_tags'].str.split(',', expand=True).stack()
num2=num1.reset_index(level=1,drop=True).rename('user_tags').reset_index()
tag=num2.groupby(['user_tags'])['index'].count().rename('num').reset_index().sort_values(['num'],ascending=False)
from pyecharts import Bar
bar=Bar('用户标签数量','用户第二多的标签是getFirm')
bar.add('数量',tag['user_tags'].values,tag['num'].values,xaxis_name='标签类型',xaxis_name_pos='end',xaxis_rotate=40)
bar


# #### 用户第二多的标签的转化率

# In[14]:


user_tags=data2.dropna(subset=['user_tags'])
user_data1=pd.merge(user_tags,data1,on=['install_date','user_id'])
user_data1_tage=user_data1['user_tags'].str.split(',', expand=True).stack()
user_data1_tage=user_data1_tage.reset_index(level=1,drop=True).rename('user_tags1').reset_index()
user_data1=user_data1.reset_index()
user_data2=pd.merge(user_data1,user_data1_tage,on=['index'])
getFirm_order=(user_data2.loc[user_data2['user_tags1']=='getFirm']).groupby(['install_date'])['user_id'].count().rename('getFirm_order').reset_index()

user_success_tags=user_data2.loc[user_data2['storefront_operation']=='purchase_success']
getFirm_success=(user_success_tags.loc[user_success_tags['user_tags1']=='getFirm']).groupby(['install_date'])['user_id'].count().rename('getFirm').reset_index()

getFirm=pd.merge(getFirm_success,getFirm_order,on='install_date')
getFirm['转化率']=getFirm['getFirm']/getFirm['getFirm_order']*100
line4=Line('用户第二多标签的转化率')
line4.add('getFirm',getFirm['install_date'].astype(str),getFirm['转化率'].values)
line4


# # 第二部分 开放性问题

# ### 每日浏览量(PV)及访客数量UV

# In[45]:


view=data1.dropna()
visit=view.groupby(['install_date'])['user_id'].count().rename('浏览次数')
UV=view.groupby(['install_date'])['user_id'].nunique().rename('访客数')

number=pd.merge(visit,UV,on='install_date').reset_index()
number['平均浏览次数']=number['浏览次数']/number['访客数'].round(2)
number


# In[48]:


line5=Line('平均浏览次数')
#line5.add('访客数',number['install_date'].astype(str),number['访客数'].values)
#line5.add('浏览次数',number['install_date'].astype(str),number['浏览次数'].values)
line5.add('次数',number['install_date'].astype(str),number['平均浏览次数'].values,xaxis_name='日期')
line5


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### 用户浏览时间段分析

# In[12]:


view_time=data1.dropna()
view_time['hour']=view_time['storefront_view_time'].dt.hour
view_num=view_time.groupby(['hour'])['user_id'].count()
line2=Line('用户浏览时段人数分布','0点-16点，浏览人数逐渐增加，到16点人数达到最大,  此后急速下降')
line2.add('多天总人数',view_num.index,view_num.values,mark_point=['max'],xaxis_name='24小时')


# #### 根据用户浏览时间段使用习惯，进行拉新活动的安排。在一天中14-19点进行优惠券发放等活动

# ### 转化率漏斗分析
#  用户使用APP的流程为下载-->浏览—>购买

# In[93]:


load1=data1.groupby(['install_date'])['user_id'].count().rename('下载人数').reset_index()
view=data1.dropna(subset=['storefront_view_time'])
view_load=view.groupby(['install_date'])['user_id'].count().rename('浏览人数').reset_index()
success_view_load=(view.loc[view['storefront_operation']=='purchase_success']).groupby(['install_date'])['user_id'].count().rename('订单人数').reset_index()
zhuanhua=pd.merge(load1,view_load,on='install_date')
zhuanhua=pd.merge(zhuanhua,success_view_load,on='install_date')
line3=Line('用户使用阶段人数分布(转化率)')
line3.add('下载',zhuanhua['install_date'].astype(str),zhuanhua['下载人数'],is_fill=True,line_opacity=1,area_opacity = 0.1)
line3.add('浏览',zhuanhua['install_date'].astype(str),zhuanhua['浏览人数'],is_fill=True,line_opacity=1,area_opacity = 0.3)
line3.add('订单',zhuanhua['install_date'].astype(str),zhuanhua['订单人数'],is_fill=True,line_opacity=1,area_opacity = 1,
          xaxis_name='日期',yaxis_name='人数',yaxis_name_gap=40)
line3


# In[115]:


zhuanhua1=zhuanhua.apply(lambda x:x['下载人数']/x['下载人数']*100,axis=1).rename('下载').reset_index()
zhuanhua1['浏览']=zhuanhua.apply(lambda x:x['浏览人数']/x['下载人数']*100,axis=1).rename('下载转化率')
zhuanhua1['订单']=zhuanhua.apply(lambda x:x['订单人数']/x['下载人数']*100,axis=1).rename('下载转化率')
avg=zhuanhua1[['浏览','下载','订单']].mean().round(2)
from pyecharts import Funnel
funnel=Funnel('转化率漏斗图','单位：%')
funnel.add('转化率',avg.index, avg.values, 
           is_label_show=True,label_formatter='{b} {c}',label_pos="inside",legend_orient='vertical', legend_pos='right')


# #### 浏览的转化率要明显高于订单的转化率，需要进行个性化的推荐提高用户的订单转化率

# ### 用户喜好度分析
# 根据在购买页的对应商品种类进行计算

# In[14]:


view_product=view.groupby(['product_type'])['user_id'].count().rename('浏览数据').reset_index()
success_view_product=(view.loc[view['storefront_operation']=='purchase_success'])
                      .groupby(['product_type'])['user_id'].count().rename('订单数量').reset_index()
success_product=pd.merge(view_product,success_view_product,on=['product_type'],how='outer')
success_product['订单率']=(success_product['订单数量']/success_product['浏览数据']*100).round(2)

bar1=Bar('商品购买率','用户第二多的标签是getFirm')
bar1.add('购买率',success_product['product_type'].values,success_product['订单率'].values,mark_point=['max'],
         xaxis_name='商品种类',xaxis_name_pos='end',yaxis_name='单位：%',xaxis_rotate=20)
bar1


# ### 不同标签下，购买商品的种类及数量

# In[150]:


bar2=Bar('不同标签下，购买商品的种类及数量','购买成功的标签依次为：loseWeight,getFirm,heartHealth')
bar2.add('lifetime_nonconsumable_2',user_success_product['user_tags1'].values,user_success_product['lifetime_nonconsumable_2'].values,is_stack = True)
bar2.add('monthly_free_trial_ab5',user_success_product['user_tags1'].values,user_success_product['monthly_free_trial_ab5'].values,is_stack = True)
bar2.add('yearly_free_trial_ab4',user_success_product['user_tags1'].values,user_success_product['yearly_free_trial_ab4'].values,is_stack = True)
bar2.add('yearly_not_trial_ab5',user_success_product['user_tags1'].values,user_success_product['yearly_not_trial_ab5'].values,is_stack = True,
        xaxis_name='标签类型',xaxis_name_pos='end',xaxis_rotate=40,legend_pos='right',legend_orient='vertical')


# #### 商品yearly_free_trial_ab4是各标签购买最多的，应该加大对该商品的推荐力度

# In[151]:


#user_tags=data2.dropna(subset=['user_tags'])
#user_data1=pd.merge(user_tags,data1,on=['install_date','user_id'])
#user_data1=user_data1.loc[user_data1['storefront_operation']=='purchase_success']
#user_data1_tage=user_data1['user_tags'].str.split(',', expand=True).stack()
#user_data1_tage=user_data1_tage.reset_index(level=1,drop=True).rename('user_tags1').reset_index()
#user_data1=user_data1.reset_index()
#user_success_tags=pd.merge(user_data1,user_data1_tage,on=['index'])
#user_success_product=user_success_tags.groupby(['user_tags1','product_type'])['user_id'].count().unstack().fillna(0).reset_index()


# ### 用户推荐性分析
# 根据用户的标签进行购买商品的推荐

# In[19]:


user_tags=data2.dropna(subset=['user_tags'])
user_tags_split=user_tags['user_tags'].str.split(',', expand=True).stack().reset_index(level=1,drop=True).rename('user_tags1').reset_index()
user_tags1=user_tags.reset_index()
user2=pd.merge(user_tags_split,user_tags1,on=['index'])
user_rem=user2.groupby(['user_id','user_tags1'])['user_id'].count().unstack()
user_rem=user_rem.fillna(0)
user_rem.head()


# In[ ]:





# In[ ]:




