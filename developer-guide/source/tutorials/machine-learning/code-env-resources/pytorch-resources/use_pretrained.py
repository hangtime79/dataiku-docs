import torch

from torchvision import models, transforms
from PIL import Image

# Import pre-trained model from cache & set to evaluation mode
model = models.resnet18(weights=True)
model.eval()

# Download example image from pytorch (it's a doggie, but what kind?)
img_url = "https://github.com/pytorch/hub/raw/master/images/dog.jpg"
img_file = "dog.jpg"
torch.hub.download_url_to_file(img_url, img_file)

# Pre-process image & create a mini-batch as expected by the model
input_image = Image.open(img_file)
preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
input_tensor = preprocess(input_image)
input_batch = input_tensor.unsqueeze(0) 

# Run softmax to get probabilities since the output has unnormalized scores 
with torch.no_grad():
    output = model(input_batch)
probabilities = torch.nn.functional.softmax(output[0], dim=0)

# Download ImageNet class labels
classes_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
classes_file = "imagenet_classes.txt"
torch.hub.download_url_to_file(classes_url, classes_file)

# Map prediction to class labels and print top 5 predicted classes
with open("imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]
top5_prob, top5_catid = torch.topk(probabilities, 5)
for i in range(top5_prob.size(0)):
    print(categories[top5_catid[i]], top5_prob[i].item())