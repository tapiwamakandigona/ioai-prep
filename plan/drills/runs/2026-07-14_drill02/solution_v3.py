from pathlib import Path
DATA_DIR = Path('data')


# %% ---- notebook cell ----
import json
import pickle
import random
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
class NotebookImage: pass
def display(*a, **k): pass
from PIL import Image as PILImage, ImageDraw
from tqdm import tqdm

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

GRID_SIZE = 8
N_DEPOTS = 6
MAX_STEPS = 120
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ACTION_NAMES = {
    0: "south",
    1: "north",
    2: "east",
    3: "west",
    4: "pickup",
    5: "dropoff",
}

ACTION_DELTAS = {
    0: (1, 0),
    1: (-1, 0),
    2: (0, 1),
    3: (0, -1),
}

DEPOT_NAMES = ["A", "B", "C", "D", "E", "F"]

print("data dir:", DATA_DIR)
print("device:", DEVICE)


# %% ---- notebook cell ----
class DeliverySimulator8x8:
    """Run one 8x8 delivery episode."""

    def reset(self, scenario: dict[str, Any]) -> tuple[int, int, int, int]:
        """Start a scenario and return the compact state."""
        self.step_count = 0
        self.carrying = False
        self.walls = {tuple(cell) for cell in scenario["walls"]}
        self.depots = [tuple(cell) for cell in scenario["depots"]]
        self.agent_pos = tuple(scenario["agent_pos"])
        self.package_location = int(scenario["package_location"])
        self.destination = int(scenario["destination"])
        return self.state()

    def state(self) -> tuple[int, int, int, int]:
        """Return row, column, package field, and destination."""
        package_field = N_DEPOTS if self.carrying else self.package_location
        return int(self.agent_pos[0]), int(self.agent_pos[1]), int(package_field), int(self.destination)

    def can_enter(self, row: int, col: int) -> bool:
        """Check whether the robot can occupy a cell."""
        return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and (row, col) not in self.walls

    def valid_action_mask(self) -> np.ndarray:
        """Return the currently valid actions."""
        row, col, _, destination = self.state()
        mask = np.zeros(6, dtype=bool)
        for action, (dr, dc) in ACTION_DELTAS.items():
            mask[action] = self.can_enter(row + dr, col + dc)
        mask[4] = (not self.carrying) and self.agent_pos == self.depots[self.package_location]
        mask[5] = self.carrying and self.agent_pos == self.depots[destination]
        return mask

    def observation(self) -> dict[str, Any]:
        """Build the model observation for the current state."""
        row, col, package_field, destination = self.state()
        carrying = package_field == N_DEPOTS
        dest_row, dest_col = self.depots[destination]
        target_row, target_col = (dest_row, dest_col) if carrying else self.depots[package_field]

        grid = np.zeros((6, GRID_SIZE, GRID_SIZE), dtype=np.float32)
        for wr, wc in self.walls:
            grid[0, wr, wc] = 1.0
        for dr, dc in self.depots:
            grid[1, dr, dc] = 1.0
        grid[2, row, col] = 1.0
        if not carrying:
            pr, pc = self.depots[package_field]
            grid[3, pr, pc] = 1.0
        grid[4, dest_row, dest_col] = 1.0
        grid[5, :, :] = float(carrying)

        blocked_moves = [float(not self.can_enter(row + dr, col + dc)) for dr, dc in ACTION_DELTAS.values()]
        vector = np.array(
            [
                row / (GRID_SIZE - 1),
                col / (GRID_SIZE - 1),
                package_field / N_DEPOTS,
                destination / (N_DEPOTS - 1),
                float(carrying),
                target_row / (GRID_SIZE - 1),
                target_col / (GRID_SIZE - 1),
                (target_row - row) / (GRID_SIZE - 1),
                (target_col - col) / (GRID_SIZE - 1),
                *blocked_moves,
            ],
            dtype=np.float32,
        )
        return {"grid": grid, "vector": vector, "action_mask": self.valid_action_mask(), "state": self.state()}

    def step(self, action: int) -> tuple[tuple[int, int, int, int], bool, bool, dict[str, Any]]:
        """Apply one action and report episode status."""
        action = int(action)
        done = False
        info = {"invalid_pickup_or_dropoff": False}

        if action in ACTION_DELTAS:
            dr, dc = ACTION_DELTAS[action]
            row, col = self.agent_pos[0] + dr, self.agent_pos[1] + dc
            if self.can_enter(row, col):
                self.agent_pos = (row, col)
        elif action == 4 and (not self.carrying) and self.agent_pos == self.depots[self.package_location]:
            self.carrying = True
        elif action == 5 and self.carrying and self.agent_pos == self.depots[self.destination]:
            done = True
            self.carrying = False
            self.package_location = self.destination
        elif action in (4, 5):
            info["invalid_pickup_or_dropoff"] = True
        else:
            raise ValueError(f"unknown action: {action}")

        self.step_count += 1
        return self.state(), done, self.step_count >= MAX_STEPS and not done, info

    def render(self) -> str:
        """Return an ASCII rendering of the current grid."""
        grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for row, col in self.walls:
            grid[row][col] = "#"
        for i, (row, col) in enumerate(self.depots):
            grid[row][col] = DEPOT_NAMES[i]

        agent_row, agent_col = self.agent_pos
        grid[agent_row][agent_col] = "T*" if self.carrying else "T"
        rows = [" ".join(f"{cell:>2}" for cell in row) for row in grid]
        package_name = "in taxi" if self.carrying else DEPOT_NAMES[self.package_location]
        rows.append(f"package={package_name}, destination={DEPOT_NAMES[self.destination]}")
        return "\n".join(rows)


