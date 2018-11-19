import requests
import random
from bs4 import BeautifulSoup
import os
import argparse


class Checker:

    def __init__(self, target):
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        for i in range(6):
            sa.append(random.choice(seed))
        user = ''.join(sa)
        self.target = target
        self.username = user
        self.password = 'taro'
        self.new = 'change'
        self.score = 0
        self.check = requests.session()
        self.img = self.username + ".jpeg"
        for files in os.listdir():
            if str(files).endswith('.jpeg'):
                os.rename(files, self.img)

    def register(self):
        register_url = self.target + "register.php"
        data = {'username': self.username, 'password': self.password}
        self.check.post(register_url, data)

    def login(self):
        login_url = self.target + "login.php"
        data = {'username': self.username, 'password': self.password}
        with self.check.post(login_url, data) as r:
            if "欢迎来到secshop" in r.text and "退出" in r.text:
                self.score = self.score + 35
                print("注册、登陆功能完成 当前分数 " + str(self.score))

    def change(self):
        change_url = self.target + "change.php"
        data = {'old': self.password, 'new': self.new}
        self.check.post(change_url, data)

        with requests.session() as session:
            login_url = self.target + "login.php"
            data = {'username': self.username, 'password': self.new}
            with session.post(login_url, data) as r:
                if "欢迎来到secshop" in r.text and "退出" in r.text:
                    self.score = self.score + 15
                    print("重置密码功能完成 当前分数" + str(self.score))

    def list(self):
        list_url = self.target + "list.php"
        with self.check.get(list_url) as res:
            soup = BeautifulSoup(res.text, "html.parser")
            id_tag = soup.select("td")[4]
            num_tag = soup.select("td")[6]
            self.buy_id = id_tag.string
            self.buy_num = int(num_tag.string)
            if self.buy_id and self.buy_num:
                self.score = self.score + 15
                print("列出商品功能完成 当前分数" + str(self.score))

    def buy(self):
        buy_url = self.target + 'buy.php?id=' + self.buy_id
        self.check.get(buy_url)
        list_url = self.target + "list.php"
        with self.check.get(list_url) as res:
            soup = BeautifulSoup(res.text, "html.parser")
            num_tag = soup.select("td")[6]
            if self.buy_id and self.buy_num and self.buy_num > int(num_tag.string):
                self.score = self.score + 15
                print("购买商品功能完成 当前分数" + str(self.score))

    def upload(self):
        upload_url = self.target + "avatar.php"
        files = {'avatar': (self.img, open(self.img, 'rb'), 'image/png', {})}
        self.check.post(upload_url, files=files)
        upload_file_url = self.target + 'upload/' + self.img
        with self.check.get(upload_file_url) as r:
            if r.status_code == 200:
                self.score = self.score + 20
                print("上传功能完成 当前分数" + str(self.score))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='check url', default='http://127.0.0.1')
    args = parser.parse_args()
    c = Checker(args.url)
    c.register()
    c.login()
    c.change()
    c.list()
    c.buy()
    c.upload()
