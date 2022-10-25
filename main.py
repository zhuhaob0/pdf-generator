import cv2
import sys
import numpy as np
from Ui_smqnw import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap
import fitz

from model import *


class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    newPoint = pyqtSignal(QPoint)

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.setupUi(self)
        self.curImage.setScaledContents(True)  # 自适应QLabel大小
        # UI界面按钮
        self.openImagePB.clicked.connect(self.loadImgList)
        self.rotatePB.clicked.connect(self.rotate)
        self.getPaperPB.clicked.connect(self.getPosition)
        self.regulatePB.clicked.connect(self.regulate)
        self.okToNextPB.clicked.connect(self.okToNext)
        self.toPdfPB.clicked.connect(self.exportPDF)
        # 图像处理按钮
        self.imgList = []
        self.image = Image()
        self.srcImagePB.clicked.connect(self.solveSrcImage)
        self.removeShadowPB.clicked.connect(self.solveRemoveShadow)
        self.brightenPB.clicked.connect(self.solveBrighten)
        self.sharpenPB.clicked.connect(self.solveSharpen)
        self.grayPB.clicked.connect(self.solveGray)
        self.binaryPB.clicked.connect(self.solveBinary)
        self.saveInkPB.clicked.connect(self.solveSaveInk)

        self.curImagePos = self.curImage.pos()
        self.curImageHeight = self.curImage.height()
        self.curImageWidth = self.curImage.width()
        self.show()

    def redrawFrame(self, img):
        """重绘预览图"""
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 由BGR转换为RGB格式
        img = QImage(img, img.shape[1],
                     img.shape[0], QImage.Format_RGB888)  # 转换为QImage格式
        self.curImage.setPixmap(QPixmap.fromImage(img))  # 绘制图像
        return

    def solveSrcImage(self):
        self.image.srcImage()
        self.redrawFrame(self.image.img)
        self.drawPositionBox()
        return

    def solveRemoveShadow(self):
        self.image.removeShadow()
        self.redrawFrame(self.image.img)
        return

    def solveBrighten(self):
        self.image.brighten()
        self.redrawFrame(self.image.img)
        return

    def solveSharpen(self):
        self.image.sharpen()
        self.redrawFrame(self.image.img)
        return

    def solveGray(self):
        self.image.gray()
        self.redrawFrame(self.image.img)
        return

    def solveBinary(self):
        self.image.binary()
        self.redrawFrame(self.image.img)
        return

    def solveSaveInk(self):
        self.image.saveInk()
        self.redrawFrame(self.image.img)
        return

    def loadImgList(self):
        """选择多张图片导入"""
        fileDialog = QFileDialog(self)
        fileDialog.setViewMode(QFileDialog.Detail)
        fileDialog.setFileMode(QFileDialog.ExistingFiles)
        fileDialog.setNameFilter("all file(*)")
        ret = fileDialog.exec_()
        if ret == QDialog.Accepted:
            self.imgList = fileDialog.selectedFiles()
            self.imgListCursor = 0  # 存储当前处理的图像索引
            self.finish = []
            for item in self.imgList:
                print(item)

            self.openImage()  # 读取第一幅图像
            self.updateTip()
            self.drawPositionBox()  # 绘制定位框并显示
        return

    def openImage(self):
        """读取图像文件"""
        self.image = Image(cv2.imread(self.imgList[self.imgListCursor]))
        # print('shape:', self.image.img.shape)
        height, width = self.image.img.shape[:2]
        self.XScale = self.image.img.shape[1] / self.curImageWidth
        self.YScale = self.image.img.shape[0] / self.curImageHeight
        offset = int(0.02 * self.curImageHeight * self.XScale)
        self.points = np.array([[offset, offset],
                                [offset, height - offset],
                                [width - offset, height - offset],
                                [width - offset, offset]], dtype=np.int_)
        return

    def drawPositionBox(self):
        """绘制定位框"""
        img = self.image.srcImg.copy()
        color = (234, 217, 153)
        for i in range(self.points.shape[0]):
            p1 = tuple(self.points[i])
            p2 = tuple(self.points[(i + 1) % self.points.shape[0]])
            cv2.line(img, p1, p2, color, int(2 * self.XScale))
            cv2.circle(img, p1, int(10 * self.XScale), color, -1)
        self.redrawFrame(img)  # 重绘预览图

    def exportPDF(self):
        """将已经处理好的图像生成pdf"""
        outputName = QFileDialog.getSaveFileName(self)
        if outputName[0]:
            doc = fitz.open()
            for img in self.finish:
                height, width = img.shape[:2]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = fitz.Pixmap(fitz.csRGB, width, height, img.tobytes())
                page = doc.new_page(width=width, height=height)
                page.insert_image(page.rect, pixmap=img)
            doc.save(outputName[0])
            doc.close()
        return

    def rotate(self):
        """顺时针旋转 90°"""
        self.image.img = rotate.rotate_bound(self.image.img)
        self.redrawFrame(self.image.img)
        return

    def getPosition(self):
        """定位纸张的四个顶点"""
        try:
            self.image.img = self.image.srcImg
            self.points = locate.locate(self.image.img)
            self.drawPositionBox()
            # print('points:', self.points)
        except:
            QMessageBox.critical(self, '定位失败', '找不到纸张边缘，请手动定位！')
        return

    def regulate(self):
        """依据四点进行矫正，透视变换"""
        self.image.img = skew.correctRect(self.image.img, self.points)
        self.redrawFrame(self.image.img)
        self.image.correctImg = self.image.img  # 矫正后的图片
        return

    def updateTip(self):
        """更新页数提示"""
        self.remainTip.setText(
            f"剩余：{len(self.imgList) - self.imgListCursor}张")
        self.finishTip.setText(f"处理：{self.imgListCursor}张")
        return

    def okToNext(self):
        """处理好当前图片，进行下一张"""
        # 界面有已处理张数和剩余张数提示，可在触发该函数时进行更改

        if self.imgListCursor < len(self.imgList):
            self.finish.append(self.image.img.copy())  # 保存到处理完成列表
            self.imgListCursor += 1  # 后移游标
            self.updateTip()
            if self.imgListCursor < len(self.imgList):
                self.openImage()
                self.drawPositionBox()

        if self.imgListCursor >= len(self.imgList):
            QMessageBox.information(self, '图片处理', '导入的图片已处理完！')
        return

    def mousePressEvent(self, event):
        """按下鼠标"""
        if self.imgList:
            pos = event.pos() - self.curImagePos
            x = pos.x() * self.XScale
            y = pos.y() * self.YScale
            dis = np.linalg.norm(
                self.points - np.tile(np.array([x, y]), (4, 1)), axis=1)
            pid = np.argmin(dis)
            if dis[pid] < 20 * self.XScale:  # 最小触发移动距离
                self.setMouseTracking(True)  # 启用光标跟踪

    def mouseReleaseEvent(self, event):
        """松开鼠标"""
        self.setMouseTracking(False)  # 禁用光标跟踪
        # print(self.points)  # 左上 左下 右下 右上

    def mouseMoveEvent(self, event):
        """移动鼠标"""
        if self.hasMouseTracking():
            pos = event.pos() - self.curImagePos
            x = pos.x() * self.XScale
            y = pos.y() * self.YScale
            dis = np.linalg.norm(
                self.points - np.tile(np.array([x, y]), (4, 1)), axis=1)
            pid = np.argmin(dis)
            self.points[pid] = [x, y]
            self.drawPositionBox()


class Image:
    """
    图片类，内部实现操作图片的若干方法
    """

    def __init__(self, image=cv2.imread('example.jpg')):
        self.srcImg = self.img = image
        self.correctImg = self.img

    def removeShadow(self):
        self.img = shadow.remove(self.correctImg)
        return

    def srcImage(self):
        self.img = self.srcImg.copy()
        return

    def brighten(self):
        self.img = light.Brighten(self.correctImg)
        return

    def sharpen(self):
        self.brighten()
        self.img = sharpen.compute(self.img)
        return

    def gray(self):
        self.img = gray.compute(self.img)
        return

    def binary(self):
        self.gray()
        self.img = binary.compute(self.img)
        return

    def saveInk(self):
        self.binary()
        self.img = saveInk.compute(self.img)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GUI()
    sys.exit(app.exec_())
