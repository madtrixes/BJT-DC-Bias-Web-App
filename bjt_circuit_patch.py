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
