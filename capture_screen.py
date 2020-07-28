import datetime
import time
import pyautogui


def main():
    
    time.sleep(10)
    
    while True:
        
        file_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        
        capture = pyautogui.screenshot()
        capture.save(r'images\{}.png'.format(file_name))
        
        time.sleep(1)
        
        


if __name__ == '__main__':
    main()