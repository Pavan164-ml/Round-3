# 🗣️ NLP / LLM / GenAI — Quick Reference Notes

> **Core Idea:** From understanding language (NLP) to generating novel content (GenAI) — the evolution of machines that read, write, and create.

---

## 1. EVOLUTION HIERARCHY — Model Map

```
═══════════════════════════════════════════════════════════════════════════════════
                        NLP / LLM / GenAI EVOLUTION MAP
═══════════════════════════════════════════════════════════════════════════════════

1950s-1980s ─── RULE-BASED NLP
    │           ├─ Hand-crafted rules & grammars
    │           ├─ Regular expressions, pattern matching
    │           └─ Limitation: Brittle, doesn't scale, no learning
    │
1990s-2000s ─── STATISTICAL NLP  ← Early Machine Learning
    │           ├─ Naïve Bayes for text classification
    │           ├─ HMM (Hidden Markov Models) for POS tagging
    │           ├─ TF-IDF for information retrieval
    │           ├─ WordNet / Ontologies
    │           └─ Limitation: Needs feature engineering, bag-of-words loses context
    │
2010s ───────── NEURAL NLP (Deep Learning Era)
    │           │
    │           ├── Word Embeddings (Static)
    │           │   ├─ Word2Vec (CBOW / Skip-gram)   ← "King - Man + Woman = Queen"
    │           │   ├─ GloVe (Global Vectors)
    │           │   └─ FastText (subword info)
    │           │
    │           ├── Recurrent Architectures (Sequential)
    │           │   ├─ RNN                     ← Handles sequences, but vanishing gradient
    │           │   ├─ LSTM (Hochreiter, 1997) ← Solves long-range dependencies
    │           │   ├─ GRU (Cho, 2014)         ← Simpler than LSTM, similar performance
    │           │   ├─ BiLSTM / BiGRU          ← Bidirectional context
    │           │   └── Seq2Seq (Sutskever, 2014) ← Encoder-Decoder for translation
    │           │       └─ + Attention (Bahdanau, 2015) ← Focus on relevant parts
    │           │
    │           ├── Convolutional Approaches
    │           │   └─ TextCNN (Kim, 2014)    ← 1D Conv over word embeddings
    │           │
    │           └── Transformer Revolution (Vaswani, 2017) ★★★
    │               └── "Attention Is All You Need"
    │                   ├─ Self-Attention replaces recurrence
    │                   ├─ Parallelizable (unlike RNNs)
    │                   └─ Foundation for everything after
    │
2018-2020 ───── PRE-TRAINING ERA (Transformers split into 2 families)
    │           │
    │           ├── ENCODER-ONLY (Autoencoding / Bidirectional)
    │           │   ├─ BERT (Devlin, 2018)        ★★★
    │           │   │   ├─ Masked LM + Next Sentence Prediction
    │           │   │   ├─ Bidirectional context
    │           │   │   └─ Best for: Understanding tasks
    │           │   ├─ RoBERTa (2019)           ← Optimized BERT (more data, no NSP)
    │           │   ├─ ALBERT (2019)            ← Parameter-efficient BERT
    │           │   ├─ DistilBERT (2019)        ← Distilled BERT (60% faster)
    │           │   └─ ELECTRA (2020)           ← Discriminator-based pre-training
    │           │
    │           ├── DECODER-ONLY (Autoregressive / Causal)
    │           │   ├─ GPT-1 (Radford, 2018)   ← 117M params, proof of concept
    │           │   ├─ GPT-2 (2019)             ← 1.5B, "too dangerous to release"
    │           │   ├─ GPT-3 (2020) ★★★         ← 175B, in-context learning
    │           │   ├─ GPT-3.5 / InstructGPT    ← RLHF alignment
    │           │   └─ GPT-4 (2023) ★★★         ← Multi-modal, SOTA
    │           │
    │           └── ENCODER-DECODER (Seq2Seq)
    │               ├─ T5 (Raffel, 2019)        ← Text-to-Text framework
    │               ├─ BART (Lewis, 2019)       ← Denoising autoencoder
    │               └─ MarianMT / M2M-100       ← Translation specialized
    │
2020-2022 ───── SCALING & EFFICIENCY ERA
    │           │
    │           ├── Efficient Transformers
    │           │   ├─ Longformer             ← Sparse attention for long docs
    │           │   ├─ BigBird                ← Linear attention + sparse
    │           │   ├─ Reformer               ← LSH attention, reversible layers
    │           │   └─ Performer              ← FAVOR+ kernel approximation
    │           │
    │           ├── Large Language Models (100B+)
    │           │   ├─ GPT-3 (175B)           ← In-context learning emergent
    │           │   ├─ PaLM (540B)            ← Pathways architecture
    │           │   ├─ Chinchilla (70B)       ← Optimal compute → more data, smaller model
    │           │   ├─ LLaMA (7B-65B)         ← Open-source, efficient
    │           │   ├─ LLaMA-2 (7B-70B)       ← Chat-optimized, open-source
    │           │   ├─ Falcon (40B-180B)      ← RefinedWeb data
    │           │   └─ GPT-4 (est. 1.7T)      ← Multi-modal, SOTA reasoning
    │           │
    │           └── Training Breakthroughs
    │               ├─ RLHF (Reinforcement Learning from Human Feedback)
    │               ├─ Chain-of-Thought (CoT) Prompting
    │               └─ Scaling Laws (Kaplan, Chinchilla)
    │
2023-2025 ───── CUTTING EDGE (Current Era)
    │           │
    │           ├── Open-Source LLMs
    │           │   ├─ LLaMA-3 / LLaMA-3.1 (8B, 70B, 405B) ★
    │           │   ├─ Mistral / Mixtral (8x7B MoE)        ★
    │           │   ├─ Gemma (Google, 2B-7B)
    │           │   ├─ Qwen / Qwen2 (Alibaba)
    │           │   ├─ DeepSeek / DeepSeek-V2 / V3         ★★
    │           │   ├─ Yi (01.AI)
    │           │   ├─ Phi-3 / Phi-4 (Microsoft, small + capable)
    │           │   └─ Command R+ (Cohere)
    │           │
    │           ├── Mixture of Experts (MoE)
    │           │   ├─ Mixtral 8x7B              ← Only activates 2/8 experts per token
    │           │   ├─ GPT-4 (rumored MoE)
    │           │   ├─ DeepSeek-MoE / DeepSeek-V2
    │           │   └─ Qwen1.5-MoE
    │           │
    │           ├── Multi-Modal Models
    │           │   ├─ GPT-4V / GPT-4o          ★★★ Text + Image + Audio
    │           │   ├─ Gemini (Ultra, Pro, Nano) ★★★ Google's multi-modal
    │           │   ├─ Claude 3 / 3.5 Opus       ★★★ Vision + Text
    │           │   ├─ LLaVA                    ← Open-source VLM
    │           │   ├─ DALL·E 3                 ← Text-to-Image
    │           │   ├─ Stable Diffusion 3       ← Open-source T2I
    │           │   ├─ Midjourney               ← SOTA image generation
    │           │   └─ Sora (OpenAI)            ← Text-to-Video
    │           │
    │           ├── Reasoning Models ★★★
    │           │   ├─ o1 (OpenAI)              ← Chain-of-Thought reasoning
    │           │   ├─ o3 (OpenAI)              ← Advanced reasoning
    │           │   ├─ DeepSeek-R1              ← Open reasoning model
    │           │   └─ Gemini 2.0 Flash Thinking ← Fast reasoning
    │           │
    │           ├── Long Context Models
    │           │   ├─ Gemini 1.5 Pro           ← 10M tokens context
    │           │   ├─ Claude 3                 ← 200K tokens
    │           │   ├─ GPT-4-128K               ← 128K tokens
    │           │   └─ Yi-34B-200K              ← 200K open-source
    │           │
    │           └── Small Language Models (SLMs)
    │               ├─ Phi-3 Mini (3.8B)        ← Beats larger models on benchmarks
    │               ├─ Gemma 2 (2B, 9B)
    │               ├─ TinyLlama (1.1B)
    │               └── MobileLLM / On-device AI
    │
    FUTURE ────── NEXT FRONTIERS
                ├─ World Models / World Simulators
                ├─ Agentic AI (AutoGPT, LangChain Agents)
                ├─ AI Agents (Multi-agent systems)
                ├─ Test-Time Compute Scaling
                ├─ Liquid Neural Networks
                ├─ Self-Improving / Self-Playing AI
                └─ AGI (Artificial General Intelligence)

═══════════════════════════════════════════════════════════════════════════════════
```

