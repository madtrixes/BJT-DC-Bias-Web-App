# BJT Common-Emitter DC Bias Web App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimal, modular, fully-tested Flask web application for BJT Common-Emitter DC Bias calculation for ENG29 2121.

**Architecture:** Python engineering calculation module (`bjt_circuit.py`) handles DC operating point math, region warnings, validation, and approximate method comparison. Flask routes (`app.py`) process web requests, pass form data, and render templates (`templates/index.html` + `static/style.css`). Pytest test suite (`test_bjt_circuit.py`) verifies calculations and Flask HTTP endpoints.

**Tech Stack:** Python 3, Flask, Pytest, HTML5, CSS3.

**Spec:** `docs/superpowers/specs/2026-11-10-bjt-bias-web-app-design.md`

## Global Constraints

- Separate Python engineering logic, Flask routes, HTML template, CSS styling, and tests.
- Input fields: $V_{CC}, R_1, R_2, R_C, R_E, \beta, V_{BE}$.
- Output parameters: $V_B, V_E, V_C, I_B, I_C, I_E, V_{CE}$, operating region (Active, Saturation, Cutoff), unit formatting, validation warnings, and Exact vs Approximate percentage comparison.
- Dependencies: `flask`, `pytest`.

## Review Focus

- Zero/Negative input values ($R_1 \le 0, R_2 \le 0, R_E < 0, R_C < 0, \beta \le 0, V_{CC} \le 0$) $\rightarrow$ Raise `ValueError` with clear message.
- Cutoff region ($V_{TH} \le V_{BE}$) $\rightarrow$ $I_B=0, I_C=0, I_E=0, V_C=V_{CC}, V_{CE}=V_{CC}$, Region = Cutoff.
- Saturation region ($V_{CE} \le 0.2\text{V}$) $\rightarrow$ $V_{CE}=0.2\text{V}, I_{C,sat}=\frac{V_{CC}-0.2}{R_C+R_E}$, Region = Saturation warning.
- High/Low $\beta$ or invalid resistance ratio ($\beta R_E < 10 R_2$) $\rightarrow$ Mark approximate method rule-of-thumb flag as False with warning.
- Non-numeric or missing HTTP form POST inputs $\rightarrow$ Render form with error banner instead of 500 error.

---

### Task 1: Engineering Logic Module (`bjt_circuit.py`)

**Files:**
- Create: `bjt_circuit.py`
- Test: `test_bjt_circuit.py`

**Interfaces:**
- Produces: `calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe=0.7)` returning dictionary with exact results, approximate comparison, region, warnings, and formatted units.

- [ ] **Step 1: Write the failing unit tests for `bjt_circuit.py`**

```python
# test_bjt_circuit.py
import pytest
from bjt_circuit import calculate_dc_bias

def test_active_region_exact_and_approx():
    # Vcc=12V, R1=33k, R2=10k, Rc=2.2k, Re=1k, beta=100, Vbe=0.7V
    res = calculate_dc_bias(vcc=12.0, r1=33000, r2=10000, rc=2200, re=1000, beta=100, vbe=0.7)
    assert res["region"] == "Active"
    assert pytest.approx(res["exact"]["V_TH"], rel=1e-2) == 2.79
    assert res["exact"]["I_C_mA"] > 0
    assert res["exact"]["V_CE"] > 0.2
    assert "approx" in res
    assert res["approx_valid"] is True

def test_cutoff_region():
    # Vcc=12V, R1=100k, R2=1k (Vth = 12 * 1 / 101 = 0.118V < Vbe 0.7V)
    res = calculate_dc_bias(vcc=12.0, r1=100000, r2=1000, rc=2200, re=1000, beta=100, vbe=0.7)
    assert res["region"] == "Cutoff"
    assert res["exact"]["I_B_uA"] == 0.0
    assert res["exact"]["I_C_mA"] == 0.0
    assert res["exact"]["V_CE"] == 12.0

def test_saturation_region():
    # Large beta and R1/R2 pulling base high, causing small Vce
    res = calculate_dc_bias(vcc=12.0, r1=10000, r2=10000, rc=10000, re=1000, beta=200, vbe=0.7)
    assert res["region"] == "Saturation"
    assert res["exact"]["V_CE"] == 0.2

def test_invalid_input_validation():
    with pytest.raises(ValueError, match="Resistances must be positive"):
        calculate_dc_bias(vcc=12.0, r1=-1000, r2=10000, rc=2200, re=1000, beta=100)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test_bjt_circuit.py`
Expected: FAIL (Module `bjt_circuit` not found)

- [ ] **Step 3: Implement `calculate_dc_bias` in `bjt_circuit.py`**

