# 🧠 Machine Learning — Quick Reference Notes

> **Core Idea:** ML algorithms learn patterns from data to make predictions or decisions without being explicitly programmed for every scenario.

---

## 1. ML Paradigms Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MACHINE LEARNING                          │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  SUPERVISED  │ UNSUPERVISED │ SEMI-SUPER.  │ REINFORCEMENT  │
│  Labeled     │  No labels   │  Few labels  │  Reward-based  │
│  Data        │  Data        │  + Unlabeled │  Learning      │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

---

## 2. SUPERVISED LEARNING

### 2.1 Regression Models (Predict Continuous Values)

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **Linear Regression** | Models linear relationship y = mx + c | Baseline for regression; data approx. linear | House price prediction, sales forecasting | Simple, interpretable, fast | Assumes linearity, sensitive to outliers |
| **Ridge / Lasso Regression** | L2 / L1 regularization to prevent overfitting | When multicollinearity exists or feature selection needed | Credit scoring, genomic data analysis | Reduces overfitting, feature selection (Lasso) | Requires tuning λ, shrinks coefficients |
| **Polynomial Regression** | Fits non-linear data by adding polynomial features | When relationship is curvilinear | Growth rate prediction, temperature trends | Captures non-linearity | Prone to overfitting if degree too high |
| **Decision Tree Regressor** | Tree-based; splits data on feature thresholds | Non-linear data requiring interpretability | Property valuation, customer lifetime value | Interpretable, no scaling needed | Prone to overfitting, unstable |
| **Random Forest Regressor** | Ensemble of decision trees (bagging) | High accuracy needed; handles missing data well | Stock market prediction, energy load forecasting | Robust, handles non-linearity, feature importance | Computationally heavy, less interpretable |
| **XGBoost / LightGBM Regressor** | Gradient-boosted trees with regularization | State-of-the-art for tabular regression | Revenue prediction, demand forecasting | High accuracy, handles mixed data, fast | Many hyperparameters, prone to overfitting if not tuned |
| **SVR (Support Vector Regressor)** | Finds hyperplane with max margin tolerance | Small-medium datasets with outliers | Financial time series, engine performance | Works well in high dimensions | Poor with large datasets, needs feature scaling |
| **KNN Regressor** | Averages k-nearest neighbors | Low-dimension, small datasets | Recommendations, imputation | Simple, non-parametric | Slow on large data, curse of dimensionality |

---

### 2.2 Classification Models (Predict Discrete Categories)

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **Logistic Regression** | Sigmoid function outputs class probability | Binary classification baseline | Spam detection, churn prediction | Interpretable, efficient, probabilistic output | Assumes linear decision boundary |
| **K-Nearest Neighbors** | Majority vote of k-nearest points | Non-linear boundaries, small datasets | Handwriting recognition, recommendation | No training phase, simple | Sensitive to scale, slow inference |
| **Naïve Bayes** | Assumes conditional independence of features | Text classification (spam, sentiment) | Email filtering, document categorization | Fast, works with high-dim data | Independence assumption rarely holds |
| **Decision Tree Classifier** | Rule-based tree splits on feature thresholds | When interpretability is critical | Loan approval, medical diagnosis | White-box, handles mixed data | High variance, prone to overfitting |
| **Random Forest Classifier** | Ensemble of decision trees (bagging) | High accuracy, handles missing/noisy data | Fraud detection, customer segmentation | Robust, feature importance, handles imbalance | Black-box, memory intensive |
| **XGBoost / LightGBM / CatBoost** | Gradient boosting with optimized trees | Winning Kaggle competitions, tabular data | Ad click prediction, credit risk | State-of-the-art accuracy, handles missing data | Sensitive to hyperparameters |
| **SVM (Support Vector Machine)** | Maximizes margin between classes (kernel trick) | High-dim spaces, clear margin of separation | Image classification, bioinformatics | Effective in high-dims, memory efficient | Poor with overlapping classes, slow training |
| **Neural Networks (MLP)** | Multiple layers of neurons with non-linear activations | Complex patterns, large datasets | Image recognition, NLP | Universal function approximator | Needs big data & compute, black-box |

---

### 2.3 Crucial Evaluation Metrics — Classification

