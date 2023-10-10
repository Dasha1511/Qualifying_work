import os
import pickle

import openpyxl
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QGraphicsScene, QMessageBox, QWidget, QLabel, \
    QListWidgetItem, QStackedWidget, QLineEdit, QListWidget, QFileDialog, QTableWidgetItem, QHeaderView, QCompleter, \
    QComboBox, QVBoxLayout, QDateEdit, QButtonGroup, QStyledItemDelegate, QTableWidget
from PyQt5 import uic, QtCore
import datetime
import sys

from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from SQL import database
from PIL import Image, ImageDraw, ImageFont

class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(Canvas, self).__init__(self.fig)

class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui',self)
        self.sql = database()
        self.conf_btn.clicked.connect(self.letmein)
        self.pass_cb.stateChanged.connect(self.showpass)
        self.reg_btn.clicked.connect(self.change_page)
        self.back_btn.clicked.connect(self.change_page)
        self.create_btn.clicked.connect(self.reg_user)
    def letmein(self):
        l = self.log_line.text()
        p = self.pass_line.text()
        users = self.sql.select_users()

        for u in users:
            if u[1] == l and u[2] == p:
                self.w = Window(u)
                self.w.show()
                self.close()
            else:
                self.r_lbl.setText('Ошибка: неверно введен \nлогин или пароль')

    def showpass(self, checked):
        if checked:
            self.pass_line.setEchoMode(QLineEdit.Normal)
        else:
            self.pass_line.setEchoMode(QLineEdit.Password)

    def change_page(self):
        page_ind = self.stackedWidget.currentIndex()
        if page_ind == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)


    def reg_user(self):
        users = self.sql.select_users()
        for us in users:
            if self.reglog_line.text() in us:
                self.err_lbl.setText('Ошибка: логин занят \nдругим пользователем')
                return 0

        if self.regpas_line.text() == self.regpas2_line.text():
            self.sql.insert_user([self.reglog_line.text(),self.regpas_line.text()])
            self.stackedWidget.setCurrentIndex(0)
            self.r_lbl.setText('Войдите под \nсозданым пользователем')
            self.regpas_line.setText('')
            self.regpas2_line.setText('')
            self.reglog_line.setText('')
        else:
            self.err_lbl.setText('Ошибка: корректно введите \nпароль')

