# Limit Practice — Streamlit App

A student-friendly web app for practising limits of the form:

$$\lim_{x \to -1} \sqrt{\frac{x + 1}{x^2 + cx + b}}$$

## Live app

_Add your Streamlit Community Cloud URL here after deploying._

## GitHub repository

_Add your GitHub repository link here._

---

## Local setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a virtual environment

> **Already have a virtual environment?** Skip to Step 3.

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

> **Note:** You'll need to do this every time you open a new terminal.

```bash
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows
```

You'll know it's active when you see `(.venv)` at the start of your terminal prompt.

### 4. Install dependencies

> **Already installed dependencies before?** Skip to Step 5.

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`. If it doesn't, paste that URL into your browser manually.

To stop the app, press `Ctrl+C` in the terminal.

---

## How it works

Each problem randomly picks a positive integer `a` (2–7) and sets:

| Parameter | Value | Role |
|-----------|-------|------|
| `b` | `a² + 1` | constant term of denominator |
| `c` | `a² + 2` | linear coefficient of denominator |
| Answer | `1/a` | the limit value |

This guarantees:
- The rational expression inside the sqrt evaluates to **0/0** at x = -1 (indeterminate form).
- The denominator factors cleanly as `(x + 1)(x + b)`.
- After cancellation the limit simplifies to `1/a`, a rational number.

The app accepts answers as fractions (`1/3`), decimals (`0.333`), or integers, and provides a full 4-step solution walkthrough after submission.

---

## Deploying to Streamlit Community Cloud

No virtual environment is needed on Streamlit Community Cloud — it installs packages from `requirements.txt` automatically.

1. Push all files (except `.venv`) to a **public** GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch, and `app.py` as the main file.
4. Click **Deploy**.
