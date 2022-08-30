import re
from collections import Counter
import emoji
import numpy
import names
import pandas as pd
from matplotlib import pyplot
from wordcloud import WordCloud, STOPWORDS

df = pd.read_json('ChatExport_2022-08-30/result.json', dtype={'from_id': str})

df = pd.json_normalize(df['messages'])
df = df[(df.id != 'nan') & (df.text != '') & (df.type == 'message')]  # This is a telegram service, likely updates
df['text'] = df['text'].apply(lambda x: ' '.join([i['text']  if type(i) == dict else i for i in x]) if type(x) == list else x)
# %%
df[['type', 'from']].groupby(['from']).count().sort_values(['type'], ascending=False)

# %%
df[['type', 'from']].groupby(['from']).count().sort_values(['type'], ascending=False)


# %%

def get_words_count(row):
    message = row.text
    emojis = ""
    # Telegram may save some messages as json
    if message is None or type(message) != str:
        return None
    return re.sub("[^\w]", " ", message).split().__len__()


df["word_count"] = df[["text"]].apply(get_words_count, axis=1)
# %%
df[['word_count', 'from']].groupby(['from']).sum().sort_values(['word_count'], ascending=False)
# %%
people = list(df['from'].unique())
people.remove('Rose')
people.remove('Werewolf Moderator [☮]')
people.remove('Otomessagesender')
people.remove('RandomGod')
people.remove('Yandex.Translate')
people.remove('Deezer Music')
people.remove(None)
people.remove('Combot')
from collections import Counter
from pprint import pprint
for name in people:
    user_df = df[df["from"] == name]
    words_per_message = numpy.sum(user_df['word_count'])
    print('stats for ', name)
    print(name, ' sent  ', int(words_per_message), ' words, average ', words_per_message / user_df.shape[0], ' per message')

    words = ' '.join(user_df['text'].values).replace('I','ı').replace('İ', 'i').lower().split()

    a = Counter(words).most_common(50)
    print(f'Most common words for {name} \n')
    for idx , (i,c) in enumerate(dict(a).items()):
        print(i , '  :  ', c , '  percentage: ', c * 100 / len(words)  )




    print(10 * '\n')



# %%
import trstop

# %%


# %%
text_df = df.text.dropna()
text = " ".join(review for review in df.text.dropna() if review is not None and type(review) == str)
print("There are {} words in all the messages.".format(len(text)))

stopwords = set(trstop.dictionary.keys())
stopwords.update(
    ['Kanka', 'Hee', 'knk'])
# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
# Display the generated image:
pyplot.figure(figsize=(10, 5))
pyplot.imshow(wordcloud, interpolation='bilinear')
pyplot.axis("off")
pyplot.show()
#%%
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.express as px
df["datetime"] = pd.to_datetime(df['date'])

def dayofweek(i):
  l = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  return l[i];
day_df=pd.DataFrame(df["word_count"])
day_df['day_of_date'] = df['datetime'].dt.weekday
day_df['day_of_date'] = day_df["day_of_date"].apply(dayofweek)
day_df["messagecount"] = 1
day = day_df.groupby("day_of_date").sum()
day.reset_index(inplace=True)

fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
fig.update_traces(fill='toself')
fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True
    )),
  showlegend=False
)
fig.show()
