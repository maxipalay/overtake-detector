import cv2

class Camera():
    def __init__(self):
        # open video
        #self.cap = cv2.VideoCapture('../ruta.mov')
        # open camera
        self.cap = cv2.VideoCapture(0)
        
        # set buffer length to 1
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # fast forward video
        '''
        while(self.cap.isOpened()):
            for i in range(2060):
                ret, frame = self.cap.read()
            break
        '''
    def get_frame(self):
        if (self.cap.isOpened()):
            ret, frame = self.cap.read()
        if ret == False:
            return None
        # Capture frame-by-frame
        
        # process frame camera
        frame_input = frame[128:352,208:432,:]
        #frame_input = cv2.resize(frame, (224,224))
        frame_input = cv2.cvtColor(frame_input, cv2.COLOR_BGR2RGB)
        frame_input = cv2.flip(frame_input, 1)
        
        # process frame
        '''
        frame = frame[60:660,500:1100,:]
        frame2 = cv2.resize(frame, (224,224), cv2.INTER_LINEAR)
        frame_input = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        frame_input = cv2.flip(frame_input, 1)
        '''
        #cv2.imshow('input',cv2.cvtColor(frame_input,cv2.COLOR_RGB2BGR)) #debug
        #cv2.waitKey(1) & 0xFF      #debug
        
        ret, frame = self.cap.read()
        #print ("image ready")      #debug
        
        cv2.waitKey(1)
        return frame_input
