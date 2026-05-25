# 🧬 Deep Learning — Quick Reference Notes

> **Core Idea:** Deep Learning uses multi-layered neural networks to automatically learn hierarchical feature representations from raw data.

---

## 1. Neural Network Fundamentals

### 1.1 Architecture of a Neural Network

```
INPUT LAYER       HIDDEN LAYERS          OUTPUT LAYER
    ○              ○ ── ○ ── ○                ○
    ○              ○ ── ○ ── ○                ○
    ○              ○ ── ○ ── ○                ○
    │              │    │    │                 │
  Features    Feature Hierarchy           Predictions
   (x₁..xₙ)   Low→Mid→High Level        (ŷ₁..ŷₘ)
```

| Component | Description |
|-----------|-------------|
| **Input Layer** | Raw features fed into the network |
| **Hidden Layers** | Intermediate layers that learn representations (weights + bias + activation) |
| **Output Layer** | Final prediction layer (softmax for classification, linear for regression) |
| **Weights (W)** | Learnable parameters connecting neurons |
| **Biases (b)** | Learnable offset parameters |
| **Activation Function** | Non-linear transformation (introduces non-linearity) |
| **Loss Function** | Measures prediction error |
| **Optimizer** | Updates weights to minimize loss (e.g., SGD, Adam) |

### 1.2 Forward Propagation — How Prediction Happens

```
z = W·x + b        → Linear transformation
a = f(z)           → Non-linear activation
ŷ = a_output       → Final prediction
Loss = L(y, ŷ)     → Error computation
```

### 1.3 Backpropagation — How Learning Happens

1. Compute loss gradient w.r.t. output ∂L/∂ŷ
2. Chain rule backward through each layer: ∂L/∂W = ∂L/∂ŷ · ∂ŷ/∂z · ∂z/∂W
3. Update weights: W := W - α · ∂L/∂W (Gradient Descent)

---

## 2. Activation Functions

