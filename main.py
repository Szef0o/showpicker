from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from bs4 import BeautifulSoup
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.list import OneLineListItem
import requests


def boolCheck(platform):
    if platform != []:
        test = True
    else:
        test = False
    return test


def searchbar(searchbar):
    url = "https://www.justwatch.com/pl/search?q="
    text = searchbar
    url = url + text
    # print(url)
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # print(doc.prettify())
    return doc


def showSite(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc


def resultsChoosing(doc):
    # print(doc.prettify())
    titles = doc.find_all("span", class_="header-title")
    titles2 = []
    dates = doc.find_all("span", class_="header-year")
    dates2 = []
    links = doc.find_all("a", class_="title-list-row__column-header")
    buttons = doc.find_all("button", class_="title-list-row__column-header router-link-active poster-link")

    for i in range(len(titles)):
        parent1 = titles[i].parent
        parent2 = parent1.parent
        # print(parent2)
        titles[i] = titles[i].string
        if parent2 not in buttons:
            titles2.append(titles[i])

    for i in range(len(dates)):
        parent1 = dates[i].parent
        parent2 = parent1.parent
        # print(parent2)
        dates[i] = dates[i].string
        if parent2 not in buttons:
            dates2.append(dates[i])

    for i in range(len(links)):
        links[i] = links[i]['href']

    # print(buttons)

    return titles2, dates2, links


def checkStreaming(doc):
    Sky = doc.find_all("img", alt="SkyShowtime")
    Amazon = doc.find_all("img", alt="Amazon Video")
    Amazon2 = doc.find_all("img", alt="Amazon Prime Video")
    Netflix = doc.find_all("img", alt="Netflix")
    Hbo_Max = doc.find_all("img", alt="Max")
    Hulu = doc.find_all("img", alt="Hulu")
    Disney_plus = doc.find_all("img", alt="Hulu")
    Apple_TV = doc.find_all("img", alt="Apple TV")
    return [boolCheck(Sky), boolCheck(Amazon), boolCheck(Amazon2), boolCheck(Netflix), boolCheck(Hbo_Max),
            boolCheck(Hulu), boolCheck(Disney_plus), boolCheck(Apple_TV)]


def takingInfo(doc):
    title = doc.find("h1")
    return title.get_text().strip()


def listServices(list):
    temp = []
    for i in range(len(list)):
        if list[i] == True:
            temp.append(i)
    # print(temp)
    return temp


def sortingServices(list):
    temp = []
    for i in list:
        if i == 0:
            temp.append("Sky Showtime")
        elif i == 1:
            temp.append("Amazon Video")
        elif i == 2:
            temp.append("Amazon Prime Video")
        elif i == 3:
            temp.append("Netflix")
        elif i == 4:
            temp.append("HBO Max")
        elif i == 5:
            temp.append("Hulu")
        elif i == 6:
            temp.append("Disney Plus")
        elif i == 7:
            temp.append("Apple TV")
    # print(temp)
    return temp



def stringCheck(string):
    x = " " in string
    if x:
        string = string.replace(" ", "-")

    return string


def reverseStringCheck(string):
    return string.capitalize()


class MainWindowMovie(Screen):
    searchbar = ObjectProperty(None)
    searchbar2 = StringProperty("")

    def searchbarResults(self):
        self.searchbar2 = self.searchbar.text
        self.searchbar.text = ""


class SearchResultsMovie(Screen):
    labeltext = StringProperty("")

    def on_pre_enter(self, *args):
        self.takeSearchResults()

    def takeSearchResults(self):
        ref = self.manager.get_screen("search")
        text = stringCheck(ref.ids.improvlabel.text)
        doc = searchbar(text)
        titles, dates, links = resultsChoosing(doc)
        self.ids.label.text = reverseStringCheck(ref.ids.improvlabel.text)
        for i in range(len(titles)):
            self.ids.container.add_widget(
                OneLineListItem(text=titles[i] + " " + dates[i], on_press=lambda x,
                                value_for_pass=links[i]: self.changeLabel(value_for_pass))
            )

    def changeLabel(self, text):
        self.labeltext = str("https://www.justwatch.com" + text)
        # print(self.labeltext)

    def on_leave(self, *args):
        self.ids.container.clear_widgets()


class ShowResults(Screen):

    def on_pre_enter(self, *args):
        self.showSearchResults()

    def showSearchResults(self):
        ref = self.manager.get_screen("choose")
        text = ref.ids.improvlabel.text
        doc = showSite(text)
        info = takingInfo(doc)
        lista = listServices(checkStreaming(doc))
        services = sortingServices(lista)
        self.ids.label.text = info
        for i in range(len(services)):
            self.ids.container.add_widget(
                OneLineAvatarListItem(text=services[i])
            )

    def on_leave(self, *args):
        self.ids.container.clear_widgets()


class WindowManager(ScreenManager):
    pass


class MainApp(MDApp):
    def __init__(self):
        super().__init__()
        self.kv = Builder.load_file("main.kv")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.kv
    pass


if __name__ == "__main__":
    MainApp().run()

