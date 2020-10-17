import cv2

class Camera():
    def __init__(self):
        # load video
        self.cap = cv2.VideoCapture('/Users/maximilianopalay/Documents/UM/2020s2/TICV/street_images/ruta.mov')
        while(self.cap.isOpened()):
            for i in range(2050):
                ret, frame = self.cap.read()
            break
    
    def get_frame(self):
        if (self.cap.isOpened()):
            ret, frame = self.cap.read()
        if ret == False:
            return None
        # process frame
        frame = frame[60:660,500:1100,:]
        frame2 = cv2.resize(frame, (224,224), cv2.INTER_LINEAR)
        frame_input = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        
        frame_input = cv2.flip(frame_input, 1)
        #cv2.imshow('input',cv2.cvtColor(frame_input,cv2.COLOR_RGB2BGR)) #debug
        #cv2.waitKey(1) & 0xFF      #debug
        
        #print ("image ready")      #debug
        return frame_input
