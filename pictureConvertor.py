#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图片尺寸转换器，支持单张图片转换和批量转换
@author: CSD
@date: '2019-06-21'
"""
import subprocess
try:
    import PyQt5
except ModuleNotFoundError:
    subprocess.call('pip install PyQt5')
    import PyQt5
import PyQt5.QtWidgets as qw
from PyQt5.QtGui import QPixmap
try:
    from PIL import Image
except ModuleNotFoundError:
    subprocess.call('pip install pillow')
    from PIL import Image
from tempfile import NamedTemporaryFile
import sys
import os


class PicConvert(qw.QWidget):
    """
    单张图片的转换
    """
    def __init__(self, picFile, screenW, screenH):
        super().__init__()

        # 窗口大小
        self.QWax = 50
        self.QWay = 30
        self.QWaw = screenW - 100
        self.QWah = screenH - 100

        # 图片显示最大尺寸 - 不可变
        self.pQaw = self.QWaw - 300
        self.pQah = self.QWah - 100

        # 原始图片
        self.picFile = picFile
        # 原始尺寸 - 初始化后不可变
        self.picW = 0
        self.picH = 0
        self.picSuffix = os.path.splitext(self.picFile)[1]

        self.tmpF = NamedTemporaryFile(suffix=self.picSuffix)
        self.initset_picture()

        # 重设的图片尺寸 - 最终尺寸
        self.reset_picw = self.picW
        self.reset_pich = self.picH

        # 复选框控制
        self.radioId = 0

        self.initUI()

    def initUI(self):
        self.setGeometry(self.QWax, self.QWay, self.QWaw, self.QWah)
        self.setWindowTitle('图片转换 @' + os.path.basename(self.picFile))
        pix = QPixmap(self.tmpF.name)
        self.picQL = qw.QLabel(self)
        self.picQL.setGeometry(30, 50, self.pQaw, self.pQah)
        self.picQL.setPixmap(pix)

        left_ax = self.QWaw - 300
        self.exbt = qw.QPushButton('导出图片', self)
        self.exbt.move(left_ax, 200)

        # 设置尺寸的组件
        ay = 300
        self.rb1 = qw.QRadioButton('输入尺寸：', self)
        self.rb1.move(left_ax, ay + 50)
        self.lb1w = qw.QLabel('宽：', self)
        self.lb1w.setGeometry(left_ax + 90, ay + 51, 20, 20)
        self.le1w = qw.QLineEdit(self)  # 输入图像宽
        self.le1w.setText(str(self.reset_picw))
        self.le1w.setGeometry(left_ax + 110, ay + 51, 40, 20)
        self.le1w.editingFinished.connect(self.display_refresh)
        self.lb1h = qw.QLabel('高：', self)
        self.lb1h.setGeometry(left_ax + 160, ay + 51, 20, 20)
        self.le1h = qw.QLineEdit(self)  # 输入图像高
        self.le1h.setGeometry(left_ax + 180, ay + 51, 40, 20)
        self.le1h.setText(str(self.reset_pich))
        self.le1h.editingFinished.connect(self.display_refresh)

        self.rb2 = qw.QRadioButton('等比例缩放：', self)
        self.rb2.move(left_ax, ay + 100)
        self.le2 = qw.QLineEdit(self)
        self.le2.setGeometry(left_ax + 95, ay + 101, 40, 20)
        self.le2.setText('1.0')
        self.le2.editingFinished.connect(self.display_refresh)

        self.bg = qw.QButtonGroup(self)
        self.bg.addButton(self.rb1, 1)
        self.bg.addButton(self.rb2, 2)

        self.orgsizeQL = qw.QLabel('图片原始尺寸：{}*{}'.format(self.picW, self.picH), self)
        self.orgsizeQL.move(left_ax, 50)
        self.resetQL = qw.QLabel('设置后的尺寸：{}*{}        '.format(self.reset_picw, self.reset_pich), self)
        self.resetQL.move(left_ax, 80)

        self.show()

        self.exbt.clicked.connect(self.export_picture)
        self.bg.buttonClicked.connect(self.set_size)

    def display_refresh(self):
        """
        刷新显示
        :return:
        """
        if self.radioId == 1:
            try:
                picw, pich = int(self.le1w.text()), int(self.le1h.text())
            except ValueError:
                qw.QMessageBox.warning(self, '警告!', '请输入数字！', qw.QMessageBox.Ok)
                return
        elif self.radioId == 2:
            try:
                odd = float(self.le2.text())
            except ValueError:
                qw.QMessageBox.warning(self, '警告!', '请输入数字！', qw.QMessageBox.Ok)
                return
            picw = int(self.picW * odd)
            pich = int(self.picH * odd)
        else:
            qw.QMessageBox.warning(self, '警告!', '请选择"输入尺寸"或"等比例缩放"！', qw.QMessageBox.Ok)
            return
        self.reset_picw = picw
        self.reset_pich = pich
        self.resetQL.setText('设置后的尺寸：{}*{}'.format(self.reset_picw, self.reset_pich))

        # 根据新尺寸刷新显示的图片

    def set_size(self):
        """
        设置图像大小
        :return:
        """
        sender = self.sender()
        if sender == self.bg:
            if self.bg.checkedId() == 1:
                self.radioId = 1
            elif self.bg.checkedId() == 2:
                self.radioId = 2
            else:
                pass

    def export_picture(self):
        """
        导出转换后的图片
        :return:
        """
        img = Image.open(self.picFile)
        new_img = img.resize((self.reset_picw, self.reset_pich), Image.BILINEAR)
        ex_file = self.picFile.replace(
            self.picSuffix, '_resise_{}-{}'.format(self.reset_picw, self.reset_pich) + self.picSuffix)
        new_img.save(ex_file)
        qw.QMessageBox.information(self, '提示', '导出图像成功：' + ex_file, qw.QMessageBox.Ok)

    def initset_picture(self):
        # 初始设置图片根据窗口重新调整
        img = Image.open(self.picFile)
        self.picW, self.picH = img.size

        wodd = self.picW / self.pQaw
        hodd = self.picH / self.pQah
        odd = max((wodd, hodd))
        self.pQaw = int(self.picW / odd)
        self.pQah = int(self.picH / odd)
        img = img.resize((self.pQaw, self.pQah), Image.BILINEAR)

        img.save(self.tmpF.name)
        img.close()


class BatchConvert(qw.QWidget):
    """
    批量转换
    """
    def __init__(self, folder):
        super().__init__()
        pic_suffix = ['.png', '.bmp', '.jpg', '.jpeg']
        self.folder = os.path.abspath(folder)
        # 输出的目录
        self.ex_folder = os.path.join(self.folder, 'export')
        if not os.path.exists(self.ex_folder):
            os.mkdir(self.ex_folder)
        self.pic_files = [os.path.join(self.folder, file) for file in os.listdir(self.folder)]
        self.pic_files = list(filter(lambda name: os.path.splitext(name)[1] in pic_suffix, self.pic_files))

        self.radioId = 0

        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('批量转换 @' + self.folder)
        self.center()

        infosql = ['文件夹：' + self.folder + ' 有 {} 张图片:'.format(len(self.pic_files))]
        for f in self.pic_files:
            infosql.append(os.path.basename(f))
        self.infoql = qw.QLabel('\n'.join(infosql), self)
        self.infoql.setGeometry(50, 50, 500, 400)

        left_ax = 600
        self.exbt = qw.QPushButton('导出图片', self)
        self.exbt.move(left_ax, 150)

        # 设置尺寸的组件
        ay = 200
        self.rb1 = qw.QRadioButton('输入尺寸：', self)
        self.rb1.move(left_ax, ay + 50)
        self.lb1w = qw.QLabel('宽：', self)
        self.lb1w.setGeometry(left_ax + 30, ay + 75, 20, 20)
        self.le1w = qw.QLineEdit(self)  # 输入图像宽
        self.le1w.setGeometry(left_ax + 50, ay + 75, 40, 20)
        self.lb1h = qw.QLabel('高：', self)
        self.lb1h.setGeometry(left_ax + 30, ay + 100, 20, 20)
        self.le1h = qw.QLineEdit(self)  # 输入图像高
        self.le1h.setGeometry(left_ax + 50, ay + 100, 40, 20)

        self.rb2 = qw.QRadioButton('等比例缩放：', self)
        self.rb2.move(left_ax, ay + 150)
        self.le2 = qw.QLineEdit(self)
        self.le2.setGeometry(left_ax + 95, ay + 151, 40, 20)

        self.bg = qw.QButtonGroup(self)
        self.bg.addButton(self.rb1, 1)
        self.bg.addButton(self.rb2, 2)

        self.exbt.clicked.connect(self.export_picture)
        self.bg.buttonClicked.connect(self.set_size)

    def set_size(self):
        sender = self.sender()
        if sender == self.bg:
            if self.bg.checkedId() == 1:
                self.radioId = 1
            elif self.bg.checkedId() == 2:
                self.radioId = 2
            else:
                pass

    def export_picture(self):
        if not os.path.exists(self.ex_folder):
            os.mkdir(self.ex_folder)

        if self.radioId == 1:
            wtext = self.le1w.text().strip()
            htext = self.le1h.text().strip()
            if len(wtext) == 0 or len(htext) == 0:
                qw.QMessageBox.warning(self, '警告!', '请输入图片尺寸！', qw.QMessageBox.Ok)
                return
            try:
                picw, pich = int(wtext), int(htext)
            except ValueError:
                qw.QMessageBox.warning(self, '警告!', '请输入数字！', qw.QMessageBox.Ok)
                return
            rely = qw.QMessageBox.information(self, '提示', '设置图片尺寸：{}*{}！'.format(picw, pich),
                                              qw.QMessageBox.Ok | qw.QMessageBox.Cancel, qw.QMessageBox.Cancel)
            if rely == qw.QMessageBox.Ok:
                for file in self.pic_files:
                    img = Image.open(file)
                    new_img = img.resize((picw, pich), Image.BILINEAR)
                    new_img.save(os.path.join(self.ex_folder, os.path.basename(file)))
            qw.QMessageBox.information(self, '提示', '图像输出文件夹：{}'.format(self.ex_folder), qw.QMessageBox.Ok)
        elif self.radioId == 2:
            if len(self.le2.text()) == 0:
                qw.QMessageBox.warning(self, '警告!', '请输入缩放比例！', qw.QMessageBox.Ok)
                return
            try:
                odd = float(self.le2.text())
            except ValueError:
                qw.QMessageBox.warning(self, '警告!', '请输入数字！', qw.QMessageBox.Ok)
                return
            rely = qw.QMessageBox.information(self, '提示', '图片缩放 {} 倍！'.format(odd),
                                              qw.QMessageBox.Ok | qw.QMessageBox.Cancel, qw.QMessageBox.Cancel)
            if rely == qw.QMessageBox.Ok:
                for file in self.pic_files:
                    img = Image.open(file)
                    picw, pich = int(img.width * odd), int(img.height * odd)
                    new_img = img.resize((picw, pich), Image.BILINEAR)
                    new_img.save(os.path.join(self.ex_folder, os.path.basename(file)))
            qw.QMessageBox.information(self, '提示', '图像输出文件夹：{}'.format(self.ex_folder), qw.QMessageBox.Ok)
        else:
            qw.QMessageBox.warning(self, '警告!', '请选择"输入尺寸"或"等比例缩放"！', qw.QMessageBox.Ok)

    def center(self):
        size = self.geometry()
        screen = qw.QDesktopWidget().screenGeometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))


class InitDialog(qw.QWidget):
    """
    初始对话框
    """
    def __init__(self):

        super().__init__()
        # 显示器像素
        screen = qw.QDesktopWidget().screenGeometry()
        self.screenW = screen.width()
        self.screenH = screen.height()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('图片转换 @CSD')
        self.resize(400, 150)
        self.center()

        self.bt1 = qw.QPushButton('打开一张图片', self)
        self.bt1.move(50, 50)
        self.bt2 = qw.QPushButton('批量转换', self)
        self.bt2.move(220, 50)

        self.show()

        self.bt1.clicked.connect(self.open_file)
        self.bt2.clicked.connect(self.open_folder)

    def center(self):

        size = self.geometry()
        self.move(int((self.screenW - size.width()) / 2),
                  int((self.screenH - size.height()) / 2))

    def open_file(self):
        """
        打开一张图片
        :return:
        """
        fname = qw.QFileDialog.getOpenFileName(self, '选择一张图片', './', ("Images (*.png *.jpg *.bmp *.jpeg)"))
        if fname[0]:
            picFile = fname[0]
            self.picWin = PicConvert(picFile, self.screenW, self.screenH)
            self.picWin.show()

    def open_folder(self):
        """
        打开文件夹
        :return:
        """
        fname = qw.QFileDialog.getExistingDirectory()
        self.bc = BatchConvert(fname)
        self.bc.show()


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    init = InitDialog()
    sys.exit(app.exec_())
