import time
class ConnLogger:
    def __init__(self):
        self.log_act = False
    
    def log_con(self):
        if self.log_act is True:
            print("logging")
    
    def start_log(self):
        self.log_act= True
        conMon = connMoni()
        conMon.moniter(self)
    
    def stop_log(self):
        self.log_act = False

class connMoni:
    def __init__(self):
        self.config = {
            'ip' : 'some'
        }

    def moniter(self, logger):
        processtime = 0
        while logger.log_act is True:
            logger.log_con()
            time.sleep(1)
            processtime += time.process_time()
            



con = ConnLogger()
con.start_log()
con.stop_log()
