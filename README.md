# ENG29 2121 - BJT Common-Emitter DC Bias Web Application
A minimal, modular, and fully tested Flask web application for ENG29 2121 (Computer Programming for Electrical Engineers) that computes the DC Operating Point (Q-Point) of a BJT Common-Emitter circuit supporting 3 bias configurations (Voltage Divider, Fixed Bias, Emitter Bias).

## Repository & Submission Info
- **GitHub Repository URL**: [https://github.com/madtrixes/BJT-DC-Bias-Web-App](https://github.com/madtrixes/BJT-DC-Bias-Web-App)
- **Commit SHA**: `83853fb60eed512579956eeb0ef80f7ad89625f5`
- **Student ID**: B6428884 (Akkarawit Jaroenphan)

## Lab Requirements Met
- **Separate Modules**:
  - `bjt_circuit.py`: Core engineering calculations, 3 bias modes (Divider, Fixed, Emitter), region detection, input validation ($R_B > 0$), and approximate checks.
  - `app.py`: Flask web application routes handling multi-mode inputs and JSON/dict outputs.
  - `templates/index.html`: Responsive HTML5 user interface with dynamic input field toggles and SVG circuit diagrams.
  - `static/style.css`: Clean engineering CSS stylesheet.
  - `test_bjt_circuit.py / test_bjt_calc_extra.py`: Comprehensive Pytest unit and integration test suite.
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

## AI Assistance Disclosure
- AI Tools Used: Assisted in structuring modular Python functions, drafting Pytest cases, configuring Playwright MCP automated browser acceptance testing (opencode.json), and refining documentation formatting. All calculation logic and validation criteria were verified independently against electrical engineering theory.
