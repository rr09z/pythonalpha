import pandas as pd
import nltk
from nltk.corpus import stopwords
import string


def remove_noise(input_text):
    noise_list = ['I', 'this', 'it', 'It']
    words = input_text.split()
    noise_free_words = [word for word in words if word not in noise_list]
    noise_free_text = " ".join(noise_free_words)
    return noise_free_text


stopwords.words('english')
data = pd.read_csv('/usr/local/5600/final/googleplay/googleplaystore.csv')
data1 = pd.read_csv('/usr/local/5600/final/googleplay/googleplaystore_user_reviews.csv')
data_app = data[data['App'] == '10 Best Foods for You']
data1_app = data1[data1['App'] == '10 Best Foods for You']
data1_app = data1_app.dropna(axis=0)
data1_app = data1_app.reset_index()
translated_review = data1_app['Translated_Review']
translated_review = translated_review.tolist()

for i in range(len(translated_review)):
    s = translated_review[i]
    s = remove_noise(s)
    for c in string.punctuation:
        s = s.replace(c, "")
    translated_review[i] = s

data1_app['Translated_Review'] = translated_review

a = data1_app['Translated_Review'].str.split()
list1 = []
for i in range(len(a)):
    at = a[i]
    for i in range(len(at)):
        list1.append(at[i])

# a = a.tolist()
freq = nltk.FreqDist(list1)
dic = {}
for key, val in freq.items():
    dic[str(key)] = str(val)
t_dic = [dic]
frequency = pd.DataFrame(t_dic).T

clean_list1 = list1[:]
sr = stopwords.words('english')
for i in clean_list1:
    if i in stopwords.words('english'):
        clean_list1.remove(i)

freq_clean = nltk.FreqDist(clean_list1)
dic_clean = {}
for key, val in freq_clean.items():
    dic_clean[str(key)] = str(val)
t_dic_clean = [dic_clean]
frequency_clean = pd.DataFrame(t_dic_clean).T

st = 'Nothing special! Could find anything useful!'
for c in string.punctuation:
    st = st.replace(c,"")

frequency_clean = frequency_clean.reset_index()
frequency_clean = frequency_clean.rename(columns={0: 'frequency'})
frequency_clean = frequency_clean.rename(columns={'index': 'word'})
frequency_clean['frequency'] = frequency_clean['frequency'].astype(float)
frequency_clean = frequency_clean.sort_values(by='frequency', ascending=False)