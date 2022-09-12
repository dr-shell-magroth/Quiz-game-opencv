# import the opencv library
import csv
import time
from cvzone.HandTrackingModule import HandDetector
import cv2
import cvzone


class Mcq():
    def __init__(self, qdata):
        self.question = qdata[0]
        self.choice1 = qdata[1]
        self.choice2 = qdata[2]
        self.choice3 = qdata[3]
        self.choice4 = qdata[4]
        self.answare = int(qdata[5])

        self.userinput = None

    def update(self, curser, boxs):
        for x, box in enumerate(boxs):
            x1, y1, x2, y2 = box
            if x1 < curser[0] < x2 and y1 < curser[1] < y2:
                self.userinput = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


# define a video capture object
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

dictector = HandDetector(detectionCon=0)

# import csv data
pathcsv = "data.csv"
with open(pathcsv, newline='\n') as f:
    reader = csv.reader(f)
    fdata = list(reader)[1:]

# crate object for
mcqList = []
for q in fdata:
    mcqList.append(Mcq(q))

# print(len(mcqList))

qnum = 0
qtotal = len(fdata)

while True:
    # Capture the video frame
    # by frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hand, img = dictector.findHands(img, flipType=False)

    if qnum < qtotal:
        mcq = mcqList[qnum]

        img, box = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=10, border=5)
        img, box1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=10, border=5)
        img, box2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=10, border=5)
        img, box3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=10, border=5)
        img, box4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=10, border=5)

        if hand:
            # get the first hand detected in our screen and index of finger
            lmlist = hand[0]['lmList']
            curser = lmlist[8]
            length, info, img = dictector.findDistance(lmlist[8], lmlist[12], img)
            if length < 40:
                # print("clicked!")
                mcq.update(curser=curser , boxs=[box1,box2,box3,box4])
                print(mcq.userinput)
                if mcq.userinput is not None:
                    time.sleep(1)
                    qnum += 1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answare == mcq.userinput:
                score += 1
        score = round((score / qtotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, " Done Man you are nice!!", [250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f" So Your score is {score}%", [250, 300], 2, 2, offset=50, border=5)

        print(score)

    # showing Progress Bar !!
    barvalue = 150 + (950 // qtotal) * qnum
    cv2.rectangle(img, (150, 600), (barvalue, 650), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(img, f'{round(qnum/qtotal) * 100} %', [1130, 635], 2, 2, offset=16)

    # Display the resulting frame
    cv2.imshow('Img', img)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    cv2.waitKey(1)

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()


#######################################################
                                                    ###
#END OF THE PROJECT !                               ###
                                                    ###
                                                    ###
#######################################################