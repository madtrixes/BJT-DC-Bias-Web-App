import pytest
from bjt_circuit import calculate_dc_bias
from app import app

def test_kilo_ohm_inputs_scaling():
    # Input resistors in kOhm (e.g., R1=33, R2=10, Rc=2.2, Re=1)
    # When passed to app or calculation with multiplier, they should be correctly scaled to ohms.
    res = calculate_dc_bias(vcc=12.0, r1=33.0 * 1000, r2=10.0 * 1000, rc=2.2 * 1000, re=1.0 * 1000, beta=100.0, vbe=0.7)
    assert res["region"] == "Active"
    assert pytest.approx(res["exact"]["R_TH"], rel=1e-2) == 7674.4


def test_cutoff_region():
    res = calculate_dc_bias(vcc=12.0, r1=100000.0, r2=1000.0, rc=2200.0, re=1000.0, beta=100.0, vbe=0.7)
    assert res["region"] == "Cutoff"
    assert res["exact"]["I_B_uA"] == 0.0
    assert res["exact"]["I_C_mA"] == 0.0
    assert res["exact"]["V_CE"] == 12.0

def test_saturation_region():
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

def test_flask_get_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"BJT Common-Emitter DC Bias" in response.data

def test_flask_post_valid_calculation():
    client = app.test_client()
    data = {
        "vcc": "12", "r1": "33", "r2": "10",
        "rc": "2.2", "re": "1.0", "beta": "100", "vbe": "0.7"
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Active" in response.data
    assert b"DC Operating Point" in response.data

def test_flask_post_invalid_input_handles_gracefully():
    client = app.test_client()
    data = {
        "vcc": "12", "r1": "-5", "r2": "10",
        "rc": "2.2", "re": "1.0", "beta": "100", "vbe": "0.7"
    }
    response = client.post("/", data=data)
    assert response.status_code == 200
    assert b"Error" in response.data or b"Resistances must be positive" in response.data
