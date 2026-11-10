from flask import Flask, render_template, request
from bjt_circuit import calculate_dc_bias

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    # Default form values in kOhm
    form_data = {
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
            form_data["vcc"] = request.form.get("vcc", "12.0")
            form_data["r1"] = request.form.get("r1", "33.0")
            form_data["r2"] = request.form.get("r2", "10.0")
            form_data["rc"] = request.form.get("rc", "2.2")
            form_data["re"] = request.form.get("re", "1.0")
            form_data["beta"] = request.form.get("beta", "100")
            form_data["vbe"] = request.form.get("vbe", "0.7")

            vcc = float(form_data["vcc"])
            # Multiply kilo-ohm inputs by 1000 to convert to ohms
            r1 = float(form_data["r1"]) * 1000.0
            r2 = float(form_data["r2"]) * 1000.0
            rc = float(form_data["rc"]) * 1000.0
            re = float(form_data["re"]) * 1000.0
            beta = float(form_data["beta"])
            vbe = float(form_data["vbe"])

            result = calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe)
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Invalid input: {str(e)}"

    return render_template("index.html", result=result, error=error, form=form_data)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
