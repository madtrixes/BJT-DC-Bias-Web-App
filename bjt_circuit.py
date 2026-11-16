def calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe=0.7):
    """
    Calculates BJT Common-Emitter DC Operating Point (Q-point) using:
    - Exact method (Thevenin equivalent)
    - Region detection (Active, Cutoff, Saturation)
    - Approximate method comparison
    """
    if vcc <= 0:
        raise ValueError("Vcc must be positive")
    if r1 <= 0 or r2 <= 0 or rc < 0 or re < 0:
        raise ValueError("Resistances must be positive (Rc, Re >= 0)")
    if beta <= 0:
        raise ValueError("Beta must be positive")
    if not (0 < vbe < vcc):
        raise ValueError("Vbe must be between 0 and Vcc")

    # Thevenin Equivalent at Base
    r_th = (r1 * r2) / (r1 + r2)
    v_th = vcc * (r2 / (r1 + r2))

    # Check Cutoff: V_TH <= V_BE
    if v_th <= vbe:
        region = "Cutoff"
        i_b = 0.0
        i_c = 0.0
        i_e = 0.0
        v_b = v_th
        v_e = 0.0
        v_c = vcc
        v_ce = vcc
        exact = {
            "V_TH": v_th,
            "R_TH": r_th,
            "I_B_uA": 0.0,
            "I_C_mA": 0.0,
            "I_E_mA": 0.0,
            "V_B": v_b,
            "V_E": v_e,
            "V_C": v_c,
            "V_CE": v_ce
        }
        approx = {
            "I_C_mA": 0.0,
            "V_CE": vcc,
            "diff_ic_pct": 0.0,
            "diff_vce_pct": 0.0
        }
        return {
            "region": region,
            "exact": exact,
            "approx": approx,
            "approx_valid": (beta * re >= 10 * r2),
            "warnings": ["Transistor is in CUTOFF region (V_TH <= V_BE). Base current is zero."]
        }

    # Active region calculation
    i_b = (v_th - vbe) / (r_th + (beta + 1) * re)
    i_c = beta * i_b
    i_e = (beta + 1) * i_b
    v_e = i_e * re
    v_b = v_e + vbe
    v_c = vcc - i_c * rc
    v_ce = v_c - v_e

    warnings = []
    region = "Active"

    # Check Saturation: V_CE <= 0.2V
    if v_ce <= 0.2:
        region = "Saturation"
        v_ce = 0.2
        i_c_sat = (vcc - 0.2) / (rc + re) if (rc + re) > 0 else 0
        i_e_sat = i_c_sat * (beta + 1) / beta if beta > 0 else i_c_sat
        i_b_sat = i_c_sat / beta if beta > 0 else 0
        i_c = i_c_sat
        i_e = i_e_sat
        i_b = i_b_sat
        v_e = i_e * re
        v_c = v_e + 0.2
        warnings.append("Transistor is in SATURATION region (V_CE <= 0.2V). Collector-emitter voltage clamped to 0.2V.")

    # Approximate Engineering Method Comparison
    approx_valid = (beta * re >= 10 * r2)
    v_b_approx = v_th
    v_e_approx = v_b_approx - vbe
    i_e_approx = v_e_approx / re if re > 0 else 0
    i_c_approx = i_e_approx
    v_ce_approx = vcc - i_c_approx * (rc + re)

    if not approx_valid:
        warnings.append("Rule of thumb (beta*Re >= 10*R2) not met. Approximate method comparison may have larger error.")

    i_c_exact_mA = i_c * 1000
    i_c_approx_mA = i_c_approx * 1000
    diff_ic = abs(i_c_exact_mA - i_c_approx_mA) / ((i_c_exact_mA + i_c_approx_mA) / 2) * 100 if (i_c_exact_mA + i_c_approx_mA) > 0 else 0.0
    diff_vce = abs(v_ce - v_ce_approx) / ((v_ce + v_ce_approx) / 2) * 100 if (v_ce + v_ce_approx) > 0 else 0.0

    exact = {
        "V_TH": v_th,
        "R_TH": r_th,
        "I_B_uA": i_b * 1e6,
        "I_C_mA": i_c_exact_mA,
        "I_E_mA": i_e * 1000,
        "V_B": v_b,
        "V_E": v_e,
        "V_C": v_c,
        "V_CE": v_ce
    }

    approx = {
        "V_B": v_b_approx,
        "V_E": v_e_approx,
        "I_C_mA": i_c_approx_mA,
        "V_CE": v_ce_approx,
        "diff_ic_pct": diff_ic,
        "diff_vce_pct": diff_vce
    }

    return {
        "region": region,
        "exact": exact,
        "approx": approx,
        "approx_valid": approx_valid,
        "warnings": warnings
    }


