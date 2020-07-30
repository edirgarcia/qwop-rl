import datetime
import time
import pyautogui


def main():
    
    time.sleep(10)
    
    while True:
        capture_screen(1)
        
def capture_screen(wait_time, step=0):
    
    capture = pyautogui.screenshot()
    #print(type(capture))
    img_path = r'images/capture_step_{}.png'.format(step)
    capture.save(img_path)
    
    time.sleep(wait_time)

    return capture


if __name__ == '__main__':
    main()