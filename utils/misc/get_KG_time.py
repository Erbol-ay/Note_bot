import requests
from bs4 import BeautifulSoup

def get_KG_time():
    # url = "https://www.google.com/search?q=%D0%B2%D1%80%D0%B5%D0%BC%D1%8F+%D0%BA%D1%8B%D1%80%D0%B3%D1%8B%D0%B7%D1%81%D1%82%D0%B0%D0%BD&oq=%D0%B2%D1%80%D0%B5%D0%BC%D1%8F+&aqs=chrome.1.69i57j35i39j0i131i433l3j0i433j0i131i433j69i60.2239j0j7&sourceid=chrome&ie=UTF-8"
    url = "https://www.timeanddate.com/worldclock/kyrgyzstan"
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        }

    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    time_str = soup.find(class_="tzmp_fig_tm")
    time = int(time_str.text[0] + time_str.text[1])

    return time