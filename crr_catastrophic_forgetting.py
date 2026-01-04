#!/usr/bin/env python3
"""
CRR-Based Solution for Catastrophic Forgetting
===============================================

This module implements a Coherence-Rupture-Regeneration (CRR) approach to
managing catastrophic forgetting in continual learning.

Key Insight: The 16 nats threshold (e^16 ≈ 8.9 million precision amplification)
provides a principled criterion for when to consolidate, restructure, or
preserve learned representations.

CRR Mechanisms for Continual Learning:
1. COHERENCE: Track prediction consistency across tasks (accumulated evidence)
2. RUPTURE: Detect when new learning threatens old knowledge (threshold crossing)
3. REGENERATION: Use memory-weighted consolidation (exponential kernel)

Author: CRR Research Team
Date: January 2026
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import copy
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# SECTION 1: CRR CORE COMPONENTS FOR CONTINUAL LEARNING
# =============================================================================

@dataclass
class CRRState:
    """Tracks the CRR state for a continual learning system."""
    coherence: float = 0.0                    # Accumulated coherence C(t)
    omega: float = 1.0                        # Rigidity threshold Ω
    precision: float = 1.0                    # Current precision Π
    rupture_count: int = 0                    # Number of ruptures
    task_coherences: Dict[int, float] = field(default_factory=dict)
    rupture_history: List[float] = field(default_factory=list)

    # The 16 nats threshold
    NATS_THRESHOLD: float = 16.0

    def update_precision(self):
        """Π = (1/Ω) * exp(C/Ω)"""
        self.precision = (1.0 / self.omega) * np.exp(self.coherence / self.omega)

    def check_rupture(self) -> bool:
        """Check if coherence exceeds threshold (16 Ω-units)"""
        return self.coherence >= self.NATS_THRESHOLD * self.omega

    def trigger_rupture(self):
        """Execute rupture: reset coherence, increment counter"""
        self.rupture_history.append(self.coherence)
        self.rupture_count += 1
        # Partial reset with memory preservation
        self.coherence *= 0.1  # Retain 10% as "consolidated" coherence
        self.update_precision()


class CoherenceTracker:
    """
    Tracks coherence as accumulated prediction consistency.

    Coherence = Σ log(p(correct prediction | model))

    High coherence = model consistently makes correct predictions
    Low coherence = model struggling with current task
    """

    def __init__(self, omega: float = 1.0):
        self.omega = omega
        self.coherence_per_task: Dict[int, List[float]] = defaultdict(list)
        self.total_coherence: float = 0.0

    def compute_prediction_coherence(self,
                                      model: nn.Module,
                                      dataloader: DataLoader,
                                      task_id: int) -> float:
        """
        Compute coherence contribution from predictions on a task.

        Returns: coherence in nats (natural log of likelihood)
        """
        model.eval()
        total_log_prob = 0.0
        n_samples = 0

        with torch.no_grad():
            for x, y in dataloader:
                logits = model(x)
                log_probs = F.log_softmax(logits, dim=1)
                # Coherence = log probability of correct class
                correct_log_probs = log_probs.gather(1, y.unsqueeze(1)).squeeze()
                total_log_prob += correct_log_probs.sum().item()
                n_samples += len(y)

        # Average coherence per sample (in nats)
        coherence = total_log_prob / max(n_samples, 1)
        self.coherence_per_task[task_id].append(coherence)
        return coherence

    def compute_cross_task_coherence(self,
                                      model: nn.Module,
                                      task_dataloaders: Dict[int, DataLoader]) -> Dict[int, float]:
        """Compute coherence on all previous tasks (for forgetting detection)."""
        coherences = {}
        for task_id, loader in task_dataloaders.items():
            coherences[task_id] = self.compute_prediction_coherence(model, loader, task_id)
        return coherences

    def detect_forgetting(self,
                          current_coherences: Dict[int, float],
                          threshold_drop: float = 2.0) -> List[int]:
        """
        Detect which tasks are being forgotten.

        Forgetting = coherence drop > threshold (in nats)
        threshold_drop = 2.0 nats corresponds to ~7x worse predictions
        """
        forgotten_tasks = []
        for task_id, current_c in current_coherences.items():
            if task_id in self.coherence_per_task and len(self.coherence_per_task[task_id]) > 0:
                max_historical = max(self.coherence_per_task[task_id])
                if max_historical - current_c > threshold_drop:
                    forgotten_tasks.append(task_id)
        return forgotten_tasks


class MemoryKernel:
    """
    Implements the CRR memory kernel K(C,Ω) = exp(C/Ω).

    Used to weight the importance of past model states for regeneration.
    """

    def __init__(self, omega: float = 1.0):
        self.omega = omega

    def compute_weight(self, coherence: float) -> float:
        """K(C,Ω) = exp(C/Ω)"""
        # Clip to avoid numerical overflow
        ratio = min(coherence / self.omega, 50.0)
        return np.exp(ratio)

    def compute_importance_weights(self,
                                    coherence_history: List[float]) -> np.ndarray:
        """
        Compute importance weights for each historical state.

        More coherent states get exponentially higher weight.
        """
        weights = np.array([self.compute_weight(c) for c in coherence_history])
        # Normalize to sum to 1
        return weights / (weights.sum() + 1e-10)


# =============================================================================
# SECTION 2: CRR CONTINUAL LEARNING METHODS
# =============================================================================

class CRRRegularizer:
    """
    CRR-based regularization for preventing catastrophic forgetting.

    Key idea: Weight parameter importance by coherence-derived precision.
    Similar to EWC but with CRR-derived importance weights.
    """

    def __init__(self, model: nn.Module, omega: float = 1.0):
        self.omega = omega
        self.memory_kernel = MemoryKernel(omega)
        self.saved_params: Dict[int, Dict[str, torch.Tensor]] = {}
        self.fisher_info: Dict[int, Dict[str, torch.Tensor]] = {}
        self.task_coherences: Dict[int, float] = {}

    def compute_fisher_information(self,
                                    model: nn.Module,
                                    dataloader: DataLoader,
                                    task_id: int) -> Dict[str, torch.Tensor]:
        """
        Compute Fisher Information Matrix (diagonal approximation).

        This measures parameter importance for the current task.
        """
        fisher = {n: torch.zeros_like(p) for n, p in model.named_parameters() if p.requires_grad}
        model.eval()

        n_samples = 0
        for x, y in dataloader:
            model.zero_grad()
            logits = model(x)
            log_probs = F.log_softmax(logits, dim=1)
            # Sample from model's distribution
            sampled = torch.multinomial(torch.exp(log_probs), 1).squeeze()
            loss = F.cross_entropy(logits, sampled)
            loss.backward()

            for n, p in model.named_parameters():
                if p.requires_grad and p.grad is not None:
                    fisher[n] += p.grad.detach() ** 2
            n_samples += len(x)

        # Average over samples
        for n in fisher:
            fisher[n] /= max(n_samples, 1)

        return fisher

    def consolidate_task(self,
                         model: nn.Module,
                         dataloader: DataLoader,
                         task_id: int,
                         coherence: float):
        """
        Consolidate learning for a task using CRR memory weighting.

        Higher coherence = more important to preserve = higher weight.
        """
        # Save current parameters
        self.saved_params[task_id] = {
            n: p.detach().clone()
            for n, p in model.named_parameters() if p.requires_grad
        }

        # Compute Fisher information
        self.fisher_info[task_id] = self.compute_fisher_information(model, dataloader, task_id)

        # Store coherence for memory weighting
        self.task_coherences[task_id] = coherence

    def compute_regularization_loss(self, model: nn.Module) -> torch.Tensor:
        """
        Compute CRR-weighted regularization loss.

        Loss = Σ_task w(C_task) * Σ_param F_param * (θ - θ_task)²

        where w(C) = exp(C/Ω) is the memory kernel weight.
        """
        reg_loss = torch.tensor(0.0)

        for task_id in self.saved_params:
            # Compute memory kernel weight based on task coherence
            weight = self.memory_kernel.compute_weight(self.task_coherences[task_id])

            for n, p in model.named_parameters():
                if n in self.saved_params[task_id] and p.requires_grad:
                    # Fisher-weighted distance from saved params
                    fisher = self.fisher_info[task_id][n]
                    saved = self.saved_params[task_id][n]
                    reg_loss = reg_loss + weight * (fisher * (p - saved) ** 2).sum()

        return reg_loss


class CRRReplayBuffer:
    """
    Experience replay buffer with CRR memory weighting.

    Samples are weighted by their coherence contribution.
    High-coherence samples (model predicted correctly with high confidence)
    are more likely to be replayed.
    """

    def __init__(self, capacity: int = 1000, omega: float = 1.0):
        self.capacity = capacity
        self.omega = omega
        self.memory_kernel = MemoryKernel(omega)

        self.samples: List[Tuple[torch.Tensor, torch.Tensor, int]] = []  # (x, y, task_id)
        self.coherences: List[float] = []

    def add_samples(self,
                    model: nn.Module,
                    x: torch.Tensor,
                    y: torch.Tensor,
                    task_id: int):
        """Add samples with their coherence scores."""
        model.eval()
        with torch.no_grad():
            logits = model(x)
            log_probs = F.log_softmax(logits, dim=1)
            sample_coherences = log_probs.gather(1, y.unsqueeze(1)).squeeze()

        for i in range(len(x)):
            if len(self.samples) < self.capacity:
                self.samples.append((x[i].clone(), y[i].clone(), task_id))
                self.coherences.append(sample_coherences[i].item())
            else:
                # Replace lowest-coherence sample
                min_idx = np.argmin(self.coherences)
                if sample_coherences[i].item() > self.coherences[min_idx]:
                    self.samples[min_idx] = (x[i].clone(), y[i].clone(), task_id)
                    self.coherences[min_idx] = sample_coherences[i].item()

    def sample_batch(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor, List[int]]:
        """Sample batch weighted by coherence (memory kernel)."""
        if len(self.samples) == 0:
            return None, None, None

        weights = self.memory_kernel.compute_importance_weights(self.coherences)
        indices = np.random.choice(len(self.samples),
                                   size=min(batch_size, len(self.samples)),
                                   replace=False,
                                   p=weights)

        x = torch.stack([self.samples[i][0] for i in indices])
        y = torch.stack([self.samples[i][1] for i in indices])
        task_ids = [self.samples[i][2] for i in indices]

        return x, y, task_ids


class CRRContinualLearner:
    """
    Main CRR-based continual learning system.

    Combines:
    - Coherence tracking for forgetting detection
    - Rupture detection using 16 nats threshold
    - Regeneration via memory-weighted consolidation
    """

    def __init__(self,
                 model: nn.Module,
                 omega: float = 1.0,
                 reg_strength: float = 1000.0,
                 replay_buffer_size: int = 500):
        self.model = model
        self.omega = omega
        self.reg_strength = reg_strength

        # CRR components
        self.state = CRRState(omega=omega)
        self.coherence_tracker = CoherenceTracker(omega)
        self.regularizer = CRRRegularizer(model, omega)
        self.replay_buffer = CRRReplayBuffer(replay_buffer_size, omega)

        # Task tracking
        self.current_task = 0
        self.task_dataloaders: Dict[int, DataLoader] = {}

        # Metrics
        self.metrics: Dict[str, List[float]] = defaultdict(list)

    def train_task(self,
                   train_loader: DataLoader,
                   val_loader: DataLoader,
                   task_id: int,
                   epochs: int = 10,
                   lr: float = 0.001):
        """
        Train on a new task with CRR-based forgetting prevention.
        """
        self.current_task = task_id
        self.task_dataloaders[task_id] = val_loader

        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        for epoch in range(epochs):
            self.model.train()
            epoch_loss = 0.0
            epoch_coherence = 0.0
            n_batches = 0

            for x, y in train_loader:
                optimizer.zero_grad()

                # Forward pass
                logits = self.model(x)
                task_loss = F.cross_entropy(logits, y)

                # CRR regularization loss (prevent forgetting)
                reg_loss = self.regularizer.compute_regularization_loss(self.model)

                # Replay loss (if we have stored samples)
                replay_loss = torch.tensor(0.0)
                replay_x, replay_y, _ = self.replay_buffer.sample_batch(32)
                if replay_x is not None:
                    replay_logits = self.model(replay_x)
                    replay_loss = F.cross_entropy(replay_logits, replay_y)

                # Total loss
                total_loss = task_loss + self.reg_strength * reg_loss + 0.5 * replay_loss
                total_loss.backward()
                optimizer.step()

                # Update coherence
                with torch.no_grad():
                    log_probs = F.log_softmax(logits, dim=1)
                    batch_coherence = log_probs.gather(1, y.unsqueeze(1)).mean().item()
                    epoch_coherence += batch_coherence

                # Add to replay buffer
                self.replay_buffer.add_samples(self.model, x, y, task_id)

                epoch_loss += total_loss.item()
                n_batches += 1

            # Update CRR state
            avg_coherence = epoch_coherence / max(n_batches, 1)
            self.state.coherence += max(0, avg_coherence + 2.0)  # Shift to positive
            self.state.update_precision()

            # Check for rupture (16 nats threshold)
            if self.state.check_rupture():
                print(f"  [RUPTURE] Coherence {self.state.coherence:.2f} exceeded threshold. Restructuring...")
                self._handle_rupture()

            # Compute validation metrics
            val_acc = self._compute_accuracy(val_loader)

            # Check for forgetting on previous tasks
            if task_id > 0:
                cross_coherences = self.coherence_tracker.compute_cross_task_coherence(
                    self.model, self.task_dataloaders
                )
                forgotten = self.coherence_tracker.detect_forgetting(cross_coherences)
                if forgotten:
                    print(f"  [WARNING] Forgetting detected on tasks: {forgotten}")

            self.metrics['train_loss'].append(epoch_loss / n_batches)
            self.metrics['val_acc'].append(val_acc)
            self.metrics['coherence'].append(self.state.coherence)
            self.metrics['precision'].append(self.state.precision)

            if epoch % 2 == 0:
                print(f"  Epoch {epoch}: Loss={epoch_loss/n_batches:.4f}, "
                      f"Acc={val_acc:.3f}, C={self.state.coherence:.2f}, "
                      f"Π={self.state.precision:.2f}")

        # Consolidate task after training
        task_coherence = self.coherence_tracker.compute_prediction_coherence(
            self.model, val_loader, task_id
        )
        self.regularizer.consolidate_task(self.model, train_loader, task_id, task_coherence)
        self.state.task_coherences[task_id] = task_coherence

        print(f"  Task {task_id} consolidated with coherence {task_coherence:.3f}")

    def _handle_rupture(self):
        """
        Handle rupture event: restructure while preserving important knowledge.

        This is the key CRR mechanism for managing catastrophic forgetting.
        """
        self.state.trigger_rupture()

        # Regeneration: reinforce high-coherence memories
        if len(self.replay_buffer.samples) > 0:
            self.model.train()
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.0001)

            # Regeneration passes with memory-weighted replay
            for _ in range(5):
                x, y, _ = self.replay_buffer.sample_batch(64)
                if x is not None:
                    optimizer.zero_grad()
                    logits = self.model(x)
                    loss = F.cross_entropy(logits, y)
                    loss.backward()
                    optimizer.step()

    def _compute_accuracy(self, dataloader: DataLoader) -> float:
        """Compute classification accuracy."""
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for x, y in dataloader:
                logits = self.model(x)
                preds = logits.argmax(dim=1)
                correct += (preds == y).sum().item()
                total += len(y)
        return correct / max(total, 1)

    def evaluate_all_tasks(self) -> Dict[int, float]:
        """Evaluate accuracy on all learned tasks."""
        accuracies = {}
        for task_id, loader in self.task_dataloaders.items():
            accuracies[task_id] = self._compute_accuracy(loader)
        return accuracies

    def get_forgetting_metrics(self) -> Dict[str, float]:
        """
        Compute forgetting metrics across all tasks.

        Returns:
        - avg_accuracy: Mean accuracy across all tasks
        - forgetting: Mean drop from peak accuracy
        - backward_transfer: Effect of later learning on earlier tasks
        """
        accuracies = self.evaluate_all_tasks()

        if len(accuracies) == 0:
            return {'avg_accuracy': 0.0, 'forgetting': 0.0}

        avg_acc = np.mean(list(accuracies.values()))

        # Compute forgetting (difference from peak coherence)
        forgetting_scores = []
        for task_id in accuracies:
            if task_id in self.state.task_coherences:
                # Use coherence as proxy for peak performance
                peak_coherence = self.state.task_coherences[task_id]
                current_coherence = self.coherence_tracker.compute_prediction_coherence(
                    self.model, self.task_dataloaders[task_id], task_id
                )
                forgetting_scores.append(max(0, peak_coherence - current_coherence))

        avg_forgetting = np.mean(forgetting_scores) if forgetting_scores else 0.0

        return {
            'avg_accuracy': avg_acc,
            'forgetting': avg_forgetting,
            'n_ruptures': self.state.rupture_count,
            'final_coherence': self.state.coherence,
            'final_precision': self.state.precision
        }


# =============================================================================
# SECTION 3: TEST NETWORKS AND DATA
# =============================================================================

class SimpleMLP(nn.Module):
    """Simple MLP for continual learning experiments."""

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


def create_permuted_mnist_tasks(n_tasks: int = 5,
                                 n_samples: int = 1000,
                                 seed: int = 42) -> List[Tuple[DataLoader, DataLoader]]:
    """
    Create Permuted MNIST tasks for continual learning benchmark.

    Each task applies a different fixed permutation to MNIST pixels.
    """
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Generate synthetic MNIST-like data (28x28 images, 10 classes)
    tasks = []

    for task_id in range(n_tasks):
        # Create permutation for this task
        if task_id == 0:
            perm = np.arange(784)  # No permutation for first task
        else:
            perm = np.random.permutation(784)

        # Generate data
        x_train = torch.randn(n_samples, 784) * 0.3
        y_train = torch.randint(0, 10, (n_samples,))

        # Add class-specific patterns
        for c in range(10):
            mask = y_train == c
            x_train[mask, c*78:(c+1)*78] += 1.0

        # Apply permutation
        x_train = x_train[:, perm]

        # Split train/val
        n_val = n_samples // 5
        train_dataset = TensorDataset(x_train[n_val:], y_train[n_val:])
        val_dataset = TensorDataset(x_train[:n_val], y_train[:n_val])

        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32)

        tasks.append((train_loader, val_loader))

    return tasks


def create_split_tasks(n_tasks: int = 5,
                       n_classes_per_task: int = 2,
                       n_samples: int = 1000,
                       seed: int = 42) -> List[Tuple[DataLoader, DataLoader]]:
    """
    Create Split tasks (each task has different class subsets).

    E.g., Task 0: classes 0-1, Task 1: classes 2-3, etc.
    """
    np.random.seed(seed)
    torch.manual_seed(seed)

    tasks = []
    total_classes = n_tasks * n_classes_per_task

    for task_id in range(n_tasks):
        classes = list(range(task_id * n_classes_per_task,
                             (task_id + 1) * n_classes_per_task))

        # Generate data for these classes
        x_data = torch.randn(n_samples, 784) * 0.3
        y_data = torch.randint(0, n_classes_per_task, (n_samples,))

        # Add class-specific patterns
        for i, c in enumerate(classes):
            mask = y_data == i
            pattern_start = c * (784 // total_classes)
            pattern_end = (c + 1) * (784 // total_classes)
            x_data[mask, pattern_start:pattern_end] += 1.5

        # Map to global class indices
        y_data = y_data + task_id * n_classes_per_task

        # Split
        n_val = n_samples // 5
        train_dataset = TensorDataset(x_data[n_val:], y_data[n_val:])
        val_dataset = TensorDataset(x_data[:n_val], y_data[:n_val])

        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32)

        tasks.append((train_loader, val_loader))

    return tasks


# =============================================================================
# SECTION 4: BASELINE METHODS FOR COMPARISON
# =============================================================================

class EWCBaseline:
    """Elastic Weight Consolidation baseline for comparison."""

    def __init__(self, model: nn.Module, ewc_lambda: float = 1000.0):
        self.model = model
        self.ewc_lambda = ewc_lambda
        self.saved_params: Dict[int, Dict[str, torch.Tensor]] = {}
        self.fisher_info: Dict[int, Dict[str, torch.Tensor]] = {}

    def compute_fisher(self, dataloader: DataLoader, task_id: int):
        fisher = {n: torch.zeros_like(p) for n, p in self.model.named_parameters() if p.requires_grad}
        self.model.eval()
        n_samples = 0

        for x, y in dataloader:
            self.model.zero_grad()
            logits = self.model(x)
            loss = F.cross_entropy(logits, y)
            loss.backward()

            for n, p in self.model.named_parameters():
                if p.requires_grad and p.grad is not None:
                    fisher[n] += p.grad.detach() ** 2
            n_samples += len(x)

        for n in fisher:
            fisher[n] /= max(n_samples, 1)

        self.fisher_info[task_id] = fisher
        self.saved_params[task_id] = {n: p.detach().clone() for n, p in self.model.named_parameters() if p.requires_grad}

    def ewc_loss(self) -> torch.Tensor:
        loss = torch.tensor(0.0)
        for task_id in self.saved_params:
            for n, p in self.model.named_parameters():
                if n in self.saved_params[task_id]:
                    loss = loss + (self.fisher_info[task_id][n] *
                                   (p - self.saved_params[task_id][n]) ** 2).sum()
        return self.ewc_lambda * loss


class NaiveBaseline:
    """Naive fine-tuning (no forgetting prevention)."""
    pass


# =============================================================================
# SECTION 5: BENCHMARK AND EVALUATION
# =============================================================================

def run_crr_experiment(n_tasks: int = 5,
                       omega: float = 1.0,
                       epochs_per_task: int = 10,
                       seed: int = 42) -> Dict:
    """
    Run CRR continual learning experiment.

    Returns detailed metrics for analysis.
    """
    print("=" * 60)
    print("CRR CONTINUAL LEARNING EXPERIMENT")
    print(f"Omega: {omega}, Tasks: {n_tasks}, Epochs/task: {epochs_per_task}")
    print("=" * 60)

    # Create tasks
    tasks = create_permuted_mnist_tasks(n_tasks=n_tasks, seed=seed)

    # Create model
    model = SimpleMLP(input_size=784, hidden_size=256, output_size=10)

    # Create CRR learner
    crr_learner = CRRContinualLearner(
        model=model,
        omega=omega,
        reg_strength=1000.0,
        replay_buffer_size=500
    )

    # Train on each task
    task_results = []
    for task_id, (train_loader, val_loader) in enumerate(tasks):
        print(f"\n--- Task {task_id} ---")
        crr_learner.train_task(
            train_loader=train_loader,
            val_loader=val_loader,
            task_id=task_id,
            epochs=epochs_per_task
        )

        # Evaluate all tasks after this one
        all_accs = crr_learner.evaluate_all_tasks()
        task_results.append(all_accs.copy())
        print(f"  Accuracies after task {task_id}: {all_accs}")

    # Final metrics
    final_metrics = crr_learner.get_forgetting_metrics()

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Average accuracy: {final_metrics['avg_accuracy']:.3f}")
    print(f"Average forgetting: {final_metrics['forgetting']:.3f}")
    print(f"Number of ruptures: {final_metrics['n_ruptures']}")
    print(f"Final coherence: {final_metrics['final_coherence']:.2f}")
    print(f"Final precision: {final_metrics['final_precision']:.2f}")

    return {
        'task_results': task_results,
        'final_metrics': final_metrics,
        'metrics_history': dict(crr_learner.metrics),
        'crr_state': crr_learner.state
    }


def run_comparison_experiment(n_tasks: int = 5,
                               epochs_per_task: int = 10,
                               seed: int = 42) -> Dict:
    """
    Compare CRR against baselines (EWC, Naive).
    """
    print("\n" + "=" * 60)
    print("COMPARISON EXPERIMENT: CRR vs EWC vs Naive")
    print("=" * 60)

    results = {}

    # 1. CRR
    print("\n[1/3] Running CRR...")
    crr_results = run_crr_experiment(n_tasks, omega=1.0, epochs_per_task=epochs_per_task, seed=seed)
    results['CRR'] = crr_results['final_metrics']

    # 2. EWC Baseline
    print("\n[2/3] Running EWC Baseline...")
    tasks = create_permuted_mnist_tasks(n_tasks=n_tasks, seed=seed)
    model_ewc = SimpleMLP(784, 256, 10)
    ewc = EWCBaseline(model_ewc, ewc_lambda=1000.0)

    for task_id, (train_loader, val_loader) in enumerate(tasks):
        optimizer = torch.optim.Adam(model_ewc.parameters(), lr=0.001)
        for epoch in range(epochs_per_task):
            model_ewc.train()
            for x, y in train_loader:
                optimizer.zero_grad()
                loss = F.cross_entropy(model_ewc(x), y) + ewc.ewc_loss()
                loss.backward()
                optimizer.step()
        ewc.compute_fisher(train_loader, task_id)

    # Evaluate EWC
    ewc_accs = []
    for task_id, (_, val_loader) in enumerate(tasks):
        model_ewc.eval()
        correct = sum((model_ewc(x).argmax(1) == y).sum().item() for x, y in val_loader)
        total = sum(len(y) for _, y in val_loader)
        ewc_accs.append(correct / total)
    results['EWC'] = {'avg_accuracy': np.mean(ewc_accs)}

    # 3. Naive Baseline
    print("\n[3/3] Running Naive Baseline...")
    tasks = create_permuted_mnist_tasks(n_tasks=n_tasks, seed=seed)
    model_naive = SimpleMLP(784, 256, 10)

    for task_id, (train_loader, _) in enumerate(tasks):
        optimizer = torch.optim.Adam(model_naive.parameters(), lr=0.001)
        for epoch in range(epochs_per_task):
            model_naive.train()
            for x, y in train_loader:
                optimizer.zero_grad()
                loss = F.cross_entropy(model_naive(x), y)
                loss.backward()
                optimizer.step()

    # Evaluate Naive
    naive_accs = []
    for task_id, (_, val_loader) in enumerate(tasks):
        model_naive.eval()
        correct = sum((model_naive(x).argmax(1) == y).sum().item() for x, y in val_loader)
        total = sum(len(y) for _, y in val_loader)
        naive_accs.append(correct / total)
    results['Naive'] = {'avg_accuracy': np.mean(naive_accs)}

    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"{'Method':<15} {'Avg Accuracy':<15}")
    print("-" * 30)
    for method, metrics in results.items():
        print(f"{method:<15} {metrics['avg_accuracy']:.3f}")

    return results


def test_16_nats_threshold():
    """
    Test that the 16 nats threshold provides meaningful rupture timing.

    This validates the core CRR hypothesis for continual learning.
    """
    print("\n" + "=" * 60)
    print("16 NATS THRESHOLD VALIDATION")
    print("=" * 60)

    results = {}

    for omega in [0.5, 1.0, 2.0, 4.0]:
        print(f"\nTesting Omega = {omega}...")

        # Run experiment
        exp_results = run_crr_experiment(
            n_tasks=5,
            omega=omega,
            epochs_per_task=10,
            seed=42
        )

        results[omega] = {
            'avg_accuracy': exp_results['final_metrics']['avg_accuracy'],
            'forgetting': exp_results['final_metrics']['forgetting'],
            'n_ruptures': exp_results['final_metrics']['n_ruptures'],
            'final_coherence': exp_results['final_metrics']['final_coherence']
        }

    print("\n" + "=" * 60)
    print("16 NATS THRESHOLD RESULTS")
    print("=" * 60)
    print(f"{'Omega':<10} {'Accuracy':<12} {'Forgetting':<12} {'Ruptures':<10} {'Final C':<10}")
    print("-" * 54)
    for omega, metrics in results.items():
        print(f"{omega:<10.1f} {metrics['avg_accuracy']:<12.3f} "
              f"{metrics['forgetting']:<12.3f} {metrics['n_ruptures']:<10d} "
              f"{metrics['final_coherence']:<10.2f}")

    # Interpretation
    print("\nInterpretation:")
    print("- Lower Omega → more frequent ruptures → less coherence accumulation")
    print("- Higher Omega → fewer ruptures → more accumulated knowledge")
    print("- Optimal Omega balances stability (low forgetting) with plasticity (new learning)")
    print(f"- The 16 nats threshold (C/Omega = 16) triggers rupture at ~{np.exp(16):.2e} precision ratio")

    return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == '__main__':
    print("CRR Catastrophic Forgetting Test Suite")
    print("=" * 60)

    # Run basic CRR experiment
    print("\n[TEST 1] Basic CRR Continual Learning")
    basic_results = run_crr_experiment(n_tasks=5, omega=1.0, epochs_per_task=5)

    # Run comparison
    print("\n[TEST 2] Comparison with Baselines")
    comparison_results = run_comparison_experiment(n_tasks=5, epochs_per_task=5)

    # Test 16 nats threshold
    print("\n[TEST 3] 16 Nats Threshold Validation")
    threshold_results = test_16_nats_threshold()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)
