from datetime import datetime

class Models():
    def log(self, text):
        print("[%s] %s" % (str(datetime.now()), text))