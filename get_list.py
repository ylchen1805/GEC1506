import requests, re
from bs4 import BeautifulSoup

en_letter = '[\u0041-\u005a|\u0061-\u007a]+'
zh_char = '[\u4e00-\u9fa5]+'

# Print the Code/代碼 values
def get_code_loc():
    url = "https://curricul.site.nthu.edu.tw/p/406-1208-50862,r8507.php?Lang=zh-tw"

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table that contains the Code/代碼 column
    table = soup.find("table")
    # Extract the Code/代碼 column
    code_column = []
    for row in table.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) > 1:
            code_column.append(columns[0].text.strip())
    ls = []
    for code in code_column:
        ls.append((" ".join(re.findall(en_letter,code))," ".join(re.findall(zh_char,code))))
    return ls

def get_code_course():
    url = "https://curricul.site.nthu.edu.tw/p/406-1208-189767,r8789.php?Lang=zh-tw"

    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table that contains the Code/代碼 column
    table = soup.find("table")

    # Extract the Code ans 開課單位 column
    ls = []
    for row in table.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) > 1:
            ls.append((columns[0].text.strip(),columns[1].text.strip()))
    return ls

if __name__ == "__main__":
    # print(get_code_loc())
    # print(get_code_course())