---

## 2. DETAILED MODEL BREAKDOWN

### 2.1 Word Embeddings (Static)

| Model | Key Feature | Problem Solved | When to Use | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|-------------|----------------|-------------|-----------------|--------|---------|
| **Word2Vec** | Neural word embeddings with CBOW/Skip-gram | Capture semantic similarity between words | Baseline embedding for NLP pipelines | Search engines, recommendation systems | Fast, captures analogies, pre-trained available | Static (one vector per word), no context |
| **GloVe** | Matrix factorization on word co-occurrence | Leverages global corpus statistics | When global statistics matter more than local context | Document classification, semantic similarity | Captures global patterns, pre-trained available | Static, needs large corpus |
| **FastText** | Subword n-gram embeddings | Handle out-of-vocabulary (OOV) words | Morphologically rich languages (German, Turkish) | Text classification for rare words, spell checking | Handles OOV, fast, subword info | Larger model size than Word2Vec |

---

### 2.2 Recurrent Architectures

| Model | Year | Key Feature | Problem Solved | When to Use | Pros ✅ | Cons ❌ |
|-------|------|-------------|----------------|-------------|--------|---------|
| **RNN** | 1986 | Hidden state across time steps | Sequence modeling | Short sequences, simple time series | Simple, handles variable length | Vanishing gradient, no long-range memory |
| **LSTM** | 1997 | Forget/Input/Output gates + cell state | Long-range dependencies (vanishing gradient) | Time series, speech, text with long context | Captures long-range dependencies | 4x param of RNN, slow, overfits |
| **GRU** | 2014 | Update/Reset gates (simpler than LSTM) | Same as LSTM with fewer params | Quicker training, moderate-length sequences | Faster than LSTM, fewer params, similar perf | Less expressive on very long sequences |
| **BiLSTM** | — | Forward + backward LSTM | Need context from both directions | NER, POS tagging, QA | Full context (past + future) | Not causal, can't generate sequentially |
| **Seq2Seq** | 2014 | Encoder → Decoder architecture | Variable-length input → output | Translation, summarization, chatbots | Flexible input/output lengths | Single context vector bottleneck |
| **Seq2Seq + Attention** | 2015 | Soft alignment between encoder & decoder | Information bottleneck in Seq2Seq | Machine translation, summarization | Better focus, handles long inputs | Still sequential → slow training |

