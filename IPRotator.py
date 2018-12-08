#Arkam Mazrui 2018
import requests
import re
from bs4 import BeautifulSoup as bs
import numpy as np

class SecretAgent:

    def __init__(self, IP, user_agent):
        self.IP, self.user_agent = IP, user_agent

    def reassign(self, IP, user_agent):
        self.IP, self.user_agent = IP, user_agent

    def get_credentials(self):
        return {"user-agent": self.user_agent}, {"http": "http://" + self.IP, "https": "https://" + self.IP}

class IPRotator:

    def __init__(self):
        r = requests.get("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt")
        self.IPs = r.text.split("\n")
        self.IPs = self.IPs[4:-2]
        self._l = len(self.IPs)
        self.IPs = [re.compile("[a-zA-Z\s]*[-+!]*").sub("", _data) for _data in self.IPs]

        z = requests.get("https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/1")
        page = bs(z.text, 'lxml')
        z = page.find_all("td", attrs={"class":"useragent"})
        self.user_agents = np.array([tag.text for tag in z])
        if len(self.user_agents) < len(self.IPs):
            z = requests.get("https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/2")
            page = bs(z.text, 'lxml')
            z = page.find_all("td", attrs={"class": "useragent"})
            new_agents = [tag.text for tag in z]
            l = abs(len(self.user_agents) - len(self.IPs))
            self.user_agents = np.append(self.user_agents, new_agents[:l])

        self._i = 0

        self.spy = SecretAgent(self.IPs[0], self.user_agents[0])
        print("When using a proxy, your spy's credentials are:\n" + str(self.spy.get_credentials()))

    def next_ip(self):
        if self._i < len(self.IPs):
            self._i += 1
            self.spy.reassign(self.IPs[self._i], self.user_agents[self._i])
            print("Your spy's new credentials are:\n" + str(self.spy.get_credentials()))
            return self.spy
        else:
            return False
