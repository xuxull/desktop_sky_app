import torch
from PIL import Image
from torchvision import transforms

from model import SimpleCNN


classes = [
    "cirriform clouds",
    "clear sky",
    "cumulonimbus clouds",
    "cumulus clouds",
    "high cumuliform clouds",
    "not_sky",
    "stratiform clouds",
    "stratocumulus clouds"
]


model = SimpleCNN()
model.load_state_dict(torch.load("sky_model.pth", map_location="cpu"))
model.eval()


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


def predict_image(image_path):

    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)

        top_probs, top_classes = torch.topk(probabilities, 2)

    top1_prob = top_probs[0][0].item()
    top2_prob = top_probs[0][1].item()

    confidence_percent = top1_prob * 100

    # если модель не уверена → это НЕ небо
    if top1_prob < 0.60:
        return "⚠ hmm... unclear", confidence_percent

    # если модель путается между 2 классами → тоже неуверенность
    if (top1_prob - top2_prob) < 0.12:
        return "⚠ hmm... unsure", confidence_percent

    predicted_class = top_classes[0][0].item()

    return classes[predicted_class], confidence_percent