---

### 2.3 Transformer Architecture (The Game Changer) ★★★

```
TRANSFORMER ARCHITECTURE (Vaswani et al., 2017)
═══════════════════════════════════════════════════
                    OUTPUT
                       ▲
                    ┌─────┐
                    │ FC  │
                    └─────┘
                       ▲
              ┌──────────────────┐
              │  Add & LayerNorm  │
              └──────────────────┘
                       ▲
              ┌──────────────────┐
              │  Feed Forward    │
              └──────────────────┘
                       ▲
              ┌──────────────────┐
              │  Add & LayerNorm  │
              └──────────────────┘
                       ▲
              ┌──────────────────┐
              │ Multi-Head       │
              │ Self-Attention   │ ← ★ Core Innovation
              └──────────────────┘
                       ▲
                   INPUT
               (Token Emb + Pos Emb)

Self-Attention: Attention(Q,K,V) = softmax(Q·Kᵀ/√dₖ)·V
- Q, K, V from same sequence
- Each token "attends" to ALL other tokens
- O(n²) complexity but fully parallelizable
═══════════════════════════════════════════════════
```

| Component | What It Does | Why It Matters |
|-----------|-------------|----------------|
| **Self-Attention** | Each token looks at every other token | Captures all pairwise relationships in O(1) steps |
| **Multi-Head Attention** | 8-128 parallel attention "views" | Learns different relationship types (syntax, semantics, etc.) |
| **Positional Encoding** | Sine/cosine or learned position signals | Gives order information (since no recurrence) |
| **Feed-Forward Network** | MLP applied per token | Adds non-linearity and capacity |
| **Layer Normalization** | Normalizes across features | Stable training, independent of batch size |
| **Residual Connections** | Skip connections around each block | Enables deep stacking (gradient flow) |
| **Masked Self-Attention** | Future tokens hidden (in decoder) | Ensures autoregressive generation |

---

### 2.4 Encoder-Only Models (Understanding Focused)

| Model | Year | Params | Key Feature | Best For | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|------|--------|-------------|----------|-----------------|--------|---------|
| **BERT** | 2018 | 110M-340M | Masked LM + bidirectional context | Classification, NER, QA, entailment | Google Search, sentiment analysis | SOTA understanding, pre-trained, fine-tunable | Expensive to train, 512 token limit |
| **RoBERTa** | 2019 | 125M-355M | BERT optimized (more data, no NSP) | Same as BERT (better) | Text classification, NER | Better than BERT on most benchmarks | Same architecture, larger compute |
| **ALBERT** | 2019 | 12M-235M | Parameter sharing, factorized embeddings | Resource-constrained environments | Mobile NLP, edge devices | 18x fewer params than BERT | Slightly lower accuracy |
| **DistilBERT** | 2019 | 67M | Knowledge distillation (60% faster, 95% perf) | Real-time inference | Chatbots, real-time classification | 60% faster, 40% smaller | Slightly less accurate |
| **ELECTRA** | 2020 | 110M-335M | Discriminator replaces masked tokens | Efficient pre-training | Text classification, NER | More sample-efficient than BERT | Complex training (generator + discriminator) |
| **DeBERTa** | 2021 | 100M-1.5B | Disentangled attention + enhanced mask decoder | SOTA understanding benchmarks | SuperGLUE, MNLI | Outperforms BERT/RoBERTa on many benchmarks | More complex architecture |

---

### 2.5 Decoder-Only Models (Generation Focused) — The GPT Family

| Model | Year | Params | Key Breakthrough | Best For | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|------|--------|-----------------|----------|-----------------|--------|---------|
| **GPT-1** | 2018 | 117M | Generative pre-training proof of concept | Text generation, classification | Experimental | Showed pre-training works | Small, limited capabilities |
| **GPT-2** | 2019 | 1.5B | Zero-shot task transfer (without fine-tuning) | Text generation, story completion | Writing assistants | Coherent long-form text, zero-shot | "Too dangerous" initially withheld |
| **GPT-3** | 2020 | 175B | **In-context learning** (few-shot prompting) | Few-shot NLP tasks | Code generation, translation, Q&A | Emergent abilities, no fine-tuning needed | Expensive ($), 2048 token limit |
| **InstructGPT** | 2022 | 175B | **RLHF** alignment with human preferences | Instruction following | ChatGPT precursor | More helpful, honest, safe | Complex human feedback pipeline |
| **GPT-3.5** | 2022 | — | Codex + InstructGPT combined | General-purpose chat, code | **ChatGPT** (launched Nov 2022) | Conversational, code-savvy | Still hallucinates, limited context |
| **GPT-4** | 2023 | ~1.7T (est.) | Multi-modal (text + image), SOTA reasoning | Any NLP task, document analysis, vision | ChatGPT Plus, Bing Chat | Better reasoning, 25K tokens, vision | Expensive, slower, less transparent |
| **GPT-4o** | 2024 | — | Omni (text + vision + audio) real-time | Real-time multi-modal conversation | Voice mode, vision chat | Real-time audio, faster, cheaper | — |
| **o1** | 2024 | — | Chain-of-Thought reasoning at inference time | Complex math, coding, science | Research, coding, math | Breaks down complex problems | Slower, expensive |
| **o3** | 2025 | — | Advanced reasoning + test-time compute scaling | Cutting-edge reasoning tasks | Scientific discovery | SOTA reasoning | Extremely expensive |