| Activation | Formula | Range | Best For | Pros ✅ | Cons ❌ |
|------------|---------|-------|----------|--------|---------|
| **Sigmoid** | σ(x) = 1/(1+e⁻ˣ) | (0, 1) | Binary classification output | Smooth, probabilistic output | Vanishing gradient, not zero-centered |
| **Tanh** | tanh(x) = (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | (-1, 1) | Hidden layers (older networks) | Zero-centered, stronger gradients | Still vanishing gradient problem |
| **ReLU** | max(0, x) | [0, ∞) | **Default for hidden layers** in most networks | Simple, no vanishing gradient, sparse activation | Dying ReLU (neurons stuck at 0) |
| **Leaky ReLU** | max(αx, x), α≈0.01 | (-∞, ∞) | When dying ReLU is a concern | Fixes dying ReLU | Slightly more computation |
| **ELU** | x if x>0, α(eˣ-1) if x≤0 | (-α, ∞) | Deeper networks needing noise-robust activations | Smooth, negative values push mean toward 0 | More compute than ReLU |
| **Swish / SiLU** | x·σ(x) | (-∞, ∞) | Modern deep networks (EfficientNet, etc.) | Smooth, self-gated, outperforms ReLU | Computationally heavier |
| **GELU** | x·Φ(x) where Φ = CDF of Gaussian | (-∞, ∞) | **Transformer/LLM default** (BERT, GPT) | Smooth, probabilistic gating, SOTA for NLP | Complex computation |
| **Softmax** | eˣⁱ/∑eˣʲ | (0,1), sums to 1 | Multi-class classification output | Converts logits to probabilities | Sensitive to extreme values |

### 2.1 Activation Function Decision Guide

```
OUTPUT LAYER:
├─ Binary Classification → Sigmoid
├─ Multi-class Classification → Softmax
└─ Regression → Linear (no activation)

HIDDEN LAYERS:
├─ CNNs / MLPs → ReLU (default)
├─ Transformers / LLMs → GELU
├─ RNNs / LSTMs → Tanh (default gate)
├─ Dying ReLU problem → Leaky ReLU / ELU
└─ Modern SOTA → Swish / GELU
```

---

## 3. Loss Functions

| Loss | Formula | Used For | Key Property |
|------|---------|----------|-------------|
| **MSE (L2)** | ∑(y-ŷ)² | Regression | Penalizes large errors heavily |
| **MAE (L1)** | ∑\|y-ŷ\| | Regression | Robust to outliers |
| **Huber Loss** | L2 for small errors, L1 for large | Regression with outliers | Combines best of MSE & MAE |
| **Binary Cross-Entropy** | -∑ y·log(ŷ) + (1-y)·log(1-ŷ) | Binary classification | Probabilistic interpretation |
| **Categorical Cross-Entropy** | -∑ y·log(ŷ) | Multi-class classification | Standard for classification |
| **KL Divergence** | ∑ P(x)·log(P(x)/Q(x)) | Distribution matching | Measures how one dist. diverges from another |
| **Contrastive Loss** | y·d² + (1-y)·max(0, margin-d)² | Siamese networks, embeddings | Pushes similar pairs together |
| **Triplet Loss** | max(0, d(a,p) - d(a,n) + margin) | Face recognition, embeddings | Anchor-positive closer than anchor-negative |

---

## 4. Optimizers

| Optimizer | Update Rule | Key Feature | When to Use |
|-----------|-------------|-------------|-------------|
| **SGD** | θ := θ - α·∇L | Simple, vanilla | Baseline, small datasets |
| **SGD + Momentum** | v = βv + ∇L; θ := θ - α·v | Accelerates convergence, smooths updates | When SGD oscillates |
| **AdaGrad** | θ := θ - α·∇L/√(G+ε) | Adaptive per-parameter LR | Sparse data (NLP, embeddings) |
| **RMSProp** | θ := θ - α·∇L/√(E[g²]+ε) | Adaptive LR with decay | Non-stationary objectives (RNNs) |
| **Adam** | Combines Momentum + RMSProp | **Default optimizer** in most DL | Almost everything (default: lr=0.001) |
| **AdamW** | Adam + decoupled weight decay | Better regularization than Adam | Transformers, LLMs |
| **Nadam** | Adam + Nesterov momentum | Faster convergence than Adam | When Adam needs a boost |

> **Rule of Thumb:** Start with **Adam** (lr=0.001). Switch to **SGD+Momentum** for CV tasks. Use **AdamW** for Transformers.

---

## 5. Regularization Techniques

| Technique | How It Works | When to Use | Effect |
|-----------|-------------|-------------|--------|
| **L1 Regularization (Lasso)** | Adds λ∑\|w\| to loss | Feature selection | Sparse weights |
| **L2 Regularization (Weight Decay)** | Adds λ∑w² to loss | General overfitting | Small weights |
| **Dropout** | Randomly drops neurons during training | Large networks, prevent co-adaptation | Ensemble effect |
| **Batch Normalization** | Normalizes layer inputs (μ, σ) per batch | Deeper networks (>10 layers) | Stabilizes training, higher LR |
| **Layer Normalization** | Normalizes across features (not batch) | RNNs, Transformers | Independent of batch size |
| **Early Stopping** | Stop when validation loss stops improving | Always | Prevents overfitting |
| **Data Augmentation** | Artificially increase data via transformations | Image/text data | More robust features |
| **Label Smoothing** | Softens hard labels (e.g., [0,1] → [0.1, 0.9]) | Classification with overconfidence | Better calibration |

---

## 6. Neural Network Architectures

### 6.1 Multi-Layer Perceptron (MLP / Dense Network)

| Aspect | Details |
|--------|---------|
| **What it solves** | Non-linear classification/regression on tabular/structured data |
| **Key feature** | Fully connected layers; universal function approximator |
| **When to use** | Tabular data, small-medium datasets, baseline for DL |
| **Real-world apps** | Credit scoring, customer churn, disease prediction |
| **Pros** | Simple, works well on structured data, interpretable (with tools) |
| **Cons** | Doesn't scale to images/sequences, overfits without regularization |

### 6.2 Convolutional Neural Networks (CNN)

| Aspect | Details |
|--------|---------|
| **Architecture** | Conv → Pooling → Conv → Pooling → Flatten → Dense → Output |
| **What it solves** | Spatial pattern recognition (images, video) |
| **Key feature** | Convolution + Pooling = translation invariance, shared weights |
| **When to use** | Image data, video, any grid-like topology |
| **Popular variants** | **LeNet** (handwriting), **AlexNet** (breakthrough), **VGG** (deep), **ResNet** (skip connections), **Inception** (multi-scale), **EfficientNet** (SOTA efficiency), **YOLO** (object detection) |
| **Real-world apps** | Image classification, object detection, medical imaging, self-driving cars, facial recognition |
| **Pros** | Parameter efficient (weight sharing), translation invariant, hierarchical features |
| **Cons** | Needs lots of data, not for sequential data, interpretability hard |

### 6.3 Recurrent Neural Networks (RNN)

| Aspect | Details |
|--------|---------|
| **Architecture** | Hidden state hₜ = f(W·xₜ + U·hₜ₋₁ + b) |
| **What it solves** | Sequential data processing |
| **Key feature** | Maintains hidden state across time steps; shared weights across time |
| **When to use** | Any sequential data (time series, text, audio) |
| **Real-world apps** | Language modeling, speech recognition, machine translation |
| **Pros** | Handles variable-length sequences, parameter sharing |
| **Cons** | Vanishing/exploding gradients, can't capture long-range dependencies, slow training |

### 6.4 LSTM (Long Short-Term Memory)

| Aspect | Details |
|--------|---------|
| **Architecture** | Cell state + 3 gates: Forget, Input, Output |
| **What it solves** | Long-range dependencies in sequences (solves vanishing gradient) |
| **Key feature** | Gates control information flow; cell state acts as memory |
| **When to use** | Long sequences, time series forecasting, sequence-to-sequence tasks |
| **Real-world apps** | Stock prediction, speech recognition, machine translation, video analysis |
| **Pros** | Captures long-range dependencies, handles variable-length sequences |
| **Cons** | Computationally expensive, 4x parameters of simple RNN, can still overfit |

### 6.5 GRU (Gated Recurrent Unit)

| Aspect | Details |
|--------|---------|
| **Architecture** | 2 gates: Update and Reset (simpler than LSTM) |
| **What it solves** | Same as LSTM but with fewer parameters |
| **Key feature** | Merge forget and input gates → "update gate"; simpler than LSTM |
| **When to use** | When you need LSTM-like performance with less compute |
| **Real-world apps** | Sentiment analysis, language modeling, music generation |
| **Pros** | Faster than LSTM, fewer parameters, comparable performance |
| **Cons** | Slightly less expressive than LSTM on very long sequences |

### 6.6 Autoencoders

| Aspect | Details |
|--------|---------|
| **Architecture** | Encoder → Bottleneck (latent) → Decoder |
| **What it solves** | Unsupervised representation learning, anomaly detection |
| **Key feature** | Learns to compress and reconstruct data (input ≈ output) |
| **When to use** | Dimensionality reduction, denoising, anomaly detection, feature extraction |
| **Popular variants** | **Vanilla AE**, **Denoising AE**, **Variational AE (VAE)** (generative), **Sparse AE** |
| **Real-world apps** | Fraud detection (anomaly), image denoising, data compression |
| **Pros** | Unsupervised, learns meaningful latent representations |
| **Cons** | May simply copy input if too powerful, VAE tricky to train |

### 6.7 Generative Adversarial Networks (GAN)

| Aspect | Details |
|--------|---------|
| **Architecture** | Generator (G) vs Discriminator (D) — adversarial training |
| **What it solves** | Generating realistic synthetic data (images, audio, etc.) |
| **Key feature** | Min-max game between generator and discriminator |
| **When to use** | Image generation, data augmentation, super-resolution, style transfer |
| **Popular variants** | **DCGAN** (conv), **CycleGAN** (style transfer), **StyleGAN** (high-res faces), **pix2pix** (paired translation) |
| **Real-world apps** | Deepfakes, image-to-image translation, drug discovery, art generation |
| **Pros** | Produces sharp, realistic outputs; unsupervised generation |
| **Cons** | Hard to train (mode collapse), unstable, computationally expensive |

### 6.8 Diffusion Models

| Aspect | Details |
|--------|---------|
| **Architecture** | Forward: add noise → Reverse: denoise step by step |
| **What it solves** | High-quality generative modeling (SOTA over GANs) |
| **Key feature** | Markov chain of diffusion steps; stable training |
| **When to use** | Image/video/audio generation where quality matters most |
| **Popular variants** | **DDPM**, **Stable Diffusion** (latent diffusion), **DALL·E 3**, **Imagen** |
| **Real-world apps** | Text-to-image (Midjourney, Stable Diffusion), video generation, molecular design |
| **Pros** | SOTA sample quality, stable training, no mode collapse |
| **Cons** | Slow generation (many steps), high compute cost |

### 6.9 Transformers

| Aspect | Details |
|--------|---------|
| **Architecture** | Self-Attention → FFN → LayerNorm (encoder/decoder stacks) |
| **What it solves** | Sequence modeling without recurrence (parallelizable) |
| **Key feature** | **Self-Attention** mechanism captures all pairwise relationships in one pass |
| **When to use** | NLP, vision (ViT), multi-modal, code generation — **the universal architecture** |
| **Real-world apps** | ChatGPT, BERT, GPT-4, LLaMA, vision transformers, protein folding |
| **Pros** | Parallelizable, captures long-range dependencies, scales with data/compute |
| **Cons** | O(n²) attention cost, needs massive data, compute hungry |
| > *Detailed in NLP/LLM/GenAI reference doc (#3)* |

---

## 7. Architecture Decision Map

```
What type of data?
│
├─ Tabular / Structured Data
│   └─ MLP (Dense Network) → Regularization → Output
│
├─ Images / Spatial Data
│   ├─ Classification → CNN (ResNet / EfficientNet)
│   ├─ Detection → YOLO / Faster R-CNN
│   ├─ Segmentation → U-Net / Mask R-CNN
│   └─ Generation → GAN / Diffusion Model
│
├─ Sequential / Time-Series Data
│   ├─ Short sequences → RNN / GRU
│   ├─ Long sequences → LSTM
│   ├─ Very long / parallel → Transformer
│   └─ Forecasting → LSTM / Temporal CNN
│
├─ Text / Language Data
│   └─ Transformer (BERT / GPT / LLaMA) ← **Always**
│
├─ Audio / Speech
│   ├─ Raw waveform → WaveNet / Audio Transformers
│   └─ Spectrograms → CNN / CRNN
│
└─ Multi-modal (Text + Image + ...)
    └─ Multi-modal Transformer (CLIP, GPT-4V, LLaVA)
```

---

## 8. Crucial Evaluation Metrics — Deep Learning

### 8.1 Classification Metrics (same as ML + DL-specific)

| Metric | Deep Learning Specific Notes |
|--------|------------------------------|
| **Accuracy** | Used when classes are balanced |
| **Precision / Recall / F1** | Standard for imbalanced classification |
| **Top-5 Accuracy** | Common for ImageNet-style classification (if correct class in top 5) |
| **Confusion Matrix** | Full diagnostic for multi-class |
| **AUC-ROC / AUC-PR** | Ranking quality |

### 8.2 Regression Metrics (same as ML)

| Metric | Notes |
|--------|-------|
| **MAE / MSE / RMSE** | Standard regression evaluation |
| **R²** | Proportion of variance explained |
| **SMAPE** | Scale-independent alternative for DL forecasts |

### 8.3 Generation Metrics

| Metric | Used For | How It Works |
|--------|----------|-------------|
| **Perplexity** | Language models | exp(CrossEntropy); lower = better |
| **BLEU** | Machine translation | N-gram precision with brevity penalty |
| **ROUGE** | Summarization | N-gram recall between generated and reference |
| **METEOR** | Translation | Recall + precision with synonym matching |
| **CIDEr** | Image captioning | TF-IDF weighted n-gram similarity |
| **FID (Fréchet Inception Distance)** | Image generation | Distance between real & generated feature distributions |
| **IS (Inception Score)** | Image generation | Quality + diversity of generated images |
| **CLIP Score** | Text-to-image | Alignment between image & text embeddings |

### 8.4 Segmentation / Detection Metrics

| Metric | Used For | Definition |
|--------|----------|------------|
| **IoU (Intersection over Union)** | Segmentation / Detection | Area of Overlap / Area of Union |
| **mAP (mean Average Precision)** | Object detection | Average precision across IoU thresholds |
| **Dice Coefficient** | Medical segmentation | 2·\|A∩B\|/(\|A\|+\|B\|) |

### 8.5 Embedding / Representation Metrics

| Metric | Used For | Definition |
|--------|----------|------------|
| **Silhouette Score** | Clustering quality of embeddings | Cohesion vs separation |
| **Alignment** | Contrastive learning | Distance between positive pairs |
| **Uniformity** | Contrastive learning | How well embeddings fill the space |

---

## 9. Key Deep Learning Concepts

### 9.1 Vanishing & Exploding Gradients

```
Problem: In deep networks, gradients shrink (vanish) → 0 or grow (explode) → ∞
Cause:  Repeated multiplication of gradients through many layers
Fix:    ReLU (less vanishing), Batch/Layer Norm, Residual connections, 
        Gradient clipping, Proper initialization (Xavier/He)
```

### 9.2 Residual Connections (Skip Connections)

```
ResNet: y = F(x) + x
- Gradient can flow directly through the skip connection
- Enables training of very deep networks (100+ layers)
- Standard in modern architectures (ResNet, Transformers)
```

### 9.3 Attention Mechanism

```
Attention(Q, K, V) = softmax(Q·Kᵀ/√dₖ)·V

- Q = Query (what I'm looking for)
- K = Key (what I'm looking at)
- V = Value (what I retrieve)
- Output = Weighted sum of values (weights from Q·K similarity)
```

### 9.4 Transfer Learning

```
Pre-trained model on large dataset → Fine-tune on target task

Benefits: Less data, faster training, better performance
Common: ImageNet pre-trained CNNs, BERT/GPT for NLP
```

### 9.5 Self-Supervised Learning

```
Model creates its own labels from the data structure:
- Masked Language Modeling (BERT): mask words, predict them
- Contrastive Learning (SimCLR): augment images, maximize agreement
- Next Token Prediction (GPT): predict next word

Key: Learns useful representations WITHOUT human labels
```

---

## 10. Training Tips & Tricks

| Challenge | Solution |
|-----------|----------|
| **Model not converging** | Reduce LR, check data preprocessing, try Adam |
| **Overfitting** | Add dropout, weight decay, data augmentation, early stopping |
| **Underfitting** | Increase model capacity, reduce regularization, train longer |
| **Unstable training** | Batch/Layer Normalization, gradient clipping, warmup LR |
| **Class imbalance** | Weighted loss, oversampling, Focal Loss |
| **Slow training** | Larger batch size, mixed precision (FP16), gradient accumulation |
| **Memory issues** | Gradient checkpointing, reduce batch size, use efficient architectures |

### 10.1 Learning Rate Schedules

| Schedule | Behavior | Best For |
|----------|----------|----------|
| **Step Decay** | Drop LR every N epochs | CV tasks |
| **Exponential Decay** | γᵉᵖᵒᶜʰ × initial_lr | Training from scratch |
| **Cosine Annealing** | Cosine curve from max to min LR | SOTA convergence |
| **Warmup + Decay** | Linear warmup → then decay | Transformers, LLMs |
| **ReduceLROnPlateau** | Reduce LR when metric plateaus | Fine-tuning, transfer learning |
| **One-Cycle** | Warmup → LR max → cooldown | Fast training |

---

## 11. Framework Comparison

| Framework | Language | Best For | Key Strength |
|-----------|----------|----------|-------------|
| **PyTorch** | Python | **Default** — research + production | Dynamic graphs, Pythonic, HF ecosystem |
| **TensorFlow/Keras** | Python | Production pipelines, mobile | TF Serving, TFLite, TFX |
| **JAX** | Python | High-performance research | XLA compilation, `vmap`, `pmap` |
| **Keras** | Python | Rapid prototyping | Simple API, runs on top of TF/JAX/PyTorch |

---

> **Pro Tip:** Master the **Transformer** architecture — it's the foundation of ALL modern AI (GPT, BERT, ViT, Whisper, CLIP). If you understand Self-Attention, you understand 80% of today's DL landscape.
