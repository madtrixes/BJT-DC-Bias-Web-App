import pytest
from bjt_circuit import calculate_dc_bias

def test_active_region_exact_and_approx():
    # Vcc=12V, R1=33k, R2=10k, Rc=2.2k, Re=1k, beta=100, Vbe=0.7V
    res = calculate_dc_bias(vcc=12.0, r1=33000.0, r2=10000.0, rc=2200.0, re=1000.0, beta=100.0, vbe=0.7)
    assert res["region"] == "Active"
    assert pytest.approx(res["exact"]["V_TH"], rel=1e-2) == 2.7906
    assert pytest.approx(res["exact"]["R_TH"], rel=1e-2) == 7674.4
    assert res["exact"]["I_C_mA"] > 0
    assert res["exact"]["V_CE"] > 0.2
    assert "approx" in res
    assert res["approx_valid"] is True

def test_cutoff_region():
    # Vcc=12V, R1=100k, R2=1k (Vth = 12 * 1 / 101 = 0.1188V < Vbe 0.7V)
    res = calculate_dc_bias(vcc=12.0, r1=100000.0, r2=1000.0, rc=2200.0, re=1000.0, beta=100.0, vbe=0.7)
    assert res["region"] == "Cutoff"
    assert res["exact"]["I_B_uA"] == 0.0
    assert res["exact"]["I_C_mA"] == 0.0
    assert res["exact"]["V_CE"] == 12.0

def test_saturation_region():
    # Large R2 pulling base high, large Rc causing low Vce
    res = calculate_dc_bias(vcc=12.0, r1=10000.0, r2=10000.0, rc=10000.0, re=1000.0, beta=200.0, vbe=0.7)
    assert res["region"] == "Saturation"
    assert pytest.approx(res["exact"]["V_CE"], abs=1e-3) == 0.2

def test_invalid_input_validation():
    with pytest.raises(ValueError, match="Resistances must be positive"):
        calculate_dc_bias(vcc=12.0, r1=-1000.0, r2=10000.0, rc=2200.0, re=1000.0, beta=100.0)

    with pytest.raises(ValueError, match="Vcc must be positive"):
        calculate_dc_bias(vcc=-12.0, r1=10000.0, r2=10000.0, rc=2200.0, re=1000.0, beta=100.0)

    with pytest.raises(ValueError, match="Beta must be positive"):
        calculate_dc_bias(vcc=12.0, r1=10000.0, r2=10000.0, rc=2200.0, re=1000.0, beta=0.0)