class Window(QWidget):
    def __init__(self, user=None):
        super().__init__()
        uic.loadUi('dashagui.ui',self)
        self.lineEdit.textChanged.connect(self.summ)
        self.lineEdit3.textChanged.connect(self.summ)
        self.lineEdit2.textChanged.connect(self.summ2)
        self.lineEdit5.textChanged.connect(self.summ2)
        self.struct_btn.clicked.connect(self.struct)
        self.rachet_btn.clicked.connect(self.new_wind)
        self.rachet_btn_2.clicked.connect(self.another_wind)
        self.rachet_btn_3.clicked.connect(self.again_wind)
        self.inrc_btn.clicked.connect(self.increace)
        self.fact_btn.clicked.connect(self.factor)
        self.save_btn.clicked.connect(self.save)
        self.graphshow_btn.clicked.connect(self.show_graph)
        self.text_btn.clicked.connect(self.show_text)
        self.pdf_btn.clicked.connect(self.show_pdf)
        self.tabWidget.currentChanged.connect(self.on_click)

        self.nums = [['0','0','0','0','0','0'] for k in range(3)]
        self.nums2 = [['','',''] for k in range(10)]
        self.u_name = user[1]

        if os.path.exists(f'{self.u_name}.bin'):
            with open(f'{self.u_name}.bin', 'rb') as f:
                self.nums, self.nums2 = pickle.load(f)

        self.cn = 0
        self.some_lbl.setText(self.tabWidget.tabText(0))
        saveres = database().select_save()
        if saveres:
            self.nums[0] = saveres[0] + saveres[1]
            self.nums[0] = [str(k) for k in self.nums[0]]
            i = 0
            self.lineEdit.setText(self.nums[i][0])
            self.lineEdit3.setText(self.nums[i][1])
            self.lineEdit4.setText(self.nums[i][2])
            self.lineEdit2.setText(self.nums[i][3])
            self.lineEdit5.setText(self.nums[i][4])
            self.lineEdit6.setText(self.nums[i][5])

        self.sc = Canvas(self)
        for spine in self.sc.axes.spines.values():
            spine.set_visible(False)
        self.vlay.addWidget(self.sc)

        self.sc2 = Canvas(self, dpi=70)
        for spine in self.sc2.axes.spines.values():
            spine.set_visible(False)
        self.lay_2.addWidget(self.sc2)

        self.extra_list = []
        self.w = SecondWindow(self)
        self.this_box.addWidget(self.w)
        self.summ()
        self.summ2()

    def show_text(self):
        self.stackedWidget.setCurrentWidget(self.page_4)

    def show_pdf(self):
        os.system("file1.pdf")

    def show_graph(self):
        # self.sc2.axes.clear()
        # self.sc2.draw()
        self.histogram_2(self.hist_list)

    def calculateit(self):
        tbl = self.some_table
        col = 2
        row = 3

        for y in range(row):
            numlist = []
            for x in range(col):
                it = tbl.item(y,x)
                if it:
                    if it.text():
                        it = int(it.text())
                    else: it = 0
                else:
                    it = 0
                numlist.append(it)

    def on_click(self, i):
        self.some_lbl.setText(self.tabWidget.tabText(i))
        ii = i
        if ii != self.cn:
            self.page_change(ii)
            self.cn = ii

    def new_wind(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.tabWidget.hide()
        self.can_layout.hide()
        self.label.hide()
        self.inrc_btn.hide()
        self.fact_btn.hide()
        self.struct_btn.hide()
        self.save_btn.hide()

    def another_wind(self):
        self.stackedWidget.setCurrentWidget(self.page)
        self.tabWidget.show()
        self.can_layout.show()
        self.label.show()
        self.inrc_btn.show()
        self.fact_btn.show()
        self.struct_btn.show()
        self.save_btn.show()

    def again_wind(self):
        self.stackedWidget.setCurrentWidget(self.page_3)
        print(self.extra_list)
        ll = [8,9,6]
        list_for_table = []
        hist_list =[]
        for i in ll:
            d = [self.extra_list[i][0], self.extra_list[i][1]]
            list_for_table.append(d)
        for y in range(3):
            for x in range(2):
                self.some_table.setItem(y, x, QTableWidgetItem(str(list_for_table[y][x])))
            if list_for_table[y][0] != 0:
                r = (list_for_table[y][0]-list_for_table[y][1])*100/list_for_table[y][0]
            else: r=0
            self.some_table.setItem(y, 2, QTableWidgetItem(str(r)))
            hist_list.append(round(r))
        self.hist_list = hist_list

    def summ(self):
        if self.lineEdit.text() and self.lineEdit3.text() and self.lineEdit.text().replace(".", "", 1).lstrip('-').isdigit() and self.lineEdit3.text().replace(".", "", 1).lstrip('-').isdigit():
            self.info_lbl.setText('')
            self.a1 = float(self.lineEdit.text())
            self.b1 = float(self.lineEdit3.text())
            self.c1 = round(self.a1 + self.b1,2)
            self.lineEdit4.setText(str(self.c1))
        else:
            self.info_lbl.setText('Корректно введите данные в таблицу. Пример: -12.5')

    def summ2(self):
        if self.lineEdit2.text() and self.lineEdit5.text() and self.lineEdit2.text().replace(".", "", 1).lstrip('-').isdigit() and self.lineEdit5.text().replace(".", "", 1).lstrip('-').isdigit():
            self.info_lbl.setText('')
            self.a2 = float(self.lineEdit2.text())
            self.b2 = float(self.lineEdit5.text())
            self.c2 = round(self.a2 + self.b2,2)
            self.lineEdit6.setText(str(self.c2))
        else:
            self.info_lbl.setText('Корректно введите данные в таблицу. Пример: -12.5')

    def struct(self):
        if self.a1 == 0 or self.b1 == 0 or self.c1 == 0:
            self.info_lbl.setText('Корректно введите данные в таблицу. Пример: -12.5')
            return 0
        if self.lineEdit4.text() and self.lineEdit6.text():
            x = round(self.a1 / self.c1 * 100, 3)
            y = round(self.b1 / self.c1 * 100, 3)
            f = x + y
            self.a_lbl.setText(str(x)+'%')
            self.b_lbl.setText(str(y)+'%')
            self.result_lbl.setText(str(round(f,3))+'%')
            self.histogram([(round(x, 1)), (round(y, 1))])

    def increace(self):
        if self.a1 == 0 or self.b1 == 0 or self.c1 == 0:
            self.info_lbl.setText('Корректно введите данные в таблицу. Пример: -12.5')
            return 0
        if self.lineEdit4.text() and self.lineEdit6.text():
            x = ((self.a2 / self.a1)-1)*100
            y = ((self.b2 / self.b1)-1)*100
            z = ((self.c2 / self.c1)-1)*100
            self.a_lbl.setText(str(round(x,3))+'%')
            self.b_lbl.setText(str(round(y, 3)) + '%')
            self.result_lbl.setText(str(round(z, 3)) + '%')
            self.histogram([(round(x, 1)), (round(y, 1))])

    def factor(self):
        if self.a1 == 0 or self.b1 == 0 or self.c1 == 0:
            self.info_lbl.setText('Корректно введите данные в таблицу. Пример: -12.5')
            return 0
        if self.lineEdit4.text() and self.lineEdit6.text():
            x = (self.a1 / self.c1 * ((self.a2 / self.a1)-1))*100
            y = (self.b1 / self.c1 * ((self.b2 / self.b1)-1))*100
            z = x+y
            self.a_lbl.setText(str(round(x,3))+'%')
            self.b_lbl.setText(str(round(y, 3)) + '%')
            self.result_lbl.setText(str(round(z, 3)) + '%')
            self.histogram([(round(x, 1)), (round(y, 1))])

    def histogram(self, y):
        self.sc.axes.clear()
        x = ['Магазин 1','Магазин 2']
        p1 = self.sc.axes.bar(x, y, color='#EE6666')

        for rect1 in p1:
            height = rect1.get_height()
            self.sc.axes.annotate("{}%".format(height), (rect1.get_x() + rect1.get_width() / 2, height + .05), ha="center",
                         va="bottom", fontsize=15)
        self.sc.draw()

    def histogram_2(self, y):
        self.sc2.axes.clear()
        x = ['Величина\nактивов','Выручка\nза период', 'Чистая\nприбыль']
        p1 = self.sc2.axes.bar(x, y, color='#EE6666')

        for rect1 in p1:
            height = rect1.get_height()
            self.sc2.axes.annotate("{}".format(height), (rect1.get_x() + rect1.get_width() / 2, height + .05), ha="center",
                         va="bottom", fontsize=15)
        self.sc2.draw()

    def save(self):
        txt = 'Магазин 1: ' + self.a_lbl.text() + '\nМагазин 2: ' + self.b_lbl.text() + '\nИтог: ' + self.result_lbl.text()

        self.sc.fig.savefig('respic.png')

        img0 = Image.open("respic.png")
        img1 = Image.new('RGBA', (450, 300), 'white')

        img1.paste(img0, (100,0))

        idraw = ImageDraw.Draw(img1)

        font = ImageFont.truetype("arial.ttf", size=20)

        idraw.text((30, 220), txt, font=font, fill=(0,0,0,1))
        img1.save('result.png')
        QMessageBox.about(self,'Готово','Сохранение прошло успешно. Название файла - result.png')

    def page_change(self,i):
        cur = [self.lineEdit.text(),self.lineEdit3.text(),self.lineEdit4.text(),self.lineEdit2.text(),self.lineEdit5.text(),self.lineEdit6.text()]
        self.nums[self.cn] = cur
        self.lineEdit.setText(self.nums[i][0])
        self.lineEdit3.setText(self.nums[i][1])
        self.lineEdit4.setText(self.nums[i][2])
        self.lineEdit2.setText(self.nums[i][3])
        self.lineEdit5.setText(self.nums[i][4])
        self.lineEdit6.setText(self.nums[i][5])

    def closeEvent(self, *args, **kwargs):
        super().closeEvent(*args, **kwargs)
        cur = [[str(self.nums[0][0]), str(self.nums[0][1]), str(self.nums[0][2])], [str(self.nums[0][3]),
               str(self.nums[0][4]), str(self.nums[0][5])]]
        database().insert_save(cur)

        with open(f'{self.u_name}.bin', 'wb') as f:
            pickle.dump([self.nums,self.nums2], f)





class Delegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            validator = QIntValidator(editor)
            editor.setValidator(validator)
        return editor


class SecondWindow(QWidget):
    def __init__(self,ui):
        super(SecondWindow, self).__init__()
        uic.loadUi('secwin.ui',self)
        self.ui = ui
        if self.ui.nums2:
            for y, row in enumerate(self.ui.nums2):
                for x, col in enumerate(row):
                    self.first_table.setItem(y, x, QTableWidgetItem(str(col)))
            self.calculateit()

        self.first_table.setItemDelegate(Delegate())
        self.first_table.currentCellChanged.connect(self.calculateit)
        self.year_ed.textEdited.connect(self.changeheaders)
        self.import_btn.clicked.connect(self.read_excel)
        self.clear_table_btn.clicked.connect(self.clear_table)

    def changeheaders(self):
        tbl = self.first_table
        restbl = self.result_table
        year = self.year_ed.text()
        if not year:
            return 0
        lbls = [str(int(year)+i) for i in range(3)]
        #tbl = QTableWidget()
        tbl.setHorizontalHeaderLabels(lbls)
        reslbls = [lbls[i]+'/'+lbls[i+1] for i in range(2)]
        reslbls += reslbls
        restbl.setHorizontalHeaderLabels(reslbls)

    def calculateit(self):
        tbl = self.first_table
        restbl = self.result_table
        col = tbl.columnCount()
        row = tbl.rowCount()

        scnd_list = []
        for y in range(row):
            numlist = []
            for x in range(col):
                it = tbl.item(y,x)
                if it:
                    if it.text():
                        it = int(it.text())
                    else: it = 0
                else:
                    it = 0
                numlist.append(it)

            reslist = []
            reslist.append(numlist[1] - numlist[0])
            reslist.append(numlist[2] - numlist[1])
            if 0 not in numlist:
                reslist.append(str(round(((numlist[1] / numlist[0])*100), 2))+'%')
                reslist.append(str(round(((numlist[2] / numlist[1])*100), 2))+'%')
            else: reslist += ['?%', '?%']
            for x, i in enumerate(reslist):
                restbl.setItem(y, x, QTableWidgetItem(str(i)))
            scnd_list.append(reslist)

        self.ui.nums2 = []
        for y in range(row):
            temp = []
            for x in range(col):
                d = self.first_table.item(y, x).text()
                temp.append(d)
            self.ui.nums2.append(temp)
        if self.ui.nums2 != [['','',''] for i in range(row)]:
            self.ui.extra_list = scnd_list
            self.ui.rachet_btn_3.setEnabled(True)
            self.ui.rachet_btn_3.setToolTip('')

    def read_excel(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Excel (*.xlsx)")
        book = openpyxl.load_workbook(filename=fileName)
        sh_names = book.get_sheet_names()
        sheet = book[sh_names[0]]

        for y in range(2, sheet.max_row+1):
            for x in range(1,4):
                self.first_table.setItem(y-2, x-1, QTableWidgetItem(str(sheet[y][x].value)))
        self.calculateit()

    def clear_table(self):
        for y in range(self.first_table.rowCount()):
            for x in range(self.first_table.columnCount()):
                self.first_table.setItem(y, x, QTableWidgetItem(''))
        self.calculateit()
        self.ui.rachet_btn_3.setEnabled(False)
        self.ui.rachet_btn_3.setToolTip('Заполните таблицу динамики экономических показателей')


if __name__ == '__main__':
        qapp = QApplication(sys.argv)
        window = Login()
        window.show()
        qapp.exec()



