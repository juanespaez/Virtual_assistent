import random
import json
import torch
from Model2 import NueralNet
from Model2 import bag_of_words, tokenize

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
with open("intents.json", "r") as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tag"]  # Changed variable name to "tags" to avoid conflict
model_state = data["model_state"]

model = NueralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Cortana"
print("lets chat!!")
while True:
    sentence = input("you: ")
    if sentence == "quit":
        break
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    predicted_tag = tags[predicted.item()]  # Changed variable name to "predicted_tag"

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if predicted_tag == intent["tag"]:  # Use "predicted_tag" here
                print(f"{bot_name} : {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: i dont understand...")
