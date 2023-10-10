import sys
import unittest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from main import Login, Window

app = QApplication(sys.argv)

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.w = Login()

    def test_login(self):
        self.w.letmein()
        f = self.w.r_lbl.text()
        self.assertEqual(f, 'Неверно')
        self.w.log_line.setText('dasha')
        self.w.pass_line.setText('qwerty')
        self.w.letmein()
        self.assertEqual(self.w.w.label.text(),'График')

    def test_summ(self):
        self.mw = Window()
        self.mw.lineEdit.setText('0')
        self.mw.lineEdit3.setText('0')
        QTest.keyClicks(self.mw.lineEdit, '23')
        QTest.keyClicks(self.mw.lineEdit3, '53')
        self.mw.summ()
        self.assertEqual(self.mw.lineEdit4.text(), '76.0')

    def test_reg(self):
        self.w.reglog_line.setText('text')
        self.w.regpas_line.setText('123')
        self.w.regpas2_line.setText('321')
        QTest.mouseClick(self.w.create_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(self.w.err_lbl.text(), 'Пароли не совпадают')
        self.w.reglog_line.setText('text')
        self.w.regpas_line.setText('123')
        self.w.regpas2_line.setText('123')
        QTest.mouseClick(self.w.create_btn, Qt.MouseButton.LeftButton)
        self.assertEqual(self.w.r_lbl.text(), 'Войдите под созданым пользователем')
        r = self.w.sql.con.cursor()
        r.execute("DELETE FROM users WHERE login='text'")
        self.w.sql.con.commit()

if __name__ == '__main__':
    unittest.main()