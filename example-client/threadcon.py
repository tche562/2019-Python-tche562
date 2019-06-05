import time
import threading
import access

class Downthread(object):
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def keep_rep(self,username):
        while self._running :
            print('rep_time-----------------------------------')
            access.report(username)
            time.sleep(250)
    
    def threadset(self,username):
        t = threading.Thread(target = self.keep_rep,args = (username,))
        t.start()

  



