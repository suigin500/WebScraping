

class AirDate():
    # コンストラクタ
    def __init__(self, year=9999, month=0, day=0):
        self.year = year
        self.month = month
        self.day = day

    def getdate(self):
        date_str = ''

        # 日付を mm/dd の形式で返す
        # 月・日がなければ空欄を返す
        if 0 != self.month:
            date_str = date_str + '{0:0>2d}'.format(self.month) + '/'
        if 0 != self.day:
            date_str = date_str + '{0:0>2d}'.format(self.day)

        return(date_str)

    # 整数型の日付を返す
    def getIntDate(self):
        date_int = self.year * 10000 + self.month * 100 + self.day
        return date_int