---

### 2.6 Encoder-Decoder Models (Seq2Seq)

| Model | Year | Key Feature | Best For | Real-World Apps | Pros ✅ | Cons ❌ |
|-------|------|-------------|----------|-----------------|--------|---------|
| **T5** | 2019 | Text-to-Text framework (everything is "translate X to Y") | Translation, summarization, QA, classification | Google products, Flan-T5 | Unified framework, strong on many tasks | Large, all tasks need prefix |
| **BART** | 2019 | Denoising autoencoder (corrupt → reconstruct) | Summarization, translation, generation | Facebook/Meta summarization | Combines BERT + GPT strengths | Complex pre-training |
| **mT5** | 2021 | Multilingual T5 (101 languages) | Cross-lingual NLP | Translation, multilingual search | Covers many languages | Larger model, data hungry |

---

### 2.7 Open-Source LLMs (2023-2025)

| Model | Creator | Params | Key Feature | Best For | Pros ✅ | Cons ❌ |
|-------|---------|--------|-------------|----------|--------|---------|
| **LLaMA** | Meta | 7B-65B | Efficient, open-source, strong perf for size | Research, fine-tuning | Free, punchy for size, efficient | License restrictions initially |
| **LLaMA-2** | Meta | 7B-70B | Chat-tuned, open-source, commercial friendly | Chat apps, fine-tuning | Commercial use, better safety | Still behind GPT-4 |
| **LLaMA-3 / 3.1** | Meta | 8B-405B | SOTA open-source, 128K context, tool use | Enterprise, on-premise | 405B rivals GPT-4, open-weight | Huge compute for 405B |
| **Mistral 7B** | Mistral AI | 7B | Beats LLaMA-2 13B on most benchmarks | Efficient deployment | Best 7B model, fast, efficient | Smaller model limits |
| **Mixtral 8x7B** | Mistral AI | 46B (MoE) | Mixture of Experts (only 12B active per token) | Cost-effective high quality | Quality of 46B, cost of 12B | MoE complexity |
| **DeepSeek-V2/V3** | DeepSeek | 236B (MoE) / 671B (MoE) | Multi-head latent attention, SOTA efficiency | Code, reasoning, general chat | Beats GPT-4 on coding tasks | Limited ecosystem |
| **DeepSeek-R1** | DeepSeek | — | Open reasoning model (like o1) | Math, science, code | Open-source reasoning | — |
| **Gemma** | Google | 2B-7B | Built on Gemini research, lightweight | On-device, mobile | Lightweight, well-documented | Smaller capacity |
| **Qwen 2.5** | Alibaba | 0.5B-72B | Strong multilingual, long context | Chinese + English, code | Strong coding, multilingual | Less Western adoption |
| **Phi-3 / Phi-4** | Microsoft | 3.8B-14B | Small but capable (trained on synthetic data) | Edge, mobile, cheap inference | Tiny but powerful | Limited to simple tasks |
| **Command R+** | Cohere | 104B | RAG-optimized, multilingual | Enterprise RAG, search | Excellent RAG, tool use | Not general-purpose SOTA |
| **Yi / Yi-1.5** | 01.AI | 6B-34B | Strong Chinese + English bilingual | Bilingual applications | Good quality, 200K context variant | Smaller community |

---

### 2.8 Multi-Modal Models

| Model | Creator | Modalities | Key Feature | Best For | Pros ✅ | Cons ❌ |
|-------|---------|-----------|-------------|----------|--------|---------|
| **GPT-4V / GPT-4o** | OpenAI | Text + Image + Audio | Vision understanding, real-time speech | Document analysis, visual QA, voice | Best all-around multi-modal | Expensive, closed |
| **Gemini Ultra / Pro** | Google | Text + Image + Audio + Video | Native multi-modal (trained on all modalities) | Multi-modal reasoning, video understanding | Native multi-modal (not stitched) | Still catching up to GPT-4 |
| **Claude 3 / 3.5** | Anthropic | Text + Image | Vision, long context (200K), safety | Document analysis, coding, safety-conscious | Best safety, long context, honest | No audio yet |
| **LLaVA** | UW/Columbia | Text + Image | Open-source vision-language | Open-source VLM research | Free, fine-tunable, strong | Smaller than GPT-4V |
| **DALL·E 3** | OpenAI | Text → Image | SOTA text-to-image alignment | Image generation, design | Best prompt following, photorealistic | Closed, expensive |
| **Stable Diffusion 3** | Stability AI | Text → Image | Open-source diffusion, 8B params | Open-source image gen | Free, controllable, fine-tunable | Quality behind DALL·E 3 |
| **Midjourney** | Midjourney | Text → Image | Artistic quality, aesthetic taste | Creative design, art | Best aesthetics, community | Closed, no API |
| **Sora** | OpenAI | Text → Video | Realistic video generation from text | Video creation, simulation | Photorealistic physics simulation | Limited access, expensive |
| **CLIP** | OpenAI | Text + Image | Contrastive text-image embeddings | Zero-shot classification, search | Connects text + image modalities | Not generative |