| Metric | Formula / Definition | Best For | Key Insight |
|--------|---------------------|----------|-------------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Balanced classes | Overall correctness |
| **Precision** | TP/(TP+FP) | When false positives are costly (spam) | "How many predicted positives are correct?" |
| **Recall (Sensitivity)** | TP/(TP+FN) | When false negatives are costly (cancer) | "How many actual positives were found?" |
| **F1-Score** | 2×(P×R)/(P+R) | Imbalanced classes | Harmonic mean of precision & recall |
| **ROC-AUC** | Area under TPR vs FPR curve | Ranking quality / model discrimination | "How well model separates classes" |
| **PR-AUC** | Area under Precision-Recall curve | Highly imbalanced datasets | Better than ROC-AUC for rare events |
| **Log Loss** | -∑ y·log(p̂) + (1-y)·log(1-p̂) | Probabilistic classification | Penalizes confident wrong predictions |
| **Confusion Matrix** | TP / FP / FN / TN table | Full diagnostic view | See exactly where model errs |

### 2.4 Crucial Evaluation Metrics — Regression

| Metric | Formula | Best For | Key Insight |
|--------|---------|----------|-------------|
| **MAE** | (1/n)∑\|yᵢ - ŷᵢ\| | When all errors equally important | Average absolute error |
| **MSE** | (1/n)∑(yᵢ - ŷᵢ)² | When large errors penalized more | Sensitive to outliers |
| **RMSE** | √MSE | Same units as target | Most common regression metric |
| **R² (R-Squared)** | 1 - SS_res/SS_tot | Model fit interpretation | Proportion of variance explained |
| **Adjusted R²** | 1 - [(1-R²)(n-1)/(n-k-1)] | Comparing models with different #features | Penalizes adding irrelevant features |
| **MAPE** | (100%/n)∑\|(yᵢ-ŷᵢ)/yᵢ\| | Relative error interpretation | Scale-independent |

---

## 3. UNSUPERVISED LEARNING

### 3.1 Clustering Models

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **K-Means** | Partitions data into k clusters (centroid-based) | Large datasets, spherical clusters | Customer segmentation, image compression | Scalable, fast, simple | Need to choose k, sensitive to outliers |
| **Hierarchical Clustering** | Builds tree of clusters (agglomerative/divisive) | Small datasets, dendrogram visualization | Gene sequencing, taxonomy creation | No k needed, dendrogram output | Expensive O(n³), not for large data |
| **DBSCAN** | Density-based; finds arbitrary shaped clusters | Irregular shaped clusters, noise detection | Anomaly detection, location-based clustering | No k needed, handles noise, arbitrary shapes | Struggles with varying densities |
| **Gaussian Mixture Models** | Soft clustering (probabilistic assignment) | Overlapping clusters, elliptical shapes | Image segmentation, speech recognition | Probabilistic, flexible cluster shape | Needs careful initialization |
| **Mean Shift** | Mode-seeking; no k required | Computer vision, tracking | Object tracking, image segmentation | No k needed, robust to outliers | Computationally expensive |

### 3.2 Dimensionality Reduction

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **PCA** | Linear projection maximizing variance | Reduce multicollinearity, compress data | Face recognition, noise filtering | Fast, decorrelates features | Linear only, hard to interpret components |
| **t-SNE** | Non-linear; preserves local neighborhood | Visualization of high-dim data | Embedding visualization, genomics | Great for 2D/3D visualization | Non-deterministic, slow, not for inference |
| **UMAP** | Non-linear; faster than t-SNE | Visualization + general dimensionality reduction | NLP embeddings, single-cell genomics | Faster than t-SNE, preserves global structure | Relatively new |
| **LDA** | Maximizes class separability | Supervised dimensionality reduction | Face recognition, marketing | Class-aware reduction | Needs labels, assumes Gaussian |

### 3.3 Association Rule Learning

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **Apriori** | Frequent itemset mining | Market basket analysis | Recommender systems, cross-selling | Simple, interpretable | Slow on large datasets |
| **FP-Growth** | Frequent pattern growth (no candidate generation) | Large transaction databases | E-commerce product affinity | Faster than Apriori | More memory intensive |

### 3.4 Evaluation Metrics — Unsupervised

