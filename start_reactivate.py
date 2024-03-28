import os
import time

while True:
    print('start')
    try:
        os.system("python3.10 /home/ftpuser/auto_moderator_bot/main.py")
    except Exception as e:
        print(f'exception in start: {e}') 
    print('crash')
    time.sleep(5)
