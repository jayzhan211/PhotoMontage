import sys
import cv2 as cv

from PyQt5.QtCore import QMimeData, QPointF, Qt, QObject, pyqtSlot, QSize, QAbstractListModel, QRectF
from PyQt5.QtGui import QImage, QPixmap, QDrag, QPainter, QStandardItemModel, QIcon, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QWidget, QVBoxLayout, QListWidget, QAbstractItemView, QHBoxLayout,
                             QListView, QListWidgetItem, QMainWindow, QStackedWidget, QStackedLayout, QMenu, QMenuBar,
                             QAction, QSpacerItem, QSizePolicy)

from crop import MainCropWindow
from cut import MainCutWindow
from image import ImgLabel


class MainQWidget(QWidget):
    def __init__(self, parent=None):
        super(MainQWidget, self).__init__(parent)

        self.layout = QStackedLayout(self)
        self.main_board = QWidget()
        self.crop_main_window = QMainWindow()
        self.cut_main_window = QMainWindow()

        self.main_board_layout = QHBoxLayout()
        self.main_board.setLayout(self.main_board_layout)

        # self.main_board.setFixedSize(1920, 1280)

        self.image_board = ImgLabel()
        # self.image_lists = QListWidget()
        self.image_lists = Gallery()

        # self.image_board.setFixedSize(1920, 1080 - 256)
        # self.image_lists.setFixedSize(1920)


        self.main_board_layout.addWidget(self.image_lists, 1)
        self.main_board_layout.addWidget(self.image_board, 2)


        # self.crop_board = CropLabel()
        # self.crop_board.setAlignment(Qt.AlignCenter)
        self.crop_board = MainCropWindow()
        self.cut_board = MainCutWindow()

        self.crop_main_window.setCentralWidget(self.crop_board)
        self.cut_main_window.setCentralWidget(self.cut_board)

        crop_menu = QMenuBar()
        crop_menu.addAction('Free')
        crop_menu.addAction('4:3')
        crop_menu.addAction('3:4')
        crop_menu.addAction('1:1')
        crop_menu.addAction('Done', lambda: self.set_crop_mode(False))

        cut_menu = QMenuBar()
        cut_menu.addAction('Cut', lambda: self.set_cut_repair(0))
        cut_menu.addAction('Repair', lambda: self.set_cut_repair(1))
        cut_menu.addAction('Clean', lambda: self.set_cut_repair(2))
        cut_menu.addAction('Done', lambda : self.set_cut_mode(False))


        self.crop_main_window.setMenuBar(crop_menu)
        self.cut_main_window.setMenuBar(cut_menu)

        self.layout.addWidget(self.main_board)
        self.layout.addWidget(self.crop_main_window)
        self.layout.addWidget(self.cut_main_window)
        self.layout.setCurrentWidget(self.main_board)
        # self.layout.setCurrentIndex(0)
        self.img = None

        # self.croppedPixmap = None


    def set_cut_repair(self, mode):

        # cut
        if mode == 0:
            self.cut_board.mode = 0

        # repair
        elif mode == 1:
            self.cut_board.mode = 1

        # clean
        elif mode == 2:
            self.cut_board.clean()
            self.cut_board.mode = 0




    def set_crop_mode(self, mode, qPixmap=None):
        print('start cropping: {}'.format(mode))

        if mode:
            # Set crop Rect

            self.crop_board.setPixmap(qPixmap)
            # print(self.crop_board.sizeHint())
            # self.crop_main_window.setFixedSize(self.crop_board.sizeHint())
            # print(self.crop_main_window.size())
            window.setFixedSize(self.crop_main_window.sizeHint())
            # self.setFixedSize(self.crop_main_window.size())
            # self.layout.setCurrentIndex(1)
            self.layout.setCurrentWidget(self.crop_main_window)
            # print(123)

        else:
            print('SetCroppedImg')


            self.layout.setCurrentIndex(0)
            # TODO self.crop_board.scene.cropped_img FIXED SIZE
            window.setCroppedImg(self.crop_board.scene.cropped_img)

    def set_cut_mode(self, mode, qPixmap=None):
        if mode:
            print('start to cut')

            self.cut_board.setPixmap(qPixmap)
            window.setFixedSize(self.cut_main_window.sizeHint())
            self.layout.setCurrentWidget(self.cut_main_window)
        else:
            self.layout.setCurrentWidget(self.main_board)
            self.image_board.changeImg(self.cut_board.scene.cuttedImg, self.image_board.selectedImgIndex)
            w, h = self.image_board.pixmap().width(), self.image_board.pixmap().height()
            self.image_board.setFixedSize(w, h)
            self.image_lists.setFixedSize(window.image_list_width, h)
            window.setFixedSize(w + self.image_lists.width(), h)


