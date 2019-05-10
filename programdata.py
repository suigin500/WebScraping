import airdate

# 放送局種別キーのタプル
braodcast_tapple = ('地上', 'BS', 'CS')

# 放送データクラス
class Program:
    def __init__(self):
        self.title = ''                     # タイトル
        self.channel_fast = ''              # 最速放送局
        self.day_fast = airdate.AirDate()   # 最速放送日
        self.channel = {}               # 波放送局
        self.day = {}                   # 放送日
        # 放送局と放送日の初期値をセット
        for braodcast in braodcast_tapple:
            self.channel[braodcast] = ''
            self.day[braodcast] = airdate.AirDate()

        return

    # setタイトル
    def SetTitle(self,title):
        # タイトルが設定されていない?
        if '' == self.title:
            # タイトルをセットしてTrueを返す
            self.title = title
            return True
        else:
            # タイトルをセットしないでFalseを返す
            return False

    # set放送局
    def SetBroadcastam(self, set_braodcast, set_channel, set_day=airdate.AirDate()):
        # キーとして定義されている放送局種別が指定された？
        if set_braodcast in braodcast_tapple:
            # 放送局と放送日をセット
            self.channel[set_braodcast] = set_channel
            self.day[set_braodcast] = set_day
            return True
        # キーとして定義されていない放送局種別が指定された?
        else:
            return False

    # get放送リスト
    def GetProgram(self):
        # 放送リストの作成
        program_list = list()
        program_list.append('')
        program_list.append(self.title)
        program_list.append('')
        for braodcast in braodcast_tapple:
            if self.channel[braodcast] != '':
                program_list.append(self.channel[braodcast] + ' : ' + self.day[braodcast].getdate())
            else :
                program_list.append('')

        return(program_list)

    # 放送データ上書き
    def UpdateProgram(self,update_program):
        # 受け取った放送データで上書きする
        # 受け取った放送データに放送局種別ごとのデータがあるか調べる
        for braodcast in braodcast_tapple:
            # 受け取った放送データに存在する放送局種別？
            if update_program.channel[braodcast]:
                # その放送局種別の日付が受け取った放送データの方が早いなら上書き
                if update_program.day[braodcast].getIntDate() < self.day[braodcast].getIntDate():
                    self.channel[braodcast] = update_program.channel[braodcast]
                    self.day[braodcast] = update_program.day[braodcast]


    # 最速放送日の更新
    def UpdateFast(self):
        # 放送局を調べて最速の放送局と放送日を取り出す
        for braodcast in braodcast_tapple:
            # 放送局に放送データが存在する？
            if '' != self.channel[braodcast]:

                # 最速放送日が設定されていなければ放送局を設定する
                if '' == self.channel_fast:
                    self.channel_fast = self.channel[braodcast]
                    self.day_fast = self.day[braodcast]

                # 放送局の放送日の方が最速放送日より速い？
                if self.day_fast.getIntDate() > self.day[braodcast].getIntDate():
                    # 最速放送日を更新する
                    self.channel_fast = self.channel[braodcast]
                    self.day_fast = self.day[braodcast]

        return


# 放送データコレクションクラス
class ProgramCorection:
    def __init__(self):
        self.progtam_list = list()

    # 放送データコレクションへの追加
    def SetProgram(self, adding_list):
        # 引数がlistでないなら結合しない
        if False == isinstance(adding_list,list):
            return

        # 引数がProgramクラスのlistでないなら結合しない
        for list_elm in adding_list:
            if False == isinstance(list_elm, Program):
                return

        # 追加放送データと放送データlistでタイトルが重複しているならlistに追加しないで値をlistにコピーする
        for add_elm in adding_list:
            for list_elm in self.progtam_list:

                # タイトルが重複している?
                if add_elm.title == list_elm.title:
                    # 放送データlistを追加放送データで上書き
                    list_elm.UpdateProgram(add_elm)
                    # 重複したタイトルを追加放送データから削除
                    adding_list.remove(add_elm)

        # 受け取ったプログラムリストを自身のプログラムリストに結合
        self.progtam_list.extend(adding_list)
        # 最速放送日を更新
        for program_elm in self.progtam_list:
            program_elm.UpdateFast()


    # 放送データリストの取得
    def GetProgram(self):
        return self.progtam_list

    # ソート
    def SortProgram(self):
        # プログラムリストのサイズを取り出す
        list_len = len(self.progtam_list)

        # プログラムリストをバブルソートする
        count_1st = 0
        count_2nd = 0
        while count_1st < list_len:
            while count_2nd < list_len:
                if self.progtam_list[count_1st].day_fast.getIntDate() < self.progtam_list[count_2nd].day_fast.getIntDate() :
                    buffer = self.progtam_list[count_1st]
                    self.progtam_list[count_1st] = self.progtam_list[count_2nd]
                    self.progtam_list[count_2nd] = buffer
                count_2nd += 1
            count_1st += 1
            count_2nd = 0

        return


