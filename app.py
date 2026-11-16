from flask import Flask, render_template, request
from bjt_circuit import calculate_dc_bias, calculate_fixed_bias, calculate_emitter_bias, calculate_divider_bias_dict

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    # Default form values
    form_data = {
        "bias_mode": "divider",
        "vcc": "12.0",
        "r1": "33.0",
        "r2": "10.0",
        "rc": "2.2",
        "re": "1.0",
        "beta": "100",
        "vbe": "0.7"
    }

    if request.method == "POST":
        try:
            form_data["bias_mode"] = request.form.get("bias_mode", "divider")
            form_data["vcc"] = request.form.get("vcc", "12.0")
            form_data["r1"] = request.form.get("r1", "33.0")
            form_data["r2"] = request.form.get("r2", "10.0")
            form_data["rc"] = request.form.get("rc", "2.2")
            form_data["re"] = request.form.get("re", "1.0")
            form_data["beta"] = request.form.get("beta", "100")
            form_data["vbe"] = request.form.get("vbe", "0.7")

            bias_mode = form_data["bias_mode"]
            vcc = float(form_data["vcc"])
            r1 = float(form_data["r1"]) * 1000.0
            r2 = float(form_data["r2"]) * 1000.0
            rc = float(form_data["rc"]) * 1000.0
            re = float(form_data["re"]) * 1000.0
            beta = float(form_data["beta"])
            vbe = float(form_data["vbe"])

            if bias_mode == "fixed":
                # For fixed bias, r1 acts as Rb
                rb = r1
                res_dict = calculate_fixed_bias(vcc, rb, rc, beta, vbe)
                # Map to format compatible with divider result display or direct dict view
                result = {
                    "region": "Active",
                    "exact": {
                        "V_B": res_dict["vb_v"],
                        "V_E": res_dict["ve_v"],
                        "V_C": res_dict["vc_v"],
                        "V_CE": res_dict["vce_v"],
                        "I_B_uA": res_dict["ib_ua"],
                        "I_C_mA": res_dict["ic_ma"],
                        "I_E_mA": res_dict["ie_ma"]
                    },
                    "approx": {"V_B": res_dict["vb_v"], "V_E": res_dict["ve_v"], "I_C_mA": res_dict["ic_ma"], "V_CE": res_dict["vce_v"], "diff_ic_pct": 0.0, "diff_vce_pct": 0.0},
                    "approx_valid": True,
                    "warnings": []
                }
            elif bias_mode == "emitter":
                # For emitter bias, r1 acts as Rb
                rb = r1
                res_dict = calculate_emitter_bias(vcc, rb, rc, re, beta, vbe)
                result = {
                    "region": "Active",
                    "exact": {
                        "V_B": res_dict["vb_v"],
                        "V_E": res_dict["ve_v"],
                        "V_C": res_dict["vc_v"],
                        "V_CE": res_dict["vce_v"],
                        "I_B_uA": res_dict["ib_ua"],
                        "I_C_mA": res_dict["ic_ma"],
                        "I_E_mA": res_dict["ie_ma"]
                    },
                    "approx": {"V_B": res_dict["vb_v"], "V_E": res_dict["ve_v"], "I_C_mA": res_dict["ic_ma"], "V_CE": res_dict["vce_v"], "diff_ic_pct": 0.0, "diff_vce_pct": 0.0},
                    "approx_valid": True,
                    "warnings": []
                }
            else:
                # Default Voltage Divider Bias (Lab 2 exact full calculation function)
                result = calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe)

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Invalid input: {str(e)}"

    return render_template("index.html", result=result, error=error, form=form_data)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
