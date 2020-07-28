import torch
from models.mnist import MnistNet
from torchvision import transforms
from PIL import Image


def main():

    PATH = "trained_models/mnist_cnn.pt"

    net = MnistNet()
    net.load_state_dict(torch.load(PATH))
    net.eval()
    
    print(net)
    
    transform=transforms.Compose([
    transforms.Resize(28),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    img = Image.open("qwop2.png")
    
    tensor_in = transform(img)
    tensor_in = torch.unsqueeze(tensor_in, 0)

    print(tensor_in.shape)
    result = net(tensor_in)
    print("Classification:", torch.argmax(result).item())
    
    


if __name__ == '__main__':
    main()