# %% ---- notebook cell ----
with (DATA_DIR / "train_demos.pkl").open("rb") as f:
    train_data = pickle.load(f)
with (DATA_DIR / "valid_scenarios.pkl").open("rb") as f:
    valid_scenarios = pickle.load(f)
with (DATA_DIR / "test_scenarios.pkl").open("rb") as f:
    test_scenarios = pickle.load(f)

train_trajectories = train_data["trajectories"]
steps = [t["num_steps"] for t in train_trajectories]

print("Loaded data")
print("  training demonstrations:", len(train_trajectories))
print("  validation scenarios:", len(valid_scenarios))
print("  test scenarios:", len(test_scenarios))
print("  training state-action samples:", sum(steps))
print("  average demonstration length:", f"{np.mean(steps):.2f}")
print("  expert success rate:", f"{100 * np.mean([t['success'] for t in train_trajectories]):.1f}%")


# %% ---- notebook cell ----
def flatten_observation(obs):
    """Flatten one observation into a feature vector."""
    return np.concatenate([
        obs["grid"].astype(np.float32).reshape(-1),
        obs["vector"].astype(np.float32),
    ])


class DeliveryDemoDataset(Dataset):
    """Store demonstration steps as supervised examples."""

    def __init__(self, trajectories):
        """Collect all observation-action pairs."""
        self.samples = [
            (obs, int(action))
            for trajectory in trajectories
            for obs, action in zip(trajectory["observations"], trajectory["actions"], strict=True)
        ]

    def __len__(self):
        """Return the number of supervised examples."""
        return len(self.samples)

    def __getitem__(self, idx):
        """Return one feature vector and action label."""
        obs, action = self.samples[idx]
        return (
            torch.tensor(flatten_observation(obs), dtype=torch.float32),
            torch.tensor(action, dtype=torch.long),
        )


train_dataset = DeliveryDemoDataset(train_trajectories)
train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)

x0, y0 = train_dataset[0]
action_counts = Counter(int(train_dataset[i][1]) for i in range(len(train_dataset)))
print("Created dataset")
print("  state-action samples:", len(train_dataset))
print("  feature dimension:", x0.numel())
print("  first action:", int(y0), ACTION_NAMES[int(y0)])
print("  action counts:", {ACTION_NAMES[k]: v for k, v in action_counts.items()})


# %% ---- notebook cell ----
class SimpleMLPActionModel(nn.Module):
    """Predict the next action from flattened observation features."""

    def __init__(self, input_dim, hidden_dim=128, n_actions=6):
        """Create a two-hidden-layer MLP."""
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions),
        )

    def forward(self, x):
        """Return action logits."""
        return self.net(x)


model = SimpleMLPActionModel(input_dim=x0.numel()).to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

print(model)
print("parameters:", sum(p.numel() for p in model.parameters()))


