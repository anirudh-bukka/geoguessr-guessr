Great — now we’ll treat this like **onboarding a new machine as an AI engineer**. I’ll give you a **clean, no-confusion setup guide** so your GeoGuessr agent runs end-to-end.

Follow this **exactly in order**.

---

# 0. What You’re Setting Up

Your project uses:

* **Python 3.10–3.11 (NOT 3.12+)**
* **uv (fast package manager)**
* **PyTorch + **Transformers**
* **FAISS**
* **LangGraph**
* **Gemini + **Claude APIs**

---

# 1. Install Prerequisites

## 1.1 Install Python (IMPORTANT)

Check version:

```bash
python3 --version
```

You need:

```bash
Python 3.10 or 3.11
```

If wrong version:

Install via:

```bash
brew install python@3.11
```

---

## 1.2 Install uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

Restart terminal, then verify:

```bash
uv --version
```

---

# 2. Clone This Repo

```bash
git clone <your-repo-url>
cd geoguessr-guessr
```

---

# 3. Create Virtual Environment

```bash
uv venv
```

Activate:

```bash
source .venv/bin/activate
```

---

# 4. Install Dependencies (IMPORTANT FIX)

DO NOT install everything together (you might see conflicts).

Run **this exact sequence**:

```bash
uv add torch torchvision torchaudio
```

```bash
uv add transformers pillow tqdm
```

```bash
uv add faiss-cpu
```

```bash
uv add python-dotenv langgraph
```

```bash
uv add anthropic
```

```bash
uv add google-genai
```

---

# 5. Setup API Keys

Create `.env` file:

```bash
touch .env
```

Add:

```env
GEMINI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
HF_TOKEN=your_key_here
```

Optional model overrides:

```env
GEMINI_MODEL=gemini-2.5-flash
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
```

---

## Where to get keys:

### Gemini (Google)

* Go to Google AI Studio
* Generate API key

### Claude (Anthropic)

* Dashboard → API Keys

### HuggingFace

* [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

# 6. Setup Dataset

Create folder:

```bash
mkdir -p dataset/geoguessr
```

Download from Kaggle and extract into:

```bash
dataset/geoguessr/
   france/
   india/
   usa/
   ...
```

---

## Avoid disk issues

If low storage:

Use subset (recommended)

```bash
mkdir dataset_small
```

Then copy ~200 images per country.

Update `config.py`:

```python
DATASET_PATH = "dataset_small"
```

---

# 7. Test Dataset Loader

Run:

```bash
uv run python -c "from dataset.dataset_loader import load_dataset; print(len(load_dataset()))"
```

Expected:

```bash
50000  (or smaller if subset)
```

---

# 8. Build Vector Index (CLIP + FAISS)

Run:

```bash
uv run python embeddings/build_index.py
```

This will:

* Load images
* Generate embeddings using **CLIP**
* Store in **FAISS**

Time:

* Full dataset → 30–60 mins
* Small dataset → 5–10 mins

---

# 9. Test Full Pipeline

Update `main.py`:

```python
image = "<path to a new image in your file system>"
```

Then run:

```bash
uv run python main.py
```

Expected output:

```bash
Country prediction + reasoning
```

---

# 10. Run Evaluation

```bash
uv run python evaluation/benchmark.py
```

Expected:

```bash
Accuracy: 0.6 - 0.8 (initial)
```

---

# 11. Optional Cleanup

Free space:

```bash
rm -rf ~/.cache/huggingface
```

Remove large dataset if needed:

```bash
rm -rf dataset/geoguessr
```

---

# Common Errors

## Error: `module google.genai has no attribute configure`

Fix:

* I was using wrong SDK, if the same happens with you:
* Use `google-genai` + `genai.Client(...)`

---

## Error: `model not found gemini-1.5-flash`

Fix:

Use:

```python
model="gemini-2.5-flash"
```

---

## FAISS import error (Mac M1)

```bash
uv add faiss-cpu
```

---

## Torch slow / crash

Force CPU:

```python
device = "cpu"
```

---

# Final Checklist

Before running:

```bash
Python 3.11
uv installed
.venv activated
dependencies installed
.env configured
dataset placed correctly
index built
```

---

# What You’ve Built (Important for Interviews)

You now have:

* Image embeddings (CLIP)
* Vector search (FAISS)
* Multimodal reasoning (Gemini)
* LLM reasoning (Claude)
* Agent pipeline (LangGraph-style, but it's not LangGraph)
---