def calculate_fixed_bias(vcc, rb, rc, beta, vbe=0.7):
    """
    Calculates BJT Fixed Bias DC Operating Point in Forward Active Region.
    Returns dictionary with keys: vb_v, ve_v, vc_v, vce_v, ib_ua, ic_ma, ie_ma.
    """
    if vcc <= 0:
        raise ValueError("Vcc must be positive")
    if rb <= 0 or rc < 0:
        raise ValueError("Resistances must be positive (Rb > 0, Rc >= 0)")
    if beta <= 0:
        raise ValueError("Beta must be positive")
    if not (0 < vbe < vcc):
        raise ValueError("Vbe must be between 0 and Vcc")

    i_b = (vcc - vbe) / rb
    if i_b <= 0:
        raise ValueError("Calculated base current (I_B) is <= 0. Forward Active model invalid.")

    i_c = beta * i_b
    i_e = (beta + 1) * i_b
    v_e = 0.0
    v_b = vbe
    v_c = vcc - i_c * rc
    v_ce = v_c - v_e

    if v_ce <= 0.2:
        raise ValueError("Calculated V_CE <= 0.2V. Transistor is in Saturation; Forward Active model invalid.")

    return {
        "vb_v": v_b,
        "ve_v": v_e,
        "vc_v": v_c,
        "vce_v": v_ce,
        "ib_ua": i_b * 1e6,
        "ic_ma": i_c * 1000,
        "ie_ma": i_e * 1000
    }


def calculate_emitter_bias(vcc, rb, rc, re, beta, vbe=0.7):
    """
    Calculates BJT Emitter Bias (single supply) DC Operating Point in Forward Active Region.
    Returns dictionary with keys: vb_v, ve_v, vc_v, vce_v, ib_ua, ic_ma, ie_ma.
    """
    if vcc <= 0:
        raise ValueError("Vcc must be positive")
    if rb <= 0 or rc < 0 or re < 0:
        raise ValueError("Resistances must be positive (Rb > 0, Rc >= 0, Re >= 0)")
    if beta <= 0:
        raise ValueError("Beta must be positive")
    if not (0 < vbe < vcc):
        raise ValueError("Vbe must be between 0 and Vcc")

    i_b = (vcc - vbe) / (rb + (beta + 1) * re)
    if i_b <= 0:
        raise ValueError("Calculated base current (I_B) is <= 0. Forward Active model invalid.")

    i_c = beta * i_b
    i_e = (beta + 1) * i_b
    v_e = i_e * re
    v_b = v_e + vbe
    v_c = vcc - i_c * rc
    v_ce = v_c - v_e

    if v_ce <= 0.2:
        raise ValueError("Calculated V_CE <= 0.2V. Transistor is in Saturation; Forward Active model invalid.")

    return {
        "vb_v": v_b,
        "ve_v": v_e,
        "vc_v": v_c,
        "vce_v": v_ce,
        "ib_ua": i_b * 1e6,
        "ic_ma": i_c * 1000,
        "ie_ma": i_e * 1000
    }


def calculate_divider_bias_dict(vcc, r1, r2, rc, re, beta, vbe=0.7):
    """
    Wrapper for Voltage Divider Bias returning standardized dictionary keys
    (vb_v, ve_v, vc_v, vce_v, ib_ua, ic_ma, ie_ma).
    """
    res = calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe)
    exact = res["exact"]
    v_ce = exact["V_CE"]
    if v_ce <= 0.2 and res["region"] == "Saturation":
        raise ValueError("Calculated V_CE <= 0.2V. Transistor is in Saturation; Forward Active model invalid.")
    if res["region"] == "Cutoff":
        raise ValueError("Transistor is in Cutoff region (V_TH <= V_BE). Forward Active model invalid.")
    
    return {
        "vb_v": exact["V_B"],
        "ve_v": exact["V_E"],
        "vc_v": exact["V_C"],
        "vce_v": v_ce,
        "ib_ua": exact["I_B_uA"],
        "ic_ma": exact["I_C_mA"],
        "ie_ma": exact["I_E_mA"]
    }