---

## 3. KEY CONCEPTS & TECHNIQUES

### 3.1 Attention Variants

| Type | Complexity | Best For | Description |
|------|-----------|----------|-------------|
| **Full Self-Attention** | O(n²) | Short sequences (< 1K) | Every token attends to every token |
| **Sparse Attention** | O(n√n) or O(n log n) | Long documents | Only attends to local + selected distant tokens |
| **Sliding Window Attention** | O(n·w) | Streaming, long sequences | Attends only to w neighbors (Mistral uses this) |
| **Cross-Attention** | O(n·m) | Encoder-Decoder | Decoder attends to encoder outputs |
| **Flash Attention** | O(n²) but 2x+ faster | All Transformers | GPU-optimized attention (IO-aware) — **always use** |
| **Grouped Query Attention (GQA)** | O(n²) but less KV cache | LLM inference | Multiple queries share keys/values (LLaMA-2/3, Mistral) |
| **Multi-Query Attention (MQA)** | O(n²) but even less KV cache | Ultra-fast inference | All queries share same key/value (PaLM) |

### 3.2 Pre-Training Objectives

| Objective | Used By | Description |
|-----------|---------|-------------|
| **Masked LM (MLM)** | BERT, RoBERTa | Mask 15% of tokens, predict them (bidirectional) |
| **Causal LM (Autoregressive)** | GPT, LLaMA | Predict next token given previous tokens (left-to-right) |
| **Permutation LM** | XLNet | Predict tokens in random order (combines MLM + AR) |
| **Denoising Autoencoder** | BART | Corrupt text → reconstruct original |
| **Text-to-Text** | T5 | All tasks framed as "input → output" |
| **Contrastive Learning** | CLIP, SimCSE | Maximize agreement between positive pairs |
| **RLHF** | InstructGPT, ChatGPT | Fine-tune with human preference reward model |

### 3.3 Training Paradigms

```
Pre-Training ─────────────> Fine-Tuning ────────────> Alignment
    │                             │                         │
    │                             │                         │
Massive data (internet)      Task-specific data        Human preferences
Expensive ($1M+)             Cheap ($100-$1K)           RLHF / DPO
General knowledge            Task adaptation           Safety, helpfulness
Self-supervised              Supervised                 Preference-based
```

### 3.4 Parameter-Efficient Fine-Tuning (PEFT)

| Method | How It Works | Parameter Savings | Best For |
|--------|-------------|-------------------|----------|
| **LoRA** | Low-rank adaptation matrices (A·B) injected into attention | ~0.1-1% of full fine-tuning | Most common PEFT method; fine-tune adapters, keep base frozen |
| **QLoRA** | LoRA + 4-bit quantization (NF4) | ~0.1% + 4x memory reduction | Fine-tuning 65B models on single GPU |
| **Adapters** | Small bottleneck layers inserted between Transformer layers | ~3-6% | Multi-task serving (swap adapters) |
| **Prefix Tuning** | Learnable virtual tokens prepended to input | ~0.1% | Prompt-based adaptation |
| **Prompt Tuning** | Learnable soft prompts (no model changes) | ~0.01% | Very lightweight, no model weights stored |
| **IA³** | Learned vectors rescale key/value/FFN activations | ~0.01% | Extremely lightweight |

### 3.5 Quantization Techniques

| Method | Precision | Memory Reduction | Quality Loss | Best For |
|--------|-----------|-----------------|--------------|----------|
| **FP32** | 32-bit | 1x (baseline) | None | Training |
| **FP16 / BF16** | 16-bit | 2x | Negligible | Training + inference |
| **INT8** | 8-bit | 4x | Minor | Inference |
| **INT4 (GPTQ, AWQ)** | 4-bit | 8x | Small | Inference on consumer GPUs |
| **NF4 (QLoRA)** | 4-bit NormalFloat | 8x | Very small | Fine-tuning on single GPU |

### 3.6 Prompting Techniques

| Technique | Description | When to Use |
|-----------|-------------|-------------|
| **Zero-Shot** | "Translate this to French: Hello" | Simple tasks, capable models |
| **Few-Shot** | Provide 2-5 examples in the prompt | Complex tasks, guide output format |
| **Chain-of-Thought (CoT)** | "Let's think step by step" | Math, logic, reasoning tasks |
| **Tree-of-Thought (ToT)** | Explore multiple reasoning paths | Complex problem solving |
| **ReAct** | Reasoning + Acting (think, act, observe) | Agent tasks (tool use) |
| **Self-Consistency** | Generate multiple CoT paths → majority vote | Improving reasoning reliability |
| **Retrieval-Augmented Generation (RAG)** | Retrieve relevant docs → augment prompt | Knowledge-intensive tasks, reduce hallucinations |
| **System Prompt** | Set behavior, tone, constraints | Consistent assistant behavior |

### 3.7 Retrieval-Augmented Generation (RAG) ★★

