import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk.stem.porter import PorterStemmer
import json
import numpy as np
import nltk


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):  # to access the dataset with an index
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


class NueralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NueralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        return out


with open("intents.json", "r") as f:
    intents = json.load(f)

nltk.download("punkt")
stemmer = PorterStemmer()


def tokenize(setence):
    return nltk.word_tokenize(setence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenize_sentence, all_words):
    tokenize_sentence = [stem(w) for w in tokenize_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenize_sentence:
            bag[idx] = 1.0
    return bag


all_words = []
tags = []
xy = []  # the coordinates of the words since we are tokenizing them

for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ["?", "¿", ".", ",", "[", "!", "]", "(", ")", ",",
                ";"]  # we eliminate the words or marks tha we do not need
all_words = [stem(w) for w in all_words if w not in ignore_words]  # algorithm that save the useful words

all_words = sorted(set(all_words))
tags = sorted(set(tags))  # this gives me all the tags that exist in the json file

x_train = []  # this is the bag of words
y_train = []  # this would be the tags

for (pattern_sentece, tag) in xy:  # we do a for with the pattern and the tags
    bag = bag_of_words(pattern_sentece, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)  # class labels/ CrossEntropyLoss

x_train = np.array(x_train)
y_train = np.array(y_train)

batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0])
learning_rate = 0.001
num_epochs = 1000

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = NueralNet(input_size, hidden_size, output_size)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device).long()

        outputs = model(words)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"epoch {epoch + 1}/{num_epochs}, loss ={loss.item():.4f}:")

# Corrected indentation for the final loss print statement
print(f"final loss, loss ={loss.item():.4f}:")

# SAVE DATA
data = {
    "model_state": model.state_dict(),
    "input_size": input_size, #
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tag": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f"training complete, saved as {FILE}")
