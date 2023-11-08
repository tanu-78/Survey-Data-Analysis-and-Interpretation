#!/usr/bin/env python
# coding: utf-8

# ![image.png](attachment:image.png)

# In[1]:


pip install opendatasets


# In[2]:


import opendatasets as od


# In[3]:


od.download("stackoverflow-developer-survey-2020")


# In[4]:


import pandas as pd 
survey=pd.read_csv("survey_results_public.csv")


# In[8]:


survey


# # Data Preparation and Cleaning

# In[9]:


#with the help of index-col we will be able to set the index according to or given coloumn
#by usingQuestionText we can convert the data frame into simple txt 
survey_ques=pd.read_csv("survey_results_schema.csv",index_col="Column").QuestionText


# In[10]:


survey_ques


# In[11]:


survey_ques.describe()


# In[12]:


survey_ques["YearsCode"]


# In[13]:


selected_coloumn=['Country','Age','Gender','EdLevel','UndergradMajor',
                  'Hobbyist','Age1stCode','YearsCode','YearsCodePro','LanguageWorkedWith',
                 'LanguageDesireNextYear',
                 'NEWLearn',
                 'NEWStuck',
                 'Employment',
                 'DevType',
                 'WorkWeekHrs',
                 'JobSat',
                 'JobFactors',
                 'NEWOvertime']


# In[14]:


len(selected_coloumn)


# In[15]:


s=survey[selected_coloumn].copy()


# In[16]:


s


# In[17]:


schema=survey_ques[selected_coloumn]


# In[18]:


schema


# In[19]:


s.info()


# In[20]:


s.Age1stCode.unique()


# In[21]:


#to change the datatype of rows
s['Age1stCode']=pd.to_numeric(s.Age1stCode,errors='coerce')
s['YearsCode']=pd.to_numeric(s.YearsCode,errors='coerce')
s['YearsCodePro']=pd.to_numeric(s.YearsCodePro,errors='coerce')


# In[22]:


s.info()


# In[23]:


s.describe()


# In[24]:


s.Age.unique()


# In[25]:


s.drop(s[s.Age<10].index,inplace=True)
s.drop(s[s.Age>100].index,inplace=True)


# In[26]:


s.Age.unique()


# In[27]:


s.drop(s[s.WorkWeekHrs<168].index,inplace=True)


# In[28]:


survey_ques.Gender


# In[ ]:





# In[29]:


s.sample(10)


# In[30]:


s['Gender'].value_counts()


# # Exploratory Data Analysis

# In[31]:


import seaborn as sns 
import matplotlib
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style("darkgrid")
matplotlib.rcParams['font.size']=14
matplotlib.rcParams['figure.figsize']=(9,5)


# In[32]:


#unique() gives the unique value 
#nunique() tells about the no of unique values
s.Country.nunique()


# In[33]:


top_countries=s.Country.value_counts().head(10)


# In[34]:


top_countries


# In[35]:


s.Country.value_counts()


# In[36]:


plt.figure(figsize=(8,6))
plt.title("Where do you live")
ax=sns.barplot(top_countries.index,top_countries)
#xticks function helps to rotate the function 
plt.xticks(rotation=80)
for i in ax.containers:
    ax.bar_label(i,)


# In[37]:


s.head(2)


# In[38]:


import numpy as np 
plt.figure(figsize=(5,5))
plt.title("Age")
plt.xlabel("Age")
plt.ylabel ("No of Respondents")
plt.hist(s.Age,bins=np.arange(10,100,5),color='purple')


# In[39]:


s.Gender


# In[40]:


gender_count=s.Gender.value_counts()


# In[41]:


gender_count


# In[42]:


#
plt.figure(figsize=(5,6))
plt.pie(gender_count,labels=gender_count.index,autopct='%1.11f%%')
plt.xticks(rotation=80)


# In[43]:


s.EdLevel


# In[44]:


#to plot the graph in horizontal way we can use y =
ab=sns.countplot(y=s.EdLevel)
#plt.xticks(rotation=80)
plt.figure(figsize=(5,6))
for i in ab.containers:
    ab.bar_label(i,)


# In[45]:


UndergradMajor=s.UndergradMajor.value_counts()*100/s.UndergradMajor.count()


# In[46]:


ag=sns.barplot(UndergradMajor,UndergradMajor.index)
plt.figure(figsize=(5,6))
for i in ag.containers:
    ag.bar_label(i,)


# In[47]:


s.Employment


# In[48]:


#normalize=true set percentage
ak=(s.Employment.value_counts(normalize=True,ascending=True)*100).plot(kind="barh",color='purple')
for i in ak.containers:
    ak.bar_label(i,)


# In[49]:


s.head(2)


# In[54]:


def split_multicolumn(col_series):
    result_df = col_series.to_frame()
    options = []
    # Iterate over the column
    for idx, value  in col_series[col_series.notnull()].iteritems():
        # Break each value into list of options
        for option in value.split(';'):
            # Add the option as a column to result
            if not option in result_df.columns:
                options.append(option)
                result_df[option] = False
            # Mark the value in the option column as True
            result_df.at[idx, option] = True
    return result_df[options]


# In[56]:


language=split_multicolumn(s.LanguageWorkedWith)


# In[57]:


language


# In[77]:


language_percentage=language.mean().sort_values(ascending=False)*100


# In[78]:


language_percentage


# In[80]:


au=sns.barplot(language_percentage,language_percentage.index)
for i in au.containers:
    au.bar_label(i,);


# In[83]:


s.LanguageDesireNextYear


# In[84]:


lang_next=split_multicolumn(s.LanguageDesireNextYear)


# In[85]:


lang_next


# In[91]:


lang_next_percentage=lang_next.mean().sort_values(ascending=False)*100
lang_next_percentage


# In[93]:


ai=sns.barplot(lang_next_percentage,lang_next_percentage.index)
for i in ai.containers:
    ai.bar_label(i,)


# In[94]:


#combining two cases to check which language is most like by students 
lang_loved=language & lang_next 
lang_loved


# In[97]:


lang_loved_percentage=(lang_loved.sum()*100/language.sum()).sort_values(ascending=False)


# In[98]:


lang_loved_percentage


# In[102]:


g=sns.barplot(lang_loved_percentage,lang_loved_percentage.index)
for i in g.containers:
    g.bar_label(i,)


# In[107]:


countries=s.groupby('Country')[['WorkWeekHrs']].mean().sort_values('WorkWeekHrs',ascending=False)
countries


# In[109]:


high_response_country=countries.loc[s.Country.value_counts()>250].head(15)


# In[112]:


high_response_country


# In[117]:


#AGE vs YearsCodePro
s.YearsCodePro


# In[124]:


sns.scatterplot('Age','YearsCodePro',hue='Hobbyist',data=s)
plt.xlabel("Age")
plt.ylabel("YearsCodePro")
plt.title("AGE vs YearsCodePro")


# In[129]:


sns.distplot(s.Age1stCode)
plt.figure(figsize=(3,4))