```
USER QUERY
    │
    ▼
┌─────────────────────┐     ┌─────────────────┐
│   Embedding Model   │────>│  Vector Database │
│   (e.g., text-embed-│     │  (Pinecone,      │
│    ding-3-small)    │     │   Chroma,        │
└─────────────────────┘     │   Weaviate)      │
                            └────────┬────────┘
                                     │ Top-K relevant docs
                                     ▼
┌────────────────────────────────────────────────┐
│        LLM Prompt = Query + Retrieved Docs     │
│  "Answer based on these documents: {docs}      │
│   Question: {query}"                           │
└────────────────────┬───────────────────────────┘
                     │
                     ▼
               FINAL ANSWER
        (grounded in retrieved knowledge)
```

| RAG Component | Options | Purpose |
|--------------|---------|---------|
| **Embedding Model** | text-embedding-3-small, BGE, E5, Instructor | Convert text to vectors |
| **Vector DB** | Chroma, Pinecone, Weaviate, Qdrant, Milvus | Store & search embeddings |
| **Retrieval** | Dense (semantic), Sparse (BM25), Hybrid | Find relevant docs |
| **Chunking Strategy** | Fixed size, semantic, recursive | Split documents optimally |
| **RAG Mode** | Naive, Advanced (re-rank), Agentic | Complexity of pipeline |

---

## 4. CRUCIAL EVALUATION METRICS

### 4.1 Language Generation Metrics

| Metric | What It Measures | Formula / Approach | Best For | Limitation |
|--------|-----------------|-------------------|----------|------------|
| **Perplexity** | How "surprised" model is by text | exp(-1/n ∑ log P(wᵢ\|context)) | Language model quality | Doesn't measure generation quality |
| **BLEU** | N-gram precision with brevity penalty | Precision-based, up to 4-grams | Machine translation | Favors shorter, exact matches |
| **ROUGE-1/2/L** | N-gram recall (ROUGE-L = longest common subsequence) | Recall-based | Summarization | Favors longer, doesn't capture semantics |
| **METEOR** | Precision + Recall + Synonym matching | Aligns words, considers synonyms | Translation, summarization | More correlation with human judgment |
| **CIDEr** | TF-IDF weighted n-gram similarity | Consensus-based | Image captioning | Domain specific |
| **BERTScore** | BERT embedding similarity | Cosine similarity of BERT embeddings | Any generation task | Correlates better with human judgment |
| **BLEURT** | Learned metric based on BERT | Fine-tuned BERT for evaluation | Generation quality | Needs training data |
| **G-Eval** | LLM-as-judge (GPT-4 evaluates) | Prompt LLM to score | Fluency, coherence, relevance | Expensive, model bias |

### 4.2 LLM-Specific Benchmarks

| Benchmark | What It Tests | Example Tasks | Models Tested |
|-----------|--------------|---------------|---------------|
| **MMLU** | Multi-task language understanding | 57 subjects (STEM, humanities, etc.) | GPT-4, LLaMA, Gemma |
| **HellaSwag** | Commonsense reasoning (choose correct ending) | "A woman is slicing onions..." | All LLMs |
| **HumanEval / MBPP** | Code generation | Write function from docstring | Code LLMs |
| **GSM8K** | Grade-school math word problems | Multi-step arithmetic | GPT-4, o1, DeepSeek |
| **MATH** | Competition-level math | Advanced math problems | o1, DeepSeek-R1 |
| **BIG-Bench** | 204 diverse tasks | Logic, biology, physics | Frontier models |
| **TruthfulQA** | Truthfulness (avoids common misconceptions) | "What is the capital of Australia?" | Safety evaluation |
| **MT-Bench** | Multi-turn chat quality | LLM-as-judge scoring | Chat models |
| **AlpacaEval** | Instruction following | Length-controlled win rate | Instruction-tuned models |
| **SWE-Bench** | Real-world software engineering | GitHub issues → PRs | Coding agents |

### 4.3 RAG Evaluation Metrics

| Metric | What It Measures | How |
|--------|-----------------|-----|
| **Hit Rate / Recall@K** | Did we retrieve relevant documents? | % of queries where relevant doc is in top-K |
| **MRR (Mean Reciprocal Rank)** | Rank of first relevant document | 1/rank averaged |
| **NDCG (Normalized Discounted Cumulative Gain)** | Ranking quality with graded relevance | Position-weighted relevance score |
| **Faithfulness / Groundedness** | Is the answer supported by retrieved docs? | NLI model checks claim vs context |
| **Answer Relevance** | Does answer address the query? | Embedding similarity between answer and query |
| **Context Precision/Recall** | Quality of retrieved context | Precision = relevant/total retrieved |

### 4.4 Safety & Alignment Metrics

| Metric | What It Measures | Description |
|--------|-----------------|-------------|
| **Refusal Rate** | Does model refuse harmful requests? | % of harmful prompts correctly refused |
| **Toxicity Score** | Offensive content detection | Perspective API score |
| **Bias Evaluation** | Demographic bias (gender, race) | BBQ, WinoBias benchmarks |
| **Truthfulness** | Factual accuracy | TruthfulQA benchmark |
| **Helpfulness** | How useful are responses? | Human evaluation / LLM-as-judge |

---

## 5. WHAT PROBLEM DOES EACH SOLVE — At a Glance

