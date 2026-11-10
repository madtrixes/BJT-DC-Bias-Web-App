# ENG29 2121 - BJT Common-Emitter DC Bias Web Application

A minimal, modular, and fully tested Flask web application for **ENG29 2121 (Computer Programming for Electrical Engineers)** that computes the DC Operating Point (Q-Point) of a BJT Common-Emitter Voltage Divider Bias circuit.

## Lab Requirements Met
- **Separate Modules**:
  - `bjt_circuit.py`: Core engineering calculations, Thevenin equivalent analysis, region detection (Active, Cutoff, Saturation), validation, and approximate method comparison.
  - `app.py`: Flask web application routes.
  - `templates/index.html`: Responsive HTML5 user interface.
  - `static/style.css`: Clean engineering CSS stylesheet.
  - `test_bjt_circuit.py`: Comprehensive Pytest unit and integration test suite.
- **Inputs**: $V_{CC}, R_1, R_2, R_C, R_E, \beta, V_{BE}$
- **Outputs**: DC operating point ($V_B, V_E, V_C, I_B, I_C, I_E, V_{CE}$) with appropriate engineering units, operating region warnings, and independent approximate engineering calculation comparison.

---

## Quickstart & Localhost Demonstration

1. **Install Dependencies**:
   ```bash
   pip install flask pytest
   ```

2. **Run Tests**:
   ```bash
   python -m pytest
   ```

3. **Run Localhost Server**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.
