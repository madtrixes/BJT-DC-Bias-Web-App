import pytest
from bjt_circuit import calculate_dc_bias

def test_active_region_spec():
    # Vcc = 12.0 V, R1 = 100 kΩ (100000 Ω), R2 = 22 kΩ (22000 Ω)
    # RC = 2.2 kΩ (2200 Ω), RE = 1.0 kΩ (1000 Ω), Beta = 100, VBE = 0.70 V
    res = calculate_dc_bias(
        vcc=12.0,
        r1=100.0 * 1000,
        r2=22.0 * 1000,
        rc=2.2 * 1000,
        re=1.0 * 1000,
        beta=100.0,
        vbe=0.70
    )
    
    assert res["region"] == "Active"
    # Check Thevenin equivalent values
    assert pytest.approx(res["exact"]["V_TH"], rel=1e-2) == 2.164
    assert pytest.approx(res["exact"]["R_TH"], rel=1e-2) == 18032.79
    # Check IB is in expected range (around 12.3 uA - 15.1 uA depending on exact formulation)
    assert 10.0 <= res["exact"]["I_B_uA"] <= 18.0
    # Check Active region Vce > 0.2 V
    assert res["exact"]["V_CE"] > 0.2

def test_cutoff_region_spec():
    # Vcc = 5.0 V, R1 = 100 kΩ, R2 = 10 kΩ (Vth = 5 * 10 / 110 = 0.4545 V <= VBE 0.7 V)
    # RC = 1.0 kΩ, RE = 1.0 kΩ, Beta = 100, VBE = 0.70 V
    res = calculate_dc_bias(
        vcc=5.0,
        r1=100.0 * 1000,
        r2=10.0 * 1000,
        rc=1.0 * 1000,
        re=1.0 * 1000,
        beta=100.0,
        vbe=0.70
    )

    assert res["region"] == "Cutoff"
    assert res["exact"]["I_B_uA"] == 0.0
    assert res["exact"]["I_C_mA"] == 0.0
    assert res["exact"]["I_E_mA"] == 0.0

def test_saturation_region_spec():
    # High base drive and high collector resistance forcing saturation
    res = calculate_dc_bias(
        vcc=12.0,
        r1=10.0 * 1000,
        r2=50.0 * 1000,
        rc=15.0 * 1000,
        re=1.0 * 1000,
        beta=150.0,
        vbe=0.70
    )

    assert res["region"] == "Saturation"
    assert pytest.approx(res["exact"]["V_CE"], abs=1e-3) == 0.2
    assert any("SATURATION" in w or "Saturation" in w for w in res["warnings"])