| Metric | Used For | Definition |
|--------|----------|------------|
| **Silhouette Score** | Clustering | Measures cohesion vs separation (-1 to 1) |
| **Inertia / WCSS** | K-Means | Sum of squared distances to cluster centers |
| **Davies-Bouldin Index** | Clustering | Average similarity ratio between clusters (lower = better) |
| **Adjusted Rand Index (ARI)** | Clustering (with ground truth) | Measures similarity of clustering to ground truth |
| **Normalized Mutual Info (NMI)** | Clustering (with ground truth) | Mutual information between clusters and labels |
| **Explained Variance Ratio** | PCA | % of variance captured by each component |
| **Reconstruction Error** | Autoencoders / Dim. Reduction | Error between original and reconstructed data |

---

## 4. SEMI-SUPERVISED LEARNING

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **Self-Training (Pseudo-Labeling)** | Model labels unlabeled data, retrains on high-confidence | Labeled data is scarce | Web page classification, medical imaging | Simple, iterative improvement | Can amplify errors |
| **Co-Training** | Two models on different feature views train each other | Natural feature splits exist | Text classification (content + links) | Leverages multiple views | Needs natural feature split |
| **Label Propagation** | Graph-based; labels propagate through similarity | Small labeled + large unlabeled dataset | Social network labeling, fraud detection | Non-parametric, transductive | Doesn't generalize to new data |
| **MixMatch / FixMatch** | Combines consistency regularization + pseudo-labeling | State-of-the-art semi-supervised | Image classification with few labels | SOTA results, data-efficient | Computationally intensive |

---

## 5. REINFORCEMENT LEARNING

| Model | Key Feature | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|-------------|-----------------|--------|---------|
| **Q-Learning** | Value-based; learns Q(s,a) via Bellman equation | Discrete state/action spaces | Grid-world navigation, simple games | Model-free, proven convergence | Struggles with continuous spaces |
| **Deep Q-Network (DQN)** | Q-Learning + Neural network as function approximator | High-dim state spaces (images) | Atari games, robotics | Handles raw pixels, experience replay | Needs careful tuning, sample inefficient |
| **Policy Gradient (REINFORCE)** | Directly optimizes policy π(a\|s) via gradient ascent | Continuous action spaces, stochastic policies | Robot control, game AI | Handles continuous actions, converges well | High variance, slow |
| **Actor-Critic (A2C/A3C)** | Combines value + policy learning (actor + critic) | Complex continuous control problems | Autonomous driving, trading bots | Lower variance, stable learning | More complex architecture |
| **PPO (Proximal Policy Optimization)** | Clipped surrogate objective for stable updates | Industry standard for RL | LLM fine-tuning (RLHF), robotics | Stable, efficient, SOTA | Hyperparameter sensitive |
| **SAC (Soft Actor-Critic)** | Maximum entropy RL for exploration + robustness | Continuous control, exploration-heavy tasks | Dexterous manipulation | Excellent exploration, sample efficient | Complex implementation |
| **Monte Carlo Tree Search** | Tree search + simulation | Perfect information games | AlphaGo/AlphaZero, chess engines | Strategic planning, no model needed | Computationally expensive |

### 5.1 Evaluation Metrics — Reinforcement Learning

| Metric | Definition | When It Matters |
|--------|------------|-----------------|
| **Cumulative Reward (Return)** | Total discounted sum of rewards | Overall agent performance |
| **Average Reward per Episode** | Mean reward across episodes | Training stability |
| **Episode Length** | Steps until termination | Efficiency (shorter = better for goal tasks) |
| **Success Rate** | % of episodes reaching goal | Task completion |
| **Convergence Speed** | Episodes to reach stable reward | Sample efficiency |
| **Q-Value / Value Estimate** | Learned state/action value | Value function accuracy |
| **Exploration vs Exploitation Ratio** | Actions taken randomly vs greedily | Learning behavior |

---

## 6. ENSEMBLE METHODS (Across Paradigms)

