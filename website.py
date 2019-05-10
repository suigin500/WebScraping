#import sys
#sys.path.append("/Lib/site-packages/")
import requests
import bs4
import logging
import urllib.request
import re
import csv
import codecs
import gethtml
import airdate
from datetime import date
import programdata

#ログ出力レベルにDEBUGを設定
#logging.basicConfig(level=logging.DEBUG)


#######################################
#	文字列から日付を抜き出す
#######################################
def getDate(sArgVal):

    # 引数に"dddd/dd"形式の日付を含む？
    m = re.search('\d\d\d\d/\d\d', sArgVal)
    if m :
        # 日付をセット
        year = re.search('\d\d\d\d(?=/)', m.group())
        month = re.search('(?<=/)\d{1,2}', m.group())
        return airdate.AirDate(int(year.group()), int(month.group()))

    # 引数に"dd/dd"形式の日付を含む？
    m = re.search('\d\d/\d\d', sArgVal)
    if m :
        # 日付をセット
        month = re.search('\d\d(?=/)', m.group())
        day = re.search('(?<=/)\d{1,2}', m.group())
        return airdate.AirDate(2017, int(month.group()), int(day.group()))

    # 引数に"dddd年dd月"形式の日付を含む？
    m = re.search('\d\d\d\d年\d\d月', sArgVal)
    if m:
        # 日付をセット
        year = re.search('\d\d\d\d(?=年)', m.group())
        month = re.search('\d{1,2}(?=月)', m.group())
        return airdate.AirDate(int(year.group()), int(month.group()))


    # 引数に"ddddD"形式の日付を含む？
    m = re.search('\d\d\d\d\D', sArgVal)
    if m:
        # 日付をセット
        year = re.search('\d\d\d\d', m.group())
        return airdate.AirDate(int(year.group()))


    # 引数に"dddd"形式の日付を含む？
    m = re.search('\d\d\d\d', sArgVal)
    if m:
        # 日付をセット
        year = re.search('\d\d\d\d', m.group())
        return airdate.AirDate(int(year.group()))

    return airdate.AirDate()


#######################################
#  Webサイトクラス
#######################################
class Website():

    def __init__(self):
        self.program_list = list()

    # getプログラムリスト
    def get_program_list(self):
        return self.program_list


#######################################
#  Moonphaseクラス
#######################################
class Moonphase(Website):
    def __init__(self):
        super(Moonphase, self).__init__()

        # 出力リストを作成
        outpit_list = list()

        # MoonPhaseのサイトから番組表を読み出す
        http_bs4 = gethtml.gethtml('http://m-p.sakura.ne.jp/Html/anime.html')
        # <table>タグをリストにして取り出す
        http_td_list = http_bs4.get_table()

        # <tr>タグのリストをCSVファイルに編集
        for table_list in http_td_list:
            # 放送データオブジェクトを作成してタイトルと放送局・放送日を設定する
            program_elm = programdata.Program()

            # リストの2番目はタイトルなので取得
            title_txt = re.sub('\s', '', table_list[1].getText())
            # 放送データオブジェクトにタイトルをセット
            program_elm.SetTitle(title_txt)

            # リストの1番目は日付なので取得
            date_txt = table_list[0].getText()
            # 空白文字を削除
            date_txt = re.sub('\s', '', date_txt)
            # (*)を削除
            date_txt = re.sub('\(\*\)', '', date_txt)

            # リストの3番目は放送局なので取得
            channel_txt = re.sub('\s', '', table_list[2].getText())

            # リストの4番目は放送時間なので取得
            hour_txt = re.sub('\s', '', table_list[3].getText())

            # 放送局と日付を結合して放送局データにする
            channel_txt = channel_txt + ' : ' + date_txt

            # リストの5番目から放送データを取得
            bikou_list = re.findall('.*', table_list[4].getText())
            # リストからら作成した放送局データをリスト5番目の放送データに結合
            bikou_list.append(channel_txt + ' : ' + date_txt)
            for housou in bikou_list:
                # 地上波を探す
                m = re.search('CBC|メ～テレ|東海テレビ|中京テレビ|三重テレビ|NHK総合|NHK\S*', housou)
                if m:
                    program_elm.SetBroadcastam('地上', m.group(), getDate(housou))

                # BSを探す
                m = re.search('BS11|BSプレミアム|BS-TBS|BSジャパン|BS日テレ|BSフジ|WOWOW|BS12|Dlife', housou)
                if m:
                    program_elm.SetBroadcastam('BS', m.group(), getDate(housou))

                # CSを探す
                m = re.search('AT-X|アニマックス|キッズステーション|ファミリー劇場', housou)
                if m:
                    program_elm.SetBroadcastam('CS', m.group(), getDate(housou))

            # プログラムリストに追加
            self.program_list.append(program_elm)
            # 放送データオブジェクトから放送データの文字列リストを取得して出力リストに追加する
            outpit_list.append(program_elm.GetProgram())

        # CSVファイルに出力
        csvfile = open('anime.csv', 'wt', newline='')
        csv_witer = csv.writer(csvfile)

        for csv_out in outpit_list:
            #エンコードできる文字ならCSVファイルに出力
            try:
                csv_witer.writerow(csv_out)
            except:
                logging.debug('Err')

        csvfile.close()


#######################################
# AT-Xクラス
#######################################
class Atx(Website):
    def __init__(self):
        super(Atx, self).__init__()

        # 今月の新番組情報を読み出す
        http_bs4 = gethtml.gethtml('http://www.at-x.com/new_arrival')

        # タイトルはh4タグなのでこれを取り出す
        text_title_list = http_bs4.get_tag('h4')
        # プログラムはrightクラスのタグでまとめられているのでこれを取り出す
        text_program_list = http_bs4.get_tag('.right')

        http_day_list = list()

        # プログラムのHTMLのリストから放送開始年月日を取り出す
        for program_elm in text_program_list:
            # "dddd年dd月dd日"の日付を探す
            m = re.search('\d\d\d\d年\d{1,2}月\d{1,2}日', program_elm)
            if m:
                # 年、月、日を取り出す
                year = re.search('\d\d\d\d(?=年)', m.group())
                month = re.search('\d{1,2}(?=月)', m.group())
                days = re.search('\d{1,2}(?=日)', m.group())

                # 取り出した年,月,日を使用してdateオブジェクトを作成して日付リストに追加
                http_day_list.append(airdate.AirDate(int(year.group()), int(month.group()), int(days.group())))

            else:
                # 日付が見つからない場合は0の年月日を日付リストに追加
                http_day_list.append(airdate.AirDate())

        # 出力リストを作成
        outpit_list = list()

        for title, day in zip(text_title_list, http_day_list):
            # 放送データオブジェクトを作成してタイトルと放送局・放送日を設定する
            program_elm = programdata.Program()
            program_elm.SetTitle(title)
            program_elm.SetBroadcastam('CS', 'AT-X', day)

            # プログラムリストに追加
            self.program_list.append(program_elm)
            # 放送データオブジェクトから放送データの文字列リストを取得して出力リストに追加する
            outpit_list.append(program_elm.GetProgram())

        # CSVファイルに出力
        csvfile = open('at_x.csv', 'wt', newline='')
        csv_witer = csv.writer(csvfile)
        for csv_out in outpit_list:
            csv_witer.writerow(csv_out)

        csvfile.close()




