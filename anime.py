import logging
import csv
import website
import programdata

# MoonPhaseクラスとAT-Xクラスを作成
moonphase = website.Moonphase()
atx = website.Atx()

# 放送データコレクションクラスを作成し、MoonPhaseクラスとAT-Xクラス内の番組リストを格納する
programcorection =  programdata.ProgramCorection()
programcorection.SetProgram(moonphase.get_program_list())
programcorection.SetProgram(atx.get_program_list())
programcorection.SortProgram()

# 出力リストを作成
anime_list = programcorection.GetProgram()
outpit_list = list()
for anime_elm in anime_list:
    outpit_list.append(anime_elm.GetProgram())

# CSVファイルに出力
csvfile = open('anime.csv', 'wt', newline='')
csv_witer = csv.writer(csvfile)
for csv_out in outpit_list:
    try:
        csv_witer.writerow(csv_out)
    except:
        logging.debug('Err')

csvfile.close()

