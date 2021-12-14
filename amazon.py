from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import messagebox as mbox
import time
import sys
import csv
from functools import partial


mail = ""
pas = ""

def window():
    win = tk.Tk()
    win.attributes("-topmost", True)
    win.title("amazon注文履歴 合計金額")
    win.geometry("400x300")

    #ラベル1を作成
    label_1 = tk.Label(win, text = "メールアドレス")
    label_1.pack()

    #テキストボックス1を作成
    text_1 = tk.Entry(win)
    text_1.pack()
    text_1.insert(tk.END,"")#初期値を指定

    #ラベル2を作成
    label_2 = tk.Label(win, text = "パスワード")
    label_2.pack()

    #テキストボックス2を作成
    text_2 = tk.Entry(show = "*", width = 20)##パスワードの入力文字を*に変換
    text_2.pack()
    text_2.insert(tk.END,"")#初期値を指定

    #ボタンを生成
    okButton = tk.Button(win, text = u"OK")
    okButton["command"] = partial(main, text_1, text_2)
    okButton.pack()

    #アプリの待機
    win.mainloop()


def main(text_1, text_2):
    mail = text_1.get()
    pas = text_2.get()

    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.implicitly_wait(10)

    browser.get("https://www.amazon.co.jp/ap/signin?_encoding=UTF8&accountStatusPolicy=P1&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fyour-account%2Forder-history%3Fie%3DUTF8%26digitalOrders%3D1%26opt%3Dab%26orderFilter%3Dyear-2018%26returnTo%3D%26unifiedOrders%3D1&pageId=webcs-yourorder&showRmrMe=1")
    email_elem = browser.find_element_by_id("ap_email")
    email_elem.send_keys(mail)
    email_elem.submit()

    password_elem = browser.find_element_by_id("ap_password")
    password_elem.send_keys(pas)
    password_elem.submit()

    # 注文履歴のページを2021年に設定
    elem = browser.find_element_by_id("nav-orders")
    elem.click()
    elem2 = browser.find_element_by_id("a-autoid-1")
    elem2.click()

    #年度の抽出
    year = browser.find_element_by_id("orderFilter_3")
    year_text = year.text
    print(year)

    # 2021年の注文履歴最初のページに遷移する
    elem3 = browser.find_element_by_id("orderFilter_3")
    elem3.click()
    time.sleep(5)

    #年度の書き込み
    with open("アマゾン注文履歴.csv", "a") as csvFile:
        wrier = csv.writer(csvFile)
        wrier.writerow([year_text + "度 注文履歴","","","","","","","","",""])
        csvFile.close()
        time.sleep(1)

    #ページ内全ての商品金額を足し合わせる
    pages_remaining = True
    total = 0
    while pages_remaining:
        try:
            price_element = browser.find_elements_by_xpath("//div[@class='a-row a-size-base']")
            price = [x.text for x in price_element]
            price_data = [s for s in price if "￥" in s]
            print(price_data)
            #

            price_data_N = []
            for data in price_data:
                after_data = data.replace("￥ ", "")
                next_after_data = after_data.replace(",", "")
                price_data_N.append(next_after_data)
            print(price_data_N)
            #

            Int_Price_Data = [int(s) for s in price_data_N]
            print(Int_Price_Data)
            #

            print(sum(Int_Price_Data))
            page_total =+ sum(Int_Price_Data)
            print(page_total)
            total = total + page_total
            print(total)
            #

            with open("アマゾン注文履歴.csv", "a") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(Int_Price_Data)
                csvFile.close()
                time.sleep(1)
                #
            next_link = browser.find_element_by_partial_link_text("次へ")
            next_link.click()
            time.sleep(1)
      #
        except:
            pages_remaining = False
            browser.close()
            with open("アマゾン注文履歴.csv", "a") as csvFile:
                writter = csv.writer(csvFile)
                writter.writerow(["合計金額",total])
                csvFile.close()
                time.sleep(1)


if __name__ == '__main__':
    window()
