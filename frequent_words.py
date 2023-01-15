import os
import re
from collections import Counter
from nltk.corpus import stopwords

current_directory = os.path.dirname(os.path.realpath(__file__))

path = current_directory + '/extra_de_subtitles'



stopwords = set(stopwords.words('english'))

def get_frequent_words(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
        # remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        #remove all numbers
        text = re.sub(r'\d+', '', text)
        # convert to lowercase
        text = text.lower()
        words = text.split()
        # remove two letter words and english stopwords
        words = [word for word in words if (len(word) > 2) and (word not in stopwords)]

        return Counter(words).most_common(500)

for file_name in os.listdir(path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(path, file_name)
        for word, count in get_frequent_words(file_path):

            print(word)

words = get_frequent_words(file_path)
#save words to a text file
with open('frequent_words.txt', 'w') as f:
    for word, count in words:
        f.write(word+"\n" )