| Problem | Solution | Model Family |
|---------|----------|-------------|
| Understanding text (classification, NER, QA) | **Encoder models** (BERT, RoBERTa, DeBERTa) | BERT family |
| Generating coherent text | **Decoder models** (GPT, LLaMA, Mistral) | GPT family |
| Translating between languages | **Encoder-Decoder** (T5, BART, Marian) | Seq2Seq family |
| Summarizing long documents | **Long-context LMs** (Gemini 1.5, Claude 3) | Long context |
| Answering from knowledge base | **RAG pipelines** (Retrieval + LLM) | Hybrid |
| Generating images from text | **Diffusion models** (DALL·E, Stable Diffusion, Midjourney) | Image Gen |
| Generating video from text | **Video diffusion** (Sora, Runway Gen-3) | Video Gen |
| Code generation | **Code LLMs** (Codex, DeepSeek-Coder, CodeLlama) | Code |
| Reasoning / math | **Reasoning models** (o1, o3, DeepSeek-R1) | Reasoning |
| Multi-modal understanding | **VLM** (GPT-4V, Gemini, Claude 3, LLaVA) | Multi-modal |
| Running on device / edge | **SLMs** (Phi-3, Gemma 2, TinyLlama) | Small LMs |
| Following complex instructions | **Instruction-tuned + RLHF** (GPT-4, Claude 3.5) | Aligned LMs |
| Real-time conversation with voice/vision | **Omni models** (GPT-4o) | Multi-modal real-time |
| Efficient fine-tuning | **PEFT** (LoRA, QLoRA, Adapters) | Fine-tuning methods |
| Cost-effective large models | **MoE** (Mixtral, DeepSeek-V2, GPT-4) | Sparse models |

---

## 6. WHEN TO USE WHAT — Decision Flow

```
What NLP/AI task do you need?
│
├─ TEXT UNDERSTANDING (Classification, NER, QA, Sentiment)
│   ├─ Need speed / small deployment? → DistilBERT / TinyBERT
│   ├─ Need best accuracy? → DeBERTa / RoBERTa / BERT Large
│   └─ Multi-lingual? → XLM-R / mBERT
│
├─ TEXT GENERATION (Chat, Writing, Creative)
│   ├─ API-based (quality matters)? → GPT-4 / Claude 3.5 / Gemini
│   ├─ Open-source / self-hosted?
│   │   ├─ Have GPU (7B-8B)? → LLaMA-3-8B / Mistral-7B / Gemma-2-9B
│   │   ├─ Have GPU (70B)? → LLaMA-3-70B / Mixtral 8x7B
│   │   ├─ Need best open-source? → LLaMA-3-405B (needs many GPUs)
│   │   └─ Budget conscious? → Phi-3 / DeepSeek-V2
│   └─ Reasoning heavy (math, code, science)? → o1 / DeepSeek-R1 / o3
│
├─ SUMMARIZATION
│   ├─ Short text → BART / T5
│   ├─ Long document → Gemini 1.5 Pro (10M ctx) / Claude 3 (200K)
│   └─ Extractive → BERT-based extractor
│
├─ TRANSLATION
│   └─ T5 / MarianMT / M2M-100 / GPT-4
│
├─ CODE GENERATION
│   ├─ API? → GPT-4 / Claude 3.5 Sonnet
│   ├─ Open-source? → DeepSeek-Coder / CodeLlama / StarCoder
│   └─ Code completion in IDE → Codex / TabNine
│
├─ SEARCH / RAG
│   ├─ Need grounding → RAG with LLM
│   ├─ Need retrieval? → Embedding Model (text-embedding-3, BGE) + Vector DB
│   └─ Enterprise knowledge → Command R+ / RAG-fine-tuned models
│
├─ IMAGE GENERATION
│   ├─ Artistic quality? → Midjourney
│   ├─ Prompt following? → DALL·E 3
│   ├─ Open-source / controllable? → Stable Diffusion 3 / Flux
│   └─ Editing/in-painting? → Stable Diffusion + ControlNet
│
├─ MULTI-MODAL (Text + Image)
│   ├─ API? → GPT-4V / GPT-4o / Claude 3.5 / Gemini
│   └─ Open-source? → LLaVA / Qwen-VL / InternVL
│
├─ AUDIO / SPEECH
│   ├─ Speech-to-Text → Whisper (OpenAI)
│   ├─ Text-to-Speech → ElevenLabs / Bark / VALL-E
│   └─ Music generation → MusicGen / Suno AI
│
└─ VIDEO GENERATION
    ├─ Realistic → Sora / Kling (Kuaishou)
    └─ Creative → Runway Gen-3 / Pika Labs
```

---

## 7. ADVANTAGES & DISADVANTAGES — LLMs / GenAI

### 7.1 Advantages ✅

| Advantage | Description |
|-----------|-------------|
| **Emergent Abilities** | At scale (>70B), models develop capabilities not present in smaller versions (reasoning, in-context learning, instruction following) |
| **Few-Shot / Zero-Shot** | Can perform tasks with little to no task-specific training data |
| **Transfer Learning** | Pre-trained knowledge transfers to many downstream tasks |
| **Scalability** | Performance improves predictably with more data, compute, and parameters (Scaling Laws) |
| **Multi-Task** | One model can handle thousands of tasks simultaneously |
| **Creativity** | Can generate novel content, stories, code, art |
| **Accessibility** | APIs make SOTA AI available to anyone without ML expertise |
| **Rapid Progress** | New SOTA models released every few months |

### 7.2 Disadvantages ❌

