import torch
import torch.nn as nn
import os

# Создаём простую заглушку модели
class DummyModel(nn.Module):
    def __init__(self):
        super(DummyModel, self).__init__()
        self.fc = nn.Linear(100, 5)  # Простая нейросеть с 5 выходами

    def forward(self, x):
        return self.fc(x)

# Создаём папку, если её нет
os.makedirs("models/final", exist_ok=True)

# Создаём и сохраняем модель
dummy_model = DummyModel()
torch.save(dummy_model, "models/final/diagnosis_model.pth")

print("✅ Dummy model saved successfully in models/final/diagnosis_model.pth")
