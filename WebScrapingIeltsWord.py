
from bs4 import BeautifulSoup
import pandas as pd
import requests


# the main funciton to retrieve the element and change it to dataframe
def getDataFrameFromSourceText(text):
    soup = BeautifulSoup(text, 'html.parser')

    word_tags = soup.find_all("span", class_="listWordWord")
    words = list(map(lambda tag: tag.get_text()[:-1], word_tags))

    word_type_tags = soup.find_all("span", class_="listWordType")
    word_types = list(map(lambda tag: tag.get_text(), word_type_tags))

    word_explan_tags = soup.find_all("span", class_="listWordExplanation")
    word_explans = list(map(lambda tag: tag.get_text(), word_explan_tags))


    page_df = pd.DataFrame({"word" : words,
                            "type" : word_types,
                            "explanation" : word_explans

    })
    
    return page_df


frames = []
#The num of pages is 17, so we loop 17 times.
for x in range(17):
    #change your url site
    urlpath = 'https://www.examword.com/ielts-list/4000-academic-word-{}?la=en'.format(x+1)
    r = requests.get(urlpath)
    df = getDataFrameFromSourceText(r.text)
    frames.append(df)

result = pd.concat(frames)
result.set_index(["word", "type"])

#output dataframe to csv
#change your csv file path
result.to_csv('/Users/yourfilepath/Documents/data/ielts_words.csv')

