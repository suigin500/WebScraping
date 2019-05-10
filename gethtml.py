import bs4
import logging
import urllib.request
from datetime import date

# エンコード
def conv_encoding(data):
    # エンコード種類のタプル
    lookup = ('utf_8', 'shift_jis')

    encode = None

    # エンコード種類を選択してエンコード
    for encoding in lookup:
      try:
        if 'shift_jis' == encoding:
            data = data.decode(encoding,'ignore')
        else:
            data = data.decode(encoding)
        encode = encoding
        break
      except:
        pass
    if encode != None:
        return data,encode
    else:
        raise LookupError


#######################################
#  Webサイトクラス
#######################################
class gethtml():
    def __init__(self, url):

        self.url = url

        # HTTPResponseオブジェクトの作成
        httpres = urllib.request.urlopen(url)
        # HTMLを読み出し
        httpdata = httpres.read()

        # 読み出したHTMLはbytes変数なのでエンコード
        http_text = None
        encoding = None
        try:
            http_text, encoding = conv_encoding(httpdata)
        except:
            logging.debug(type(httpdata))

        # 読み出したHTMLソースをBeautifulSoupオブジェクトに変換してHTMLタグを操作できるようにする
        self.http_bs4 = bs4.BeautifulSoup(http_text, 'html.parser')

# 引数で受け取ったタグの内部テキストのリストを作成して返す
    def get_tag(self, tag1):

        # タグで指定された bs4.element.Tag のlistを取得
        tag_list = self.http_bs4.select(tag1)

        for tag_elem in tag_list:
            # 同じタグが入れ子になっているなら、親を含めて削除
            nest_tag = tag_elem.select(tag1)
            if nest_tag != list():
                tag_list.remove(tag_elem)


        # bs4.element.Tag のlistから内部テキストを取り出す
        text_list = list()
        for tag_elem in tag_list:
            text_list.append(tag_elem.getText())

        # 内部テキストのリストを返す
        return (text_list)

# 引数で受け取ったテーブルのリストを作成して返す
    def get_table(self):
        #t <able>タグを取り出す
        http_table_list = self.http_bs4.select('table')

        # <tr>タグで区切ってリストに出力
        http_tr_list = http_table_list[2].select('tr')

        # <td>タグで区切ったリストをリストに出力
        http_td_list = list()
        for table_list in http_tr_list:
            http_td_list.append( table_list.select('td'))

        # 内部テキストのリストを返す
        return (http_td_list)
