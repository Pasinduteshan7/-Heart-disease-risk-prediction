from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import joblib
import numpy as np
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "heart_risk_prediction_regression_model.sav")
ALLOWED_EXTENSIONS = {"sav"}

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"
os.makedirs(MODEL_DIR, exist_ok=True)

def model_exists():
    return os.path.isfile(MODEL_PATH)

def load_model():
    if not model_exists():
        return None
    # Compatibility shim: older pickled models sometimes reference
    # `sklearn.linear_model.base` which was moved to
    # `sklearn.linear_model._base` in newer scikit-learn versions.
    # If unpickling fails with ModuleNotFoundError, this mapping
    # helps joblib.find the correct module/class during load.
    try:
        import sys
        # try to import the new module and alias it to the old name
        import sklearn.linear_model._base as _base
        sys.modules.setdefault('sklearn.linear_model.base', _base)
    except Exception:
        # if anything goes wrong, ignore and attempt normal load
        pass

    model = joblib.load(MODEL_PATH)
    # Some models saved with different scikit-learn versions may miss
    # newer attributes on loaded estimator instances (for example
    # `LinearRegression.positive`). Try to patch common cases so the
    # loaded object is usable for predict(). This is a best-effort
    # approach that avoids forcing package reinstall immediately.
    def _patch_positive(obj, _seen=None):
        if _seen is None:
            _seen = set()
        try:
            oid = id(obj)
        except Exception:
            return
        if oid in _seen:
            return
        _seen.add(oid)

        # If it's a pipeline, iterate steps
        try:
            from sklearn.pipeline import Pipeline
        except Exception:
            Pipeline = None

        if Pipeline is not None and isinstance(obj, Pipeline):
            for name, step in obj.steps:
                _patch_positive(step, _seen)
            return

        # If object has a nested estimator in common attrs, patch them
        # Look for attributes that are estimators or lists/dicts of estimators
        for attr_name in dir(obj):
            # skip private attrs
            if attr_name.startswith("__"):
                continue
            try:
                val = getattr(obj, attr_name)
            except Exception:
                continue
            if val is None:
                continue
            # If this is a LinearRegression-like instance, ensure it has 'positive'
            try:
                clsname = val.__class__.__name__
            except Exception:
                clsname = None

            if clsname == 'LinearRegression':
                if not hasattr(val, 'positive'):
                    try:
                        setattr(val, 'positive', False)
                    except Exception:
                        pass
                # also recurse into its attributes
                _patch_positive(val, _seen)
                continue

            # Recurse into lists/tuples
            if isinstance(val, (list, tuple, set)):
                for item in val:
                    _patch_positive(item, _seen)
                continue

            # Recurse into dict values
            if isinstance(val, dict):
                for item in val.values():
                    _patch_positive(item, _seen)
                continue

            # If val looks like an estimator (has predict), recurse
            try:
                if hasattr(val, 'predict') or hasattr(val, 'transform'):
                    _patch_positive(val, _seen)
            except Exception:
                pass

    try:
        _patch_positive(model)
    except Exception:
        # never let the patching step break loading
        pass

    return model

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    has_model = model_exists()
    return render_template("patient_details.html", has_model=has_model)

@app.route("/upload-model", methods=["GET", "POST"])
def upload_model():
    if request.method == "POST":
        if "model_file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["model_file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(MODEL_DIR, "heart_risk_prediction_regression_model.sav")
            file.save(save_path)
            flash("Model uploaded successfully.")
            return redirect(url_for("index"))
        else:
            flash("Invalid file type. Please upload a .sav file.")
            return redirect(request.url)
    return render_template("upload_model.html")

@app.route("/getresults", methods=["POST"])
def getresults():
    if not model_exists():
        flash("Model file not found. Please upload the model or place it in the 'models/' folder.")
        return redirect(url_for("index"))
    form = request.form
    # required features (model trained on 7 features in this order)
    required = ["gender", "age", "tc", "hdl", "smoke", "bpm", "diab"]

    # Check presence of required fields in the POST data
    missing = [f for f in required if f not in form]
    if missing:
        # Return a clear message rather than a generic 400
        flash(f"Missing form fields: {', '.join(missing)}")
        return redirect(url_for("index"))

    # Parse inputs safely
    try:
        name = form.get("name", "").strip() or "Unknown"
        gender = float(form.get("gender"))
        age = float(form.get("age"))
        tc = float(form.get("tc"))
        hdl = float(form.get("hdl"))
        smoke = float(form.get("smoke"))
        bpm = float(form.get("bpm"))
        diab = float(form.get("diab"))
    except ValueError:
        flash("Please enter valid numeric values for the numeric fields.")
        return redirect(url_for("index"))

    # The model trained in Colab used 7 features (Sex, Age, TC, HDL, Smoke, BP medication, Diabetics).
    # Drop SBP here to match the training feature order used in Colab.
    test_data = np.array([gender, age, tc, hdl, smoke, bpm, diab]).reshape(1, -1)

    model = load_model()
    if model is None:
        flash("Could not load model. Make sure the .sav file is valid.")
        return redirect(url_for("index"))

    try:
        prediction = model.predict(test_data)
        if isinstance(prediction, np.ndarray):
            risk_val = float(prediction.ravel()[0])
        else:
            risk_val = float(prediction)
    except Exception as e:
        flash(f"Model prediction failed: {e}")
        return redirect(url_for("index"))

    if 0.0 <= risk_val <= 1.0:
        risk_pct = round(risk_val * 100, 2)
    else:
        risk_pct = round(risk_val, 2)

    resultDict = {"name": name, "risk": risk_pct}
    return render_template("patient_results.html", results=resultDict)

@app.route("/models/<path:filename>")
def serve_model(filename):
    return send_from_directory(MODEL_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
