from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys
import time
import cvzone
from ultralytics import YOLO
import numpy as np
from sort import *
import math

model = YOLO("../Yolo-Weights/yolov8n.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

x1 = 0
x2 = 0
y1 = 0
y2 = 0

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    global x1
    global x2
    global y1
    global y2

    def run(self):

        cap = cv2.VideoCapture("C:/Users/anlys/OneDrive/Masaüstü/TAUV-GUI/Videos/people.mp4")
        while True:
            ret, frame = cap.read()
            results = model(frame, stream=True)

            detections = np.empty((0, 5))

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Bounding Box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
                    w, h = x2 - x1, y2 - y1

                    # Confidence
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    # Class Name
                    cls = int(box.cls[0])
                    currentClass = classNames[cls]

                    if currentClass == "person" and conf > 0.3:
                        # cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                        #                    scale=0.6, thickness=1, offset=3)
                        # cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))

            resultsTracker = tracker.update(detections)

            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(result)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(frame, f' {int(id)}', (max(0, x1), max(35, y1)),
                                   scale=2, thickness=3, offset=10)

            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.width = 1080
        self.height = 640

        self.setWindowTitle("TAUROV GUI")
        self.setGeometry(50, 100, self.width, self.height)

        self.tabWidgets()
        self.widgets()
        self.layouts()
        self.setStyle()
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.inputImage.setPixmap(QPixmap.fromImage(image))

    def tabWidgets(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Object Detection")
        self.tabs.addTab(self.tab2, "Parameters")

    def widgets(self):
        # tab1 left (real-time cam stream)

        self.inputImage = QLabel(self)

        # tab1 left middle
        self.engine1 = QLabel(self)
        self.engine1.setText("Engine 1")
        self.checkEngine1 = QPushButton("Check")
        self.checkEngine1.clicked.connect(self.checkEngineFunction)

        self.engine2 = QLabel(self)
        self.engine2.setText("Engine 2")
        self.checkEngine2 = QPushButton("Check")
        self.checkEngine2.clicked.connect(self.checkEngineFunction)

        self.engine3 = QLabel(self)
        self.engine3.setText("Engine 3")
        self.checkEngine3 = QPushButton("Check")
        self.checkEngine3.clicked.connect(self.checkEngineFunction)

        self.engine4 = QLabel(self)
        self.engine4.setText("Engine 4")
        self.checkEngine4 = QPushButton("Check")
        self.checkEngine4.clicked.connect(self.checkEngineFunction)

        # tab right middle
        # creating progress bar
        self.progressButton = QPushButton("Mission 1")
        self.progressButton.setStyleSheet(
            "border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #00FFFF;width: 10px;margin: 0.5px;")
        self.progressButton.clicked.connect(self.progressAction)
        self.mission1 = QLabel(self)
        self.pbar = QProgressBar(self)
        self.pbar.setStyleSheet(
            "border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #CD96CD;width: 10px;margin: 0.5px;")
        self.pbar2 = QProgressBar(self)
        self.pbar2.setStyleSheet(
            "border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #CD96CD;width: 10px;margin: 0.5px;")

        # tab right
        self.detectedObjects = QTextEdit(self)
        self.detectedObjects.setText(f"{str(x1)} {str(y1)}")

    def setStyle(self):
        self.checkEngine1.setStyleSheet(
            "border: 2px solid grey; border-radius: 5px; text-align: center;background-color: #CD96CD;width: 10px;margin: 0.5px;")

    def layouts(self):
        # main Layout
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.leftMiddleLayout = QFormLayout()
        self.rightMiddleLayout = QFormLayout()
        self.rightLayout = QFormLayout()

        # left layout and groupbox
        self.leftLayoutGroupBox = QGroupBox("Frame")
        self.leftLayout.addRow(self.inputImage)
        self.leftLayoutGroupBox.setLayout(self.leftLayout)

        # left middle layout and groupbox
        self.leftMiddleGroupBox = QGroupBox("Engines")
        self.leftMiddleLayout.addRow(self.engine1)
        self.leftMiddleLayout.addRow(self.checkEngine1)
        self.leftMiddleLayout.addRow(self.engine2)
        self.leftMiddleLayout.addRow(self.checkEngine2)
        self.leftMiddleLayout.addRow(self.engine3)
        self.leftMiddleLayout.addRow(self.checkEngine3)
        self.leftMiddleLayout.addRow(self.engine4)
        self.leftMiddleLayout.addRow(self.checkEngine4)
        self.leftMiddleGroupBox.setLayout(self.leftMiddleLayout)

        # right middle layout and groupbox
        self.rightMiddleGroupbox = QGroupBox("Missions")
        self.rightMiddleLayout.addRow(self.progressButton)
        self.rightMiddleLayout.addRow(self.mission1)
        self.rightMiddleLayout.addRow("Mission 1", self.pbar)
        self.rightMiddleLayout.addRow("Mission 2", self.pbar2)
        self.rightMiddleGroupbox.setLayout(self.rightMiddleLayout)

        # right layout and groupbox
        self.rightLayoutGroupBox = QGroupBox("Detected Objects")
        self.rightLayout.addRow(self.detectedObjects)
        self.rightLayoutGroupBox.setLayout(self.rightLayout)

        # tab1 main layout
        self.mainLayout.addWidget(self.leftLayoutGroupBox, 50)
        self.mainLayout.addWidget(self.leftMiddleGroupBox, 15)
        self.mainLayout.addWidget(self.rightMiddleGroupbox, 20)
        self.mainLayout.addWidget(self.rightLayoutGroupBox, 15)
        self.tab1.setLayout(self.mainLayout)

    def checkEngineFunction(self):
        pass

    def progressAction(self):
        for i in range(101):
            time.sleep(0.05)
            self.pbar.setValue(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())