# %% ---- notebook cell ----
@torch.no_grad()
def train_action_accuracy():
    """Measure action accuracy on the training demonstrations."""
    model.eval()
    correct = total = 0
    for x, y in DataLoader(train_dataset, batch_size=1024):
        pred = model(x.to(DEVICE)).argmax(dim=1).cpu()
        correct += int((pred == y).sum())
        total += int(y.numel())
    return correct / total


EPOCHS = 1  # baseline skipped in v3 (already measured: SR 0.21)
for epoch in tqdm(range(1, EPOCHS + 1)):
    model.train()
    total_loss = total_examples = 0

    for x, y in train_loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        loss = criterion(model(x), y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += float(loss.item()) * len(y)
        total_examples += len(y)

    if epoch == 1 or epoch % 5 == 0 or epoch == EPOCHS:
        print(f"epoch {epoch:02d} | loss {total_loss / total_examples:.4f} | train action acc {train_action_accuracy():.3f}")


# %% ---- notebook cell ----
@torch.no_grad()
def model_action(obs):
    """Choose the highest-logit action for one observation."""
    model.eval()
    x = torch.tensor(flatten_observation(obs), dtype=torch.float32, device=DEVICE).unsqueeze(0)
    logits = model(x)
    return int(logits.argmax(dim=1).item())


def run_episode(scenario, action_fn, max_steps=MAX_STEPS, render=False):
    """Run an action model on one scenario."""
    simulator = DeliverySimulator8x8()
    simulator.reset(scenario)
    frames, actions = [], []
    invalid_pickup_or_dropoff = 0
    done = False

    if render:
        frames.append(simulator.render())

    for _ in range(max_steps):
        action = int(action_fn(simulator.observation()))
        _, done, timed_out, info = simulator.step(action)
        actions.append(action)
        invalid_pickup_or_dropoff += int(info["invalid_pickup_or_dropoff"])
        if render:
            frames.append(simulator.render())
        if done or timed_out:
            break

    return {
        "success": done,
        "steps": len(actions),
        "invalid_pickup_or_dropoff": invalid_pickup_or_dropoff,
        "actions": actions,
        "frames": frames,
    }


def evaluate_action_model(scenarios, action_fn, limit=None):
    """Evaluate complete-episode success on a scenario list."""
    results = [run_episode(s, action_fn) for s in tqdm(scenarios[:limit])]
    return {
        "success_rate": float(np.mean([r["success"] for r in results])),
        "avg_steps": float(np.mean([r["steps"] for r in results])),
        "avg_invalid_pickup_or_dropoff": float(np.mean([r["invalid_pickup_or_dropoff"] for r in results])),
        "results": results,
    }


rng = np.random.default_rng(SEED)


def random_action_model(obs):
    """Sample a random action."""
    return int(rng.integers(6))


def mlp_action_model(obs):
    """Use the trained MLP action model."""
    return model_action(obs)



# %% GEMMA P1
import torch
from torch.utils.data import Dataset, DataLoader

class GridDemoDataset(Dataset):
    def __init__(self, trajectories):
        self.samples = []
        for traj in trajectories:
            for obs, action in zip(traj['observations'], traj['actions']):
                self.samples.append((obs, action))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        obs, action = self.samples[idx]
        return (
            torch.tensor(obs['grid'], dtype=torch.float32),
            torch.tensor(obs['vector'], dtype=torch.float32),
            torch.tensor(obs['action_mask'], dtype=torch.bool),
            torch.tensor(action, dtype=torch.long)
        )

grid_dataset = GridDemoDataset(train_trajectories)
grid_loader = DataLoader(grid_dataset, batch_size=128, shuffle=True)


# %% GEMMA P2
import torch
import torch.nn as nn

class CNNActionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(6, 32, 3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * 8 * 8 + 13, 128), nn.ReLU(),
            nn.Linear(128, 6)
        )

    def forward(self, grid, vector):
        x = self.conv(grid)
        x = torch.flatten(x, 1)
        x = torch.cat([x, vector], dim=1)
        return self.fc(x)

cnn_model = CNNActionModel().to(DEVICE)
print(sum(p.numel() for p in cnn_model.parameters()))


# %% GEMMA P8 flips (fixed)
import torch

def flip_lr(grid, v, mask, action):
    grid = torch.flip(grid, [2])
    v = v.clone()
    v[1], v[6], v[8] = 1 - v[1], 1 - v[6], -v[8]
    tmp = v[11].clone()
    v[11], v[12] = v[12], tmp
    mask = mask.clone()
    tmp_m = mask[2].clone()
    mask[2], mask[3] = mask[3], tmp_m
    action = torch.tensor(3 if action == 2 else 2 if action == 3 else action).long()
    return grid, v, mask, action

def flip_ud(grid, v, mask, action):
    grid = torch.flip(grid, [1])
    v = v.clone()
    v[0], v[5], v[7] = 1 - v[0], 1 - v[5], -v[7]
    tmp = v[9].clone()
    v[9], v[10] = v[10], tmp
    mask = mask.clone()
    tmp_m = mask[0].clone()
    mask[0], mask[1] = mask[1], tmp_m
    action = torch.tensor(1 if action == 0 else 0 if action == 1 else action).long()
    return grid, v, mask, action


# %% GEMMA P7 dataset
from torch.utils.data import Dataset, DataLoader

class FlipAugmentedDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset
    def __len__(self):
        return 4 * len(self.dataset)
    def __getitem__(self, i):
        x = self.dataset[i // 4]
        m = i % 4
        if m == 0: return x
        if m == 1: return flip_lr(*x)
        if m == 2: return flip_ud(*x)
        return flip_ud(*flip_lr(*x))

aug_dataset = FlipAugmentedDataset(grid_dataset)
aug_loader = DataLoader(aug_dataset, batch_size=128, shuffle=True)


# %% GEMMA P3 (aug_loader)
all_labels = torch.tensor([sample[3] for sample in grid_dataset])
counts = torch.bincount(all_labels, minlength=6).float()
weights = 1.0 / counts
weights = weights / weights.sum()
criterion = nn.CrossEntropyLoss(weight=weights.to(DEVICE))
optimizer = torch.optim.Adam(cnn_model.parameters(), lr=1e-3)

for epoch in range(30):
    total_loss = 0
    for grid, vector, mask, action in aug_loader:
        grid, vector, mask, action = grid.to(DEVICE), vector.to(DEVICE), mask.to(DEVICE), action.to(DEVICE)
        optimizer.zero_grad()
        logits = cnn_model(grid, vector)
        logits[~mask] = -1e9
        loss = criterion(logits, action)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/30, Loss: {total_loss / len(aug_loader):.4f}")


# %% GEMMA P4
import torch

def cnn_action(obs):
    grid = torch.tensor(obs['grid'], dtype=torch.float32, device=DEVICE).unsqueeze(0)
    vector = torch.tensor(obs['vector'], dtype=torch.float32, device=DEVICE).unsqueeze(0)
    with torch.no_grad():
        cnn_model.eval()
        logits = cnn_model(grid, vector).squeeze(0)
    mask = torch.tensor(obs['action_mask'], device=DEVICE)
    logits[~mask] = -1e9
    return int(logits.argmax())

cnn_eval = evaluate_action_model(valid_scenarios, cnn_action, limit=100)
print(f"SR: {cnn_eval['success_rate']}, Steps: {cnn_eval['avg_steps']}, Inv: {cnn_eval['avg_invalid_pickup_or_dropoff']}")

failed = [r for r in cnn_eval['results'] if not r['success']]
no_pickup = sum(1 for r in failed if 4 not in r['actions'])
has_pickup = len(failed) - no_pickup
print(f"Failed before pickup: {no_pickup}, Failed after pickup: {has_pickup}")


# %% save
import torch as _t; _t.save(cnn_model.state_dict(), 'cnn_aug_v3.pt')


# %% GEMMA P5 (verbatim, may fail)
import traceback
try:
    import pandas as pd
    import json
    
    test_predictions = generate_predictions(test_scenarios, cnn_action, limit=None)
    rows = []
    for p in test_predictions:
        row_id = f"{p['scenario']['layout_id']}__{p['scenario']['episode_seed']}"
        actions_json = json.dumps(p['actions'], separators=(',', ':'))
        rows.append({'id': row_id, 'actions': actions_json})
    
    df = pd.DataFrame(rows)
    df.to_csv('submission.csv', index=False)
    
    with open('submission.csv', 'r') as f:
        lines = f.readlines()
        for line in lines[1:3]:
            print(line.strip())
    
    print(f"Total row count: {len(df)}")
except Exception:
    traceback.print_exc()
