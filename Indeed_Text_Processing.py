#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import string
from nltk.corpus import stopwords


# In[2]:


df=pd.read_csv(r'C:\Users\deepa\Desktop\MEM\Data Scraping Project\Raw_Extract_4th Aug.csv', index_col=0 )


# Inserting State Row

# In[7]:


def get_state(addr):
    return addr.split(",")[-1][1:3]

state = df['job_location'].apply(get_state)
state


# In[8]:


df.insert(4, column='job_state', value=state)


# Clean Text

# In[15]:


def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return [word.lower() for word in nopunc.split() if word.lower() not in stopwords.words('english')]


# In[16]:


df['job_descriptions'].apply(text_process)


# In[17]:


df.isnull().sum(axis = 0)


# In[23]:


df_clean = df[df.job_descriptions != 'Unknown']


# In[27]:


df_clean.to_csv(r'C:\Users\deepa\Desktop\MEM\Data Scraping Project\Clean Extract 4th Aug.csv')


# NLP

# In[28]:


from sklearn.feature_extraction.text import CountVectorizer


# In[29]:


cv = CountVectorizer(analyzer=text_process )
bow_transformer=cv.fit(df_clean['job_descriptions'])


# In[30]:


#List of vocalulary used
vocab=list(cv.vocabulary_.keys())


# In[31]:


# Print total number of vocab words
print(len(bow_transformer.vocabulary_))


# In[32]:


#Transform the entire DataFrame of descriptions
jd_bow = bow_transformer.transform(df_clean['job_descriptions'])


# In[33]:


from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer().fit(jd_bow)


# In[34]:


jd_tfidf = tfidf_transformer.transform(jd_bow)


# In[35]:


print(jd_tfidf.shape)


# In[41]:


skills = ['sql', 'tableau', 'python', 'excel', 'powerbi', 'r', 'cognos', 'cloud', 'oracle', 'roi', 'security', 'mining',
          'sap', 'kpis', 'kpi', 'sas', 'ssrs', 'reporting', 'rdbms', 'ab', 'warehousing']


# In[37]:


#List of common skills from most trendy to least trendy
skill_idf_val = []
for skill in skills:
    idf_val = tfidf_transformer.idf_[bow_transformer.vocabulary_[skill]]
    skill_idf_val.append(idf_val)

skill_trend = pd.DataFrame({'skills':skills,
'skill_idf_val': skill_idf_val                
})


# In[51]:


skill_trend=skill_trend.sort_values(['skill_idf_val'])


# In[54]:


#Export of common skills
skill_trend.to_csv(r'C:\Users\deepa\Desktop\MEM\Data Scraping Project\Common 4th Aug.csv')


# In[58]:


skill_trend


# In[ ]:





# In[44]:


#List of vocabulary from most used to least used
skill_idf_val = []
for skill in vocab:
    idf_val = tfidf_transformer.idf_[bow_transformer.vocabulary_[skill]]
    skill_idf_val.append(idf_val)

vocab_trend = pd.DataFrame({'vocab':vocab,
'skill_idf_val': skill_idf_val                
})


# In[53]:


vocab_trend=vocab_trend.sort_values(['skill_idf_val'])


# In[59]:


vocab_trend


# In[56]:


#Export of solimatica skills
vocab_trend.to_csv(r'C:\Users\deepa\Desktop\MEM\Data Scraping Project\Vocab 4th Aug.csv')


# In[ ]:




