# Personal Snippets File (starter)

> Grow this during prep. Goal: on contest day you can retype/adapt any of these in <5 minutes.
> All libraries below are on the official IOAI 2026 allowed list.

## 1. Load data + quick look
```python
import pandas as pd
df = pd.read_csv("train.csv")
print(df.shape); print(df.head()); print(df.isna().sum())
```

## 2. sklearn workflow (tabular)
```python
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from lightgbm import LGBMClassifier

X = df.drop(columns=["label"]); y = df["label"]
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = LGBMClassifier(n_estimators=300)
model.fit(X_tr, y_tr)
print("val F1:", f1_score(y_val, model.predict(X_val)))
```

## 3. The sacred PyTorch training loop
```python
import torch, torch.nn as nn
from torch.utils.data import DataLoader

device = "cuda" if torch.cuda.is_available() else "cpu"
model = MyModel().to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    model.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
    # validation
    model.eval(); correct = total = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            pred = model(xb.to(device)).argmax(1).cpu()
            correct += (pred == yb).sum().item(); total += len(yb)
    print(f"epoch {epoch}: val acc {correct/total:.4f}")
```

## 4. Transfer learning recipe (ResNet18)
```python
import torchvision
model = torchvision.models.resnet18(weights="IMAGENET1K_V1")  # or load local .pth in contest
for p in model.parameters():
    p.requires_grad = False          # freeze backbone
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)  # new head (trainable)
```

## 5. Early stopping (bolt-on)
```python
best_val, patience, bad = float("inf"), 3, 0
# inside epoch loop, after computing val_loss:
if val_loss < best_val:
    best_val, bad = val_loss, 0
    torch.save(model.state_dict(), "best.pth")
else:
    bad += 1
    if bad >= patience: break
# after loop:
model.load_state_dict(torch.load("best.pth"))
```

## 6. Embeddings + cosine similarity (Chameleon-style)
```python
from sentence_transformers import SentenceTransformer, util
enc = SentenceTransformer("all-MiniLM-L6-v2")  # contest: use provided local model path
emb_hints = enc.encode(hint_texts, convert_to_tensor=True)
emb_cands = enc.encode(candidate_words, convert_to_tensor=True)
scores = util.cos_sim(emb_hints, emb_cands)      # (n_hints, n_candidates)
best = scores.argmax(dim=1)
```

## 7. Submission writers (format errors = 0 points)
```python
# one 0/1 per line, no header (GAITE 2025 style)
pd.Series(preds).to_csv("submissionA.csv", index=False, header=False)

# id,label Kaggle style
pd.DataFrame({"id": ids, "label": preds}).to_csv("submission.csv", index=False)

# ALWAYS verify:
print(open("submissionA.csv").read().splitlines()[:5], sum(1 for _ in open("submissionA.csv")))
```

## 8. Debug rituals
```python
print(x.shape, x.dtype, x.min(), x.max())   # before blaming the model
xb, yb = next(iter(train_loader)); print(xb.shape, yb.shape)  # test loader first
# train on tiny subset first:
small = torch.utils.data.Subset(train_ds, range(64))
```
