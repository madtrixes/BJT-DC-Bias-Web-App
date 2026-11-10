# Design Document: BJT Common-Emitter DC Bias Web App

## 1. Intent & Purpose
Build the smallest working, clean, and tested Flask web application for ENG29 2121 (Computer Programming for Electrical Engineers) that computes the DC Operating Point (Q-Point) of a BJT Common-Emitter voltage-divider bias circuit.

## 2. Scope & Boundaries
- **Goals**:
  - Accept DC input parameters: $V_{CC}, R_1, R_2, R_C, R_E, \beta, V_{BE}$.
  - Calculate exact DC Q-Point parameters ($V_B, V_E, V_C, I_B, I_C, I_E, V_{CE}$).
  - Determine operating region (Active, Saturation, Cutoff) and generate validation warnings.
  - Compare results with an independent engineering approximate calculation ($\beta R_E \ge 10 R_2$).
  - Clean modular code structure: engineering logic, Flask web routes, HTML template, CSS, and automated unit tests.
- **Non-Goals**: No AC analysis, transient analysis, graphical circuit editor, or FET support.

## 3. Approaches Considered & Selected Approach
- **Approach A (Single-file Flask app)**: Combining logic, HTML inline strings, and routing in one file. *Rejected* due to lab requirements for separate python logic, templates, CSS, and tests.
- **Approach B (Modular Flask Web App - Selected)**:
  - `bjt_circuit.py`: Core electrical engineering formulas, validation, exact (Thevenin) and approximate solver, region determination.
  - `app.py`: Flask web application, route handling, input parsing.
  - `templates/index.html`: Web interface form and results table with formatted engineering units.
  - `static/style.css`: Clean, readable UI layout styling.
  - `test_bjt_circuit.py`: Pytest suite verifying engineering logic, region edge cases, and Flask routes.

## 4. Detailed Specification & Formulas

### 4.1 Input Parameters & Validation
- $V_{CC}$ (V): Collector Supply Voltage ($>0$)
- $R_1, R_2$ (k$\Omega$ or $\Omega$): Voltage Divider Resistors ($>0$)
- $R_C$ (k$\Omega$ or $\Omega$): Collector Resistor ($\ge 0$)
- $R_E$ (k$\Omega$ or $\Omega$): Emitter Resistor ($\ge 0$)
- $\beta$: DC Current Gain ($>0$)
- $V_{BE}$ (V): Base-Emitter On Voltage ($0 < V_{BE} < V_{CC}$, default $0.7\text{V}$)

### 4.2 Engineering Formulas (Exact / Thevenin)
1. **Thevenin Voltage & Resistance**:
   $$V_{TH} = V_{CC} \cdot \frac{R_2}{R_1 + R_2}$$
   $$R_{TH} = \frac{R_1 \cdot R_2}{R_1 + R_2}$$

2. **Operating Region & Q-Point**:
   - **Cutoff Check**: If $V_{TH} \le V_{BE}$:
     - Region: **Cutoff**
     - $I_B = 0, I_C = 0, I_E = 0$
     - $V_B = V_{TH}, V_E = 0\text{V}, V_C = V_{CC}, V_{CE} = V_{CC}$
   - **Active Calculation**:
     - $I_B = \frac{V_{TH} - V_{BE}}{R_{TH} + (\beta + 1)R_E}$
     - $I_C = \beta \cdot I_B$, $I_E = (\beta + 1) \cdot I_B$
     - $V_E = I_E \cdot R_E$, $V_B = V_E + V_{BE}$, $V_C = V_{CC} - I_C \cdot R_C$, $V_{CE} = V_C - V_E$
   - **Saturation Check**: If $V_{CE} \le 0.2\text{V}$ (where $V_{CE,sat} = 0.2\text{V}$):
     - Region: **Saturation**
     - $I_{C,sat} = \frac{V_{CC} - 0.2}{R_C + R_E}$
     - $V_{CE} = 0.2\text{V}$, $V_E = I_{C,sat} \cdot R_E$, $V_C = V_E + 0.2\text{V}$

### 4.3 Independent Engineering Calculation (Approximate Method)
- Check condition: $\beta \cdot R_E \ge 10 \cdot R_2$
- Approximate formulas:
  - $V_{B,approx} \approx V_{TH}$
  - $V_{E,approx} = V_{B,approx} - V_{BE}$
  - $I_{E,approx} = \frac{V_{E,approx}}{R_E}$
  - $I_{C,approx} \approx I_{E,approx}$
  - $V_{CE,approx} = V_{CC} - I_{C,approx}(R_C + R_E)$
- Output percentage difference vs. Exact method for $I_C$ and $V_{CE}$.

## 5. Next Steps
Invoke `writing-plans` skill to generate the implementation plan.