class Gallery(QListWidget):
    def __init__(self):
        super(Gallery, self).__init__()

        self.indexfrom = -1
        self.itemClicked.connect(self.getImg)
        self.itemPressed.connect(self.getIndex)

        # self.order = []

    # def dragEnterEvent(self, e):
    #     super(Gallery, self).dragEnterEvent(e)
    #     print('self.currentRow(): {}'.format(self.currentRow()))


    def getIndex(self, item):

        self.indexfrom = window.mainWindow.image_lists.indexFromItem(item).row()
        print('self.indexfrom: {}'.format(self.indexfrom))


    def dropEvent(self, e):
        print('self.currentRow() in dropevent: {}'.format(self.currentRow()))
        if self.currentRow() > 0:
            super(Gallery, self).dropEvent(e)
            # force to 1
            if self.currentRow() == 0:
                print('force to 1')
                item = self.takeItem(0)
                print('self.count(): {}'.format(self.count()))
                self.insertItem(1, item)
                print('self.count(): {}'.format(self.count()))
                self.setCurrentRow(1)
                print('curRow: {}'.format(self.currentRow()))
                assert self.currentRow() == 1
            print('curRow: {}'.format(self.currentRow()))
            assert self.currentRow() > 0
            print('from -> to : {} -> {}'.format(self.indexfrom, self.currentRow()))
            if self.indexfrom != self.currentRow():
                window.mainWindow.image_board.reorder(self.indexfrom, self.currentRow())

        # item = self.takeItem(self.indexfrom)
        # self.insertItem(curRow, item)
        # print(self.indexfrom, curRow)
        # print(window.mainWindow.image_board.order)
        # item = window.mainWindow.image_board.order[self.indexfrom]
        # window.mainWindow.image_board.order.remove(window.mainWindow.image_board.order[self.indexfrom])
        # window.mainWindow.image_board.order.insert(curRow, item)
        # print(window.mainWindow.image_board.order)
        # window.mainWindow.image_board.order[self.indexfrom], window.mainWindow.image_board.order[curRow] = window.mainWindow.image_board.order[curRow], window.mainWindow.image_board.order[self.indexfrom]
        # self.order[self.indexfrom], self.order[curRow] = self.order[curRow], self.order[self.indexfrom]
        # print(self.order)
        # print('{} to {}'.format(self.indexfrom, curRow))

    def getImg(self, item):
        window.mainWindow.image_board.selectImage(self.indexfrom)

    def addItem(self, item):
        super(Gallery, self).addItem(item)
        # self.order.append(len(self.order))
        # print(self.order)

    def removeImg(self, index):
        print('index: {}'.format(index))
        item = self.takeItem(index)
        print(self.count())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.image_list_width = 256
        self.image_board_height = 1080
        self.image_board_width = 1920

        # MainWindow Size
        self.resize(QSize(self.image_board_width + self.image_list_width, self.image_board_height))


        button_list = QMenuBar()
        button_list.addAction('SetBackGround', self.setBackGround)
        button_list.addAction('AddImage', self.addImage)
        button_list.addAction('SaveImage', self.saveImage)
        button_list.addAction('ResizeMode', self.setresizeMode)
        button_list.addAction('MoveMode', self.setmoveMode)
        button_list.addAction('FlipMode', self.setflipMode)
        button_list.addAction('TurnMode', self.setturnMode)
        button_list.addAction('RemoveImage', self.removeImg)
        button_list.addAction('Cut', self.cutImg)


        self.setMenuBar(button_list)

        self.mainWindow = MainQWidget()
        self.setCentralWidget(self.mainWindow)

        self.setBG = False

    # @pyqtSlot()

    def removeImg(self):
        index = self.mainWindow.image_board.selectedImgIndex
        if index > 0:
            self.mainWindow.image_board.removeImg(index)
            self.mainWindow.image_lists.removeImg(index)

            # item = self.mainWindow.image_lists.takeItem(self.mainWindow.image_board.selectedImgIndex)
            # item = None
            # print('self.mainWindow.image_lists.count(): {}'.format(self.mainWindow.image_lists.count()))
            # print(self.mainWindow.image_lists.re)


    def setBackGround(self):
        self.mainWindow.image_lists.clear()
        self.mainWindow.image_lists.setViewMode(QListView.ListMode)
        self.mainWindow.image_lists.setDragDropMode(QAbstractItemView.InternalMove)
        # self.mainWindow.image_lists.itemClicked.connect(self.selectImage)
        print('pass')
        # self.mainWindow.image_lists.dropEvent()
        # self.mainWindow.image_lists.dropEvent.connect(self.dropImage)
        print('pass2')
        self.mainWindow.image_board.initialize()
        # self.mainWindow.image_board.img = None
        # self.mainWindow.image_board.img_layers = []
        self.setBG = True

        self.addImage()


    def addImage(self):
        filename, tmp = QFileDialog.getOpenFileName(
            self, caption='Open Image', directory='./images', filter='*.png *.jpg *.bmp')

        if filename is '':
            return

        src = cv.imread(filename)
        # dst = cv.resize(src, dsize=(348, 720), interpolation=cv.INTER_CUBIC)

        self.mainWindow.img = src

        height, width, channel = self.mainWindow.img.shape

        bytesPerLine = 3 * width
        qImg = QImage(self.mainWindow.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        qPixmap = QPixmap.fromImage(qImg)

        # TODO RESIZE IMAGE
        qPixmap = qPixmap.scaledToHeight(720)
        self.mainWindow.set_crop_mode(True, qPixmap)

        # TODO main Window size 保持不變 crop window 可變動

        # TODO addimage 不要更動window size 同時保證大小不超過background

        # self.mainWindow.image_board.setPixmap(qPixmap)
        # print(456)
        # image_list_item = QListWidgetItem()
        # icon = QIcon()
        # icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        # image_list_item.setIcon(icon)
        # self.mainWindow.image_lists.addItem(image_list_item)

    def setCroppedImg(self, qPixmap):
        self.mainWindow.image_board.addPixmap(qPixmap)

        image_list_item = QListWidgetItem()
        icon = QIcon()
        icon.addPixmap(qPixmap, QIcon.Normal, QIcon.Off)
        image_list_item.setIcon(icon)
        self.mainWindow.image_lists.addItem(image_list_item)

        if self.setBG:
            w, h = self.mainWindow.image_board.pixmap().width(), self.mainWindow.image_board.pixmap().height()
            # TODO comment out
            print('w, h: ({}, {})'.format(w, h))
            self.mainWindow.image_board.setFixedSize(w, h)
            self.mainWindow.image_lists.setFixedSize(self.image_list_width, h)
            self.setFixedSize(w + self.mainWindow.image_lists.width(), h)


    # def selectImage(self, item):
    #     print('index: {}'.format(self.mainWindow.image_lists.indexFromItem(item).row()))
    #     self.mainWindow.image_board.selectImage(self.mainWindow.image_lists.indexFromItem(item).row())

    # def dropImage(self):
    #     print('DRop!!!')
    #     print(self.mainWindow.image_lists.currentRow())

    def saveImage(self):
        print('Save Image')
        filename, tmp = QFileDialog.getSaveFileName(
            self, caption='Save Image', directory='./images', filter='*.png *.jpg *.bmp')

        self.mainWindow.image_board.pixmap().toImage().save(filename)

    def setmoveMode(self):
        self.mainWindow.image_board.mode = 0
        self.mainWindow.image_board.update()
    def setresizeMode(self):
        self.mainWindow.image_board.mode = 1
        self.mainWindow.image_board.update()

    def setflipMode(self):
        self.mainWindow.image_board.mode = 2
        self.mainWindow.image_board.update()
    def setturnMode(self):
        self.mainWindow.image_board.mode = 3
        self.mainWindow.image_board.update()

    def cutImg(self):
        if self.mainWindow.image_board.selectedImgIndex > 0:
            # print('self.mainWindow.image_board.selectedImgIndex: {}'.format(self.mainWindow.image_board.selectedImgIndex))
            img = self.mainWindow.image_board.imgLayer[self.mainWindow.image_board.selectedImgIndex]
            self.mainWindow.set_cut_mode(True, img)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
