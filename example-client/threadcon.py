import time
import threading
import access

class Downthread(object):
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def keep_rep(self,username,status):
        while self._running :
            print('rep_time-----------------------------------')
            access.report(username,status)
            time.sleep(250)
    
    def threadset(self,username,status):
        tx = threading.Thread(target = self.keep_rep,args = (username,status))
        tx.start()


    

  



