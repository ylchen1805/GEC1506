import pandas as pd
import requests
import os
import re

url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/OPENDATA/open_course_data.json'
response = requests.get(url)

with open('cur.json', 'wb') as file:
    file.write(response.content)
    file.close()

df = pd.read_json('cur.json')
os.remove("cur.json")


# extract the English characters until encountered Chinese characters
def extract_english_until_chinese(input_string):
    pattern = r'[^\u4e00-\u9fff]+'

    match = re.search(pattern, input_string)
    if match:
        english_part = match.group(0)
        return english_part.strip()
    else:
        return ""

# extract all the English characters


def extract_all_letters(input_string):
    pattern = r'[a-zA-Z]+'
    matches = re.findall(pattern, input_string)
    return ''.join(matches)

def get_list_location():
    return

def select(target: dict = {}, strict: bool = False):
    '''
        target: {
            "time":[] (ex. ["F1", "F5"])
            "loc" :[] (ex. ["GEN ll", "HSS"]) 
            "dep" :[] (ex. ["AES", "CS", "EE"])
        }

        strict : strict selection for time 

    return value type : pandas.DataFrame
    '''

    series_ls = []
    for _, item in df.iterrows():
        flag1 = False  # for time
        flag2 = False  # for location
        flag3 = False  # for department

        for key in target.keys():
            for condi in target[key]:
                if key == "time" and not strict:
                    if not pd.isnull(item['教室與上課時間']):
                        if condi in item["教室與上課時間"]:
                            flag1 = True
                elif key == "loc":
                    if not pd.isnull(item['教室與上課時間']):
                        result = extract_english_until_chinese(item['教室與上課時間'])
                        if condi == result:
                            flag2 = True
                else:
                    result = extract_all_letters(item['科號'])
                    if condi == result:
                        flag3 = True

        if strict and 'time' in target.keys():
            if not pd.isnull(item['教室與上課時間']):

                split_segment = item['教室與上課時間'].rsplit('\t', 1)
                last_segment = split_segment[-1]
                slicePairs = [last_segment[i:i+2]
                              for i in range(0, len(last_segment), 2)]

                matchAll = True
                for p in slicePairs:
                    if p == '\n':
                        continue
                    if p not in target['time']:
                        matchAll = False

                flag1 = True if (matchAll and slicePairs) else False

        flag1 = True if 'time' not in target.keys() else flag1
        flag2 = True if 'loc' not in target.keys() else flag2
        flag3 = True if 'dep' not in target.keys() else flag3

        if flag1 and flag2 and flag3:
            series_ls.append(item)

    return pd.DataFrame(series_ls)


if __name__ == "__main__":
    temp = select({"time": ["F3", "F4", "M1"], "loc": [
                  "GEN II", "ENG I"], "dep": ["MATH"]})
    temp.to_csv("./out1.csv")

    temp = select({"time": ["M3", "T4", "M1"]})
    temp.to_csv("./out2.csv")

    temp = select({"time": ["Ma", "Mb", "Mc"], "loc": ["GEN II", "ENG I"]})
    temp.to_csv("./out3.csv")

    temp = select({"time": ["M3", "M4", "W2"],
                  "loc": ["DELTA"], "dep": ["CS"]}, strict=True)
    temp.to_csv("./out4.csv")

    temp = select({"time": ["M3", "M4", "W2"],
                   "loc": ["DELTA"], "dep": ["CS", "EE"]}, strict=True)
    temp.to_csv("./out5.csv")

    temp = select({"time": ["T3", "T4", "R4"],
                  "dep": ["MATH"]}, strict=True)
    temp.to_csv("./out6.csv")

    temp = select({"time": ["Ma", "Mb", "Mc"], "loc": [
                  "GEN II", "ENG I"]}, strict=True)
    temp.to_csv("./out7.csv")

    temp = select({"time": ["T3", "T4", "R3", "R4"],
                  "dep": ['CHE']}, strict=True)
    temp.to_csv("./out8.csv")

    temp = select({"time": ["T3", "T4", "R3", "R4"],
                  "dep": ['CHEM']}, strict=True)
    temp.to_csv('./out9.csv')

    temp = select({"time": ["T3", "T4", "R3", "R4"],
                  "dep": ['CHE', 'CHEM']}, strict=True)
    temp.to_csv('./out10.csv')
