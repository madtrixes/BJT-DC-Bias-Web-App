import pytest
from bjt_circuit import calculate_fixed_bias, calculate_emitter_bias, calculate_divider_bias_dict as calculate_divider_bias

def test_fixed_bias_valid():
    res = calculate_fixed_bias(vcc=12.0, rb=240.0, rc=2.2, beta=100, vbe=0.7)
    assert res["ic_ma"] > 0
    assert res["vce_v"] > 0.2
    assert "vb_v" in res
    assert "ve_v" in res
    assert "vc_v" in res
    assert "vce_v" in res
    assert "ib_ua" in res
    assert "ic_ma" in res
    assert "ie_ma" in res

def test_emitter_bias_valid():
    res = calculate_emitter_bias(vcc=20.0, rb=50.0, rc=0.1, re=0.1, beta=100, vbe=0.7)
    assert res["ic_ma"] > 0
    assert res["ve_v"] > 0
    assert "vce_v" in res

def test_divider_bias_dict_valid():
    res = calculate_divider_bias(vcc=12.0, r1=33.0, r2=10.0, rc=2.2, re=1.0, beta=100, vbe=0.7)
    assert res["ic_ma"] > 0
    assert res["ve_v"] > 0
    assert "vce_v" in res

def test_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_fixed_bias(vcc=-12.0, rb=240.0, rc=2.2, beta=100)
    with pytest.raises(ValueError):
        calculate_emitter_bias(vcc=12.0, rb=0.0, rc=2.2, re=1.0, beta=100)
    with pytest.raises(ValueError):
        calculate_divider_bias(vcc=12.0, r1=33.0, r2=10.0, rc=2.2, re=-1.0, beta=100)