| Method | Key Idea | Models Used | When to Use |
|--------|----------|-------------|-------------|
| **Bagging (Bootstrap Aggregating)** | Train models on bootstrapped samples, average predictions | Decision Trees (Random Forest) | High variance models → reduce overfitting |
| **Boosting** | Sequentially train models to correct previous errors | Decision Trees (XGBoost, AdaBoost) | Bias reduction → improve accuracy |
| **Stacking** | Train meta-model on outputs of base models | Any diverse models | When you want to combine model strengths |
| **Voting (Hard/Soft)** | Majority vote (hard) or average probability (soft) | Any classifiers | Simple ensemble, quick accuracy boost |

---

## 7. HOW TO CHOOSE THE RIGHT MODEL — Decision Flow

```
START: What kind of data do you have?
│
├─ Labeled (X, y available)?
│   ├─ Continuous target? → REGRESSION
│   │   ├─ Linear relationship? → Linear Regression
│   │   ├─ Non-linear, small data? → SVR / Decision Tree
│   │   └─ High accuracy needed? → XGBoost / Random Forest
│   │
│   └─ Categorical target? → CLASSIFICATION
│       ├─ Text data? → Naïve Bayes / Logistic Regression
│       ├─ Image data? → CNN / SVM
│       ├─ Interpretability critical? → Decision Tree / Logistic Regression
│       ├─ Small dataset (<10K)? → SVM / Logistic Regression
│       └─ Large dataset, SOTA accuracy? → XGBoost / LightGBM / Neural Net
│
├─ No labels available?
│   ├─ Need to group data? → CLUSTERING
│   │   ├─ Know number of clusters? → K-Means
│   │   ├─ Don't know k? → DBSCAN / Hierarchical
│   │   └── Want probabilities? → GMM
│   │
│   ├─ Need to compress/visualize? → PCA / t-SNE / UMAP
│   └─ Need association rules? → Apriori / FP-Growth
│
├─ Few labels + lots of unlabeled? → SEMI-SUPERVISED
│   └─ Self-Training / Label Propagation / MixMatch
│
└─ Interactive / sequential decision making? → REINFORCEMENT
    ├─ Discrete actions? → Q-Learning / DQN
    ├─ Continuous actions? → PPO / SAC / A2C
    └─ Game/planning? → MCTS
```

---

## 8. OVERFITTING vs UNDERFITTING — Quick Diagnosis

| Symptom | Problem | Fix |
|---------|---------|-----|
| Low train error, High test error | **Overfitting** | Reduce model complexity, add regularization, more data, early stopping |
| High train error, High test error | **Underfitting** | Increase model complexity, add features, reduce regularization |
| High bias, Low variance | **Underfitting** | More complex model, more features |
| Low bias, High variance | **Overfitting** | Regularization, more data, ensemble |

---

## 9. BIAS-VARIANCE TRADEOFF — Core Principle

```
Error = Bias² + Variance + Irreducible Error

Bias        → Error from wrong assumptions (underfitting)
Variance    → Error from sensitivity to training data (overfitting)

High Bias      = Model is too simple → misses patterns
High Variance  = Model is too complex → learns noise
Goal           = Find the sweet spot
```

---

## 10. KEY FORMULAS REFERENCE CARD

| Concept | Formula |
|---------|---------|
| Linear Regression | y = β₀ + β₁x₁ + ... + βₙxₙ + ε |
| Logistic (Sigmoid) | σ(z) = 1/(1+e⁻ᶻ) |
| Gradient Descent | θⱼ := θⱼ - α·∂J(θ)/∂θⱼ |
| Cross-Entropy Loss | -∑ y·log(ŷ) |
| MSE | (1/n)∑(y - ŷ)² |
| MAE | (1/n)∑\|y - ŷ\| |
| R² | 1 - SS_res/SS_tot |
| Bayes Theorem | P(A\|B) = P(B\|A)·P(A)/P(B) |
| SVM Hinge Loss | max(0, 1 - y·f(x)) |
| Bellman Equation (RL) | V(s) = max[R(s,a) + γ·V(s')] |
| Information Gain | IG = H(parent) - ∑(nᵢ/n)·H(childᵢ) |

---

> **Pro Tip:** For tabular data, start with **Linear/Logistic Regression** (baseline) → **Random Forest** (robust) → **XGBoost/LightGBM** (SOTA). For images → CNNs. For sequences → RNNs/Transformers. For text → Transformers/LLMs.
