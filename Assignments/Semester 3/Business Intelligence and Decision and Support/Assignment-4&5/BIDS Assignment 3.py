
# coding: utf-8

# # 1. Importing Libraries

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set(rc={'figure.figsize':(20,10)})
import datetime
from datetime import datetime
import seaborn as sns
import datetime
now = datetime.datetime.now()
from sklearn.model_selection import train_test_split


# # 2. Loading Data from Postgres and GUI

# In[3]:


df=pd.read_csv('train.csv')


# In[8]:


df.isna().sum()


# In[6]:


df['date'] = df['date'].date


# In[118]:


df.iloc[0]


# In[83]:


item_number=103665
#store_number=     #GUI inputs
#on_promotion=
#date=


# In[84]:


#subset=pd.read_csv('item_108701.csv')
subset=df.loc[df['item_nbr']==item_number]     #Load Data from Postgres according to GUI inputs


# # 3. Data Transformation and combining

# ### 3.1 Holiday Dataset

# In[85]:


holiday=pd.read_csv('holidays_events.csv')
holiday['type'] = pd.factorize(holiday['type'])[0]
holiday['locale'] = pd.factorize(holiday['locale'])[0]  #loading and transforming Holiday dataset
holiday['locale_name'] = pd.factorize(holiday['locale_name'])[0]
holiday['holiday_status']=1
#holiday.drop(['type','locale','locale_name'],inplace=True,axis=1)


# ### 3.2 Stores Dataset

# In[86]:


stores=pd.read_csv('stores.csv')
stores['city']=pd.factorize(stores['city'])[0]
stores['state']=pd.factorize(stores['state'])[0]
stores['type']=pd.factorize(stores['type'])[0]
#stores.drop(['type','state','city'],inplace=True,axis=1)


# ### 3.3 Items Dataset

# In[87]:


items=pd.read_csv('items.csv')
items['family']=pd.factorize(items['family'])[0]


# ### 3.4 Transformation

# In[88]:


subset['onpromotion']=pd.factorize(subset['onpromotion'])[0]
subset.dropna(inplace=True,axis=0,how='any')


# ### 3.5 Converting Date into number of days

# In[89]:


current_year=now.year
current_month=now.month
current_day=now.day


# #### 3.5.1Subset Date to Duration

# In[90]:


subset['date'] = pd.to_datetime(subset['date'], format = '%Y-%m-%d')   #transforming date Column
subset_year = subset['date'].dt.year
subset_month = subset['date'].dt.month
subset_day = subset['date'].dt.day
subset['Duration'] = ((current_year * 365) + (current_month * 30) + current_day) - ((subset_year*365) + (subset_month*30) + subset_day)
subset.drop('date',axis=1,inplace=True)


# #### 3.5.2 Holiday Date to Duration

# In[91]:


holiday['date'] = pd.to_datetime(holiday['date'], format = '%d/%m/%Y')   #transforming date Column
holiday_year = holiday['date'].dt.year
holiday_month = holiday['date'].dt.month
holiday_day = holiday['date'].dt.day
holiday['Duration'] = ((current_year * 365) + (current_month * 30) + current_day) - ((holiday_year*365) + (holiday_month*30) + holiday_day)
holiday.drop('date',axis=1,inplace=True)


# ### 3.6 Joining datasets

# In[92]:


#subset=subset.merge(holiday, left_on='Duration', right_on='Duration', how='left')
#subset=subset.merge(stores, left_on='store_nbr', right_on='store_nbr', how='left')
#subset=subset.merge(items, left_on='item_nbr', right_on='item_nbr', how='left')


# In[93]:


subset.fillna('99',inplace=True)
#subset.drop('Unnamed: 0',axis=1,inplace=True)


# In[94]:


subset


# # 4. Splitting Train and Test dataset

# In[95]:


X_train,X_test,y_train,y_test=train_test_split(subset.drop(['id','unit_sales'],axis=1),subset['unit_sales'],test_size=0.3)


# # 5. Classifiers

# ## 5.2 Random Regressor



from sklearn.ensemble import RandomForestRegressor
lm = RandomForestRegressor(n_estimators=20)
lm.fit(X_train, y_train)
lm_predict = lm.predict(X_test)





from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test,lm_predict))
print('MSE:', metrics.mean_squared_error(y_test, lm_predict))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, lm_predict)))





sns.regplot(x=y_test, y=lm_predict, data=subset)





# ## Predicting output according to GUI input

# In[66]:


subset['minmax_unitsales']=(subset['unit_sales']-subset['unit_sales'].min())/(subset['unit_sales'].max()-subset['unit_sales'].min())


# In[68]:


sns.distplot(subset['minmax_unitsales'])

