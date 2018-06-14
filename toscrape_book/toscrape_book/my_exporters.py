# coding = utf-8
# 与settings.py同级目录
#每种格式都是BaseItemExporter的子类，所以需要导入该模块然后继承
from scrapy.exporters import BaseItemExporter
#使用第三方库xlwt将数据写入Excel文件
import xlwt


class ExcelItemExporter(BaseItemExporter):  #继承
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.wbook = xlwt.Workbook()
        self.wsheet = self.wbook.add_sheet('scrapy')
        self.row = 0

    def finish_exporting(self):
        self.wbook.save(self.file)

    def export_item(self, item):
        # 调用基类的_get_serialized_fields方法，获得item所有字段的迭代器，然后调用self.wsheet.write方法将各字段写入Excel表格
        fields = self._get_serialized_fields(item)
        for col, v in enumerate(x for _, x in fields):
            self.wsheet.write(self.row, col, v)
        self.row += 1