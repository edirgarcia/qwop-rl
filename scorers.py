import torch
from models.mnist import MnistNet
from torchvision import transforms
from PIL import Image


class MnistScorer:

    def __init__(self):
        self.model_path = "trained_models/mnist_cnn.pt"
        self.net = MnistNet()
        self.net.load_state_dict(torch.load(self.model_path))
        self.net.eval()
        #print(self.net)

        self.transform=transforms.Compose([
        transforms.Resize((28,28)),
        transforms.Grayscale(num_output_channels=1),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])

        self.char_dictionary = {0:'-',1:'0',2:'1',3:'2',4:'3',5:'4',6:'5',7:'6',8:'7',9:'8',10:'9',11:'.',12:''}


    def score_from_path(self, img_path):
        img = Image.open(img_path)
        return self.score(img)

    def score(self, img):
        tensor_in = self.transform(img)
        tensor_in = torch.unsqueeze(tensor_in, 0)

        #print(tensor_in.shape)
        result = self.net(tensor_in)
        result_value = torch.argmax(result).item()
        #print("Classification:", result_value)
        return self.char_dictionary[result_value]

def main():    
    scorer = MnistScorer()
    print(scorer.score_from_path("images/chars/train/0/0.png"))



if __name__ == '__main__':
    main()