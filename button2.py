import threading
import time
import sys

def background():
        while True:
            time.sleep(3)
            print 'disarm me by typing disarm'


def other_function():
    print 'You disarmed me! Dying now.'

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=background)
threading1.daemon = True
threading1.start()

while True:
    if raw_input() == 'disarm':
        other_function()
        sys.exit()
    else:
        print 'not disarmed'