Implement validation logic, Thevenin equivalent math, Cutoff/Active/Saturation region checks, approximate method comparison ($\beta R_E \ge 10 R_2$), and formatting dictionary.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test_bjt_circuit.py`
Expected: PASS

- [ ] **Step 5: Commit Task 1**

```bash
git add bjt_circuit.py test_bjt_circuit.py
git commit -m "feat: implement BJT DC bias engineering calculation logic and unit tests"
```

---

### Task 2: Flask Web Application Routes (`app.py`)

**Files:**
- Create: `app.py`
- Modify: `test_bjt_circuit.py`

**Interfaces:**
- Consumes: `calculate_dc_bias` from `bjt_circuit.py`
- Produces: Flask application instance `app` with `GET` and `POST` routes at `/`.

- [ ] **Step 1: Add failing web route tests to `test_bjt_circuit.py`**

```python
from app import app

def test_flask_get_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"BJT Common-Emitter DC Bias" in response.data

def test_flask_post_valid_calculation():
    client = app.test_client()
    data = {
        "vcc": "12", "r1": "33000", "r2": "10000",
        "rc": "2200", "re": "1000", "beta": "100", "vbe": "0.7"
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Active" in response.data
    assert b"DC Operating Point" in response.data

def test_flask_post_invalid_input_handles_gracefully():
    client = app.test_client()
    data = {
        "vcc": "12", "r1": "-500", "r2": "10000",
        "rc": "2200", "re": "1000", "beta": "100", "vbe": "0.7"
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Error" in response.data or b"Resistances must be positive" in response.data
```

- [ ] **Step 2: Run web tests to verify failure**

Run: `pytest test_bjt_circuit.py`
Expected: FAIL (Module `app` not found)

- [ ] **Step 3: Implement `app.py`**

Create Flask app route `@app.route("/", methods=["GET", "POST"])` that parses form parameters with unit scale factors (k$\Omega$ vs $\Omega$), calls `calculate_dc_bias()`, and renders `index.html`.

- [ ] **Step 4: Run web tests to verify pass**

Run: `pytest test_bjt_circuit.py`
Expected: PASS

- [ ] **Step 5: Commit Task 2**

```bash
git add app.py test_bjt_circuit.py
git commit -m "feat: implement Flask web application routes and integration tests"
```

---

### Task 3: HTML Template UI & CSS Styling (`templates/index.html` & `static/style.css`)

**Files:**
- Create: `templates/index.html`
- Create: `static/style.css`

**Interfaces:**
- Consumes: Form context and `result` dict passed from `app.py`
- Produces: User-friendly web form, Q-point summary card, engineering comparison table, region badges, and responsive CSS layout.

- [ ] **Step 1: Create HTML Template `templates/index.html`**

Write responsive HTML5 template with:
- Course Header: ENG29 2121 - Computer Programming for Electrical Engineers
- Title: BJT Common-Emitter DC Bias Calculator
- Inputs section with labeled number inputs and pre-filled default values.
- Results section featuring Operating Region Badge (Active/Cutoff/Saturation), Exact Q-point values ($V_{TH}, R_{TH}, I_B, I_C, I_E, V_B, V_E, V_C, V_{CE}$), and Comparative Engineering Table (Exact vs Approximate method with % difference).
- Error alert banner for invalid input.

- [ ] **Step 2: Create CSS Styling `static/style.css`**

Write CSS with clean engineering layout:
- Typography, CSS grid form layout, cards for inputs and outputs.
- Color-coded badges: Green for Active (`.badge-active`), Red/Orange for Saturation/Cutoff (`.badge-warning`).
- Comparison data table styling.

- [ ] **Step 3: Run full test suite to verify UI integration**

Run: `pytest test_bjt_circuit.py`
Expected: PASS

- [ ] **Step 4: Commit Task 3**

```bash
git add templates/index.html static/style.css
git commit -m "feat: add HTML template UI and CSS stylesheet for BJT bias web app"
```

---

### Task 4: Verification, Localhost Server Demonstration & Commit

**Files:**
- Modify: `README.md` (Add quickstart instructions and lab requirements outline)

- [ ] **Step 1: Install dependencies and run pytest**

Run: `pip install flask pytest`
Run: `pytest`
Expected: 100% test pass rate.

- [ ] **Step 2: Verify localhost server startup**

Run background command or python verification script to confirm `app.py` starts on `http://127.0.0.1:5000/`.

- [ ] **Step 3: Create README.md & final git commit**

```bash
git add README.md
git commit -m "docs: add lab project documentation and quickstart instructions"
```