| Disadvantage | Description | Mitigation |
|-------------|-------------|-----------|
| **Hallucination** | Model generates false/confident incorrect information | RAG, grounding, factual consistency checking |
| **Computational Cost** | Training costs $1M-$100M; inference expensive | Quantization, distillation, smaller models |
| **Data Hunger** | Needs trillions of tokens for training | Synthetic data, better data curation |
| **Bias & Toxicity** | Learns biases from training data | RLHF, dataset filtering, debiasing |
| **Lack of Interpretability** | Black-box; hard to explain decisions | Mechanistic interpretability, attention analysis |
| **Context Window Limits** | Cannot process entire books/datasets (except Gemini) | RAG, sliding window, LongContext models |
| **Knowledge Cutoff** | Static knowledge from training date | RAG with real-time search |
| **Security Vulnerabilities** | Prompt injection, jailbreaking, extraction | Guardrails, input sanitization |
| **Environmental Impact** | High energy consumption for training/inference | Efficient architectures, green data centers |
| **Evaluation Difficulty** | Hard to evaluate open-ended generation quality | LLM-as-judge, human eval, diverse benchmarks |

---

## 8. KEY DIFFERENTIATORS — Model Comparison

| Dimension | BERT (Encoder) | GPT (Decoder) | T5 (Enc-Dec) |
|-----------|---------------|---------------|--------------|
| **Direction** | Bidirectional | Left-to-right | Bidirectional enc → AR dec |
| **Best at** | Understanding | Generation | Both (translation, sum.) |
| **Training** | Masked LM | Causal LM | Text-to-Text |
| **Inference** | Encoder once (fast) | Autoregressive (slower) | Enc-dec (medium) |
| **Fine-tuning** | Task-specific head | Prompting / full model | Unified T5 format |

| Dimension | Dense Models | MoE Models |
|-----------|-------------|------------|
| **Parameters** | All active per token | Subset active (e.g., 2/8 experts) |
| **Compute per token** | Proportional to total params | Proportional to active params |
| **Efficiency** | Less efficient | More efficient (same quality, less FLOPs) |
| **Examples** | LLaMA, Mistral (dense) | Mixtral, DeepSeek-V2, GPT-4 |

| Dimension | Small LMs (SLMs) | Large LMs (LLMs) |
|-----------|-----------------|------------------|
| **Size** | <10B parameters | >10B parameters |
| **Deployment** | Edge, mobile, single GPU | Datacenter, multi-GPU |
| **Latency** | Low (<100ms) | High (seconds) |
| **Capabilities** | Basic tasks, fine-tuned for specific | Complex reasoning, emergent abilities |
| **Cost** | Cheap | Expensive |

---

## 9. SCALING LAWS — Quick Reference

| Law | Key Insight | Equation |
|-----|-------------|----------|
| **Kaplan Scaling Law** | Model performance improves predictably with more params, data, and compute | L ∝ N^(-α) ∝ D^(-β) ∝ C^(-γ) |
| **Chinchilla Law** | For optimal training, params and tokens should scale equally — most models are undertrained | N_opt = 1.7 × 10^(-4) · C_total^(0.52) |
| **Emergent Abilities** | Certain capabilities (math, reasoning) only appear at model scale > ~70B | Threshold-dependent |
| **Inference Scaling** | More test-time compute improves reasoning quality (o1, o3) | Performance ∝ test-time compute |

> **Key Takeaway:** Most 2020-2022 models (GPT-3, LLaMA-1) were **undertrained** — they should have been trained on 4x more data given their parameter count. Chinchilla-optimal training changed everything.

---

## 10. FRAMEWORKS & TOOLS

| Framework | Purpose | Best For |
|-----------|---------|----------|
| **Hugging Face Transformers** | Load, train, use any Transformer model | **Go-to for everything** |
| **LangChain** | Build LLM applications (RAG, agents, chains) | Application development |
| **LlamaIndex** | Data framework for LLM apps (RAG focus) | Document Q&A, indexing |
| **vLLM** | High-throughput LLM inference | Production serving |
| **TGI (Text Generation Inference)** | HuggingFace's optimized inference server | Self-hosting |
| **Ollama** | Run local LLMs easily | Local experimentation |
| **llama.cpp** | Run quantized LLMs on CPU/laptop | Consumer hardware inference |
| **Axolotl** | Fine-tune LLMs easily | Fine-tuning |
| **Unsloth** | 2x faster fine-tuning with less memory | Efficient LoRA/QLoRA |
| **DeepSpeed** | Distributed training optimization | Training large models |
| **TRL** | Transformer Reinforcement Learning (RLHF/DPO) | Alignment training |
| **Weights & Biases** | Experiment tracking | ML experiment management |
| **MLflow** | Model lifecycle management | MLOps |
| **TensorRT-LLM** | NVIDIA's optimized LLM inference | GPU-optimized serving |

---

> **Pro Tip for Interview:** Understand the **Transformer** end-to-end — Self-Attention, Multi-Head Attention, Positional Encoding, LayerNorm, Residual connections. Then understand the **3 families**: Encoder-only (BERT) for understanding, Decoder-only (GPT) for generation, Encoder-Decoder (T5) for translation/summarization. Then know the **key innovations**: Scaling Laws, RLHF, LoRA/QLoRA, RAG, MoE, and Quantization. This covers 90% of GenAI interview questions.
