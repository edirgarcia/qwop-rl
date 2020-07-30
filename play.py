import torch
import time
from models.mnist import MnistNet
from torchvision import transforms
from PIL import Image
from capture_screen import capture_screen
from image_utils import extract_score, get_score_crop


def main():

    print("starting to play in")
    for i in range(5,0,-1):
        print(str(i)+"...")
        time.sleep(1)
    print("playing...")
    
    for i in range(100):
        curr_step_img = capture_screen(1, i)
        score_crop = get_score_crop(curr_step_img, i)
        curr_score = extract_score(score_crop, i)
        print("Current Score:", curr_score) 



if __name__ == '__main__':
    main()