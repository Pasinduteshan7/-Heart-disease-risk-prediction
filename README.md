

```markdown
# Heart Risk Predictor (Flask)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![ML Library](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)

A lightweight Flask web application that loads a pre-trained `scikit-learn` model to predict a patient's heart disease risk using basic clinical inputs.

> **Repository Description:** Heart disease risk prediction web app (Flask) using a saved scikit-learn model.

---

## 🚀 Features

- **Interactive Web UI:** Simple, clean form to enter patient clinical details and view instant prediction results.
- **Dynamic Model Management:** Upload a `.sav` joblib model dynamically via the web UI or place it directly into the dedicated backend folder.
- **Pre-deployment Diagnostics:** Built-in validation script (`diag_load.py`) to test model compatibility and perform dummy predictions before spinning up the server.

---

## 📁 Repository Structure

```text
├── models/               # Directory for heart_risk_prediction_regression_model.sav
├── templates/            # HTML templates for the input form, upload interface, and results
├── app.py                # Main Flask application logic and routing
├── diag_load.py          # Diagnostic pipeline loader script
└── requirements.txt      # Python package dependencies

```

---

## 🛠️ Quick Start (Windows PowerShell)

Follow these steps to get your local development server running:

### 1. Set Up a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```

### 2. Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt

```

### 3. Validate Your Model (Optional but Recommended)

Run the diagnostic check to verify your saved model structure:

```powershell
python diag_load.py

```

### 4. Launch the Web Application

```powershell
python app.py

```

Once initialized, navigate to `http://127.0.0.1:5000` in your web browser.

---

## 🧠 Model Compatibility Notes

* **Expected Format:** The application expects a `joblib`-serialized `scikit-learn` estimator named `heart_risk_prediction_regression_model.sav` located in the `models/` directory (or uploaded via the `/upload-model` route).
* **Feature Schema:** The web interface parses and submits exactly **7 features** sequentially to the pipeline:
| Index | Feature Code | Description |
| --- | --- | --- |
| 1 | `gender` | Patient Gender |
| 2 | `age` | Patient Age |
| 3 | `tc` | Total Cholesterol |
| 4 | `hdl` | High-Density Lipoprotein |
| 5 | `smoke` | Smoking Status |
| 6 | `bpm` | Blood Pressure Medication Status |
| 7 | `diab` | Diabetes History Status |



> ⚠️ **Version Warning:** If your model was serialized with a different version of `scikit-learn` than the one installed in your environment, unpickling warnings or errors may occur. For exact matching, modify `requirements.txt` to pin your original training version (e.g., `scikit-learn==1.6.1`).

---

## 🔧 Customizing the Application

* **Preprocessing Pipelines:** If your specific architecture requires input scaling, categorical encoding, or altered feature ordering, modify the data matrix parsing within `app.py` directly before executing `model.predict()`.
* **Probability Outputs:** For classification models outputting confidence risk levels via probabilities, adjust the response mapping function `getresults()` in `app.py` to support `.predict_proba()`.

---

## 🔒 Security & Production Deployment

* **Secret Keys:** The application currently initializes with a fallback key `app.secret_key = "replace-with-a-secure-random-key"`. For production instances, parse a strong, cryptographically secure string from your system environment variables.
* **Production Server:** Do not use the native Flask development server (`python app.py`) in production. Instead, serve the WSGI application layer utilizing a robust production-grade wrapper such as **Waitress** (for Windows environments) or **Gunicorn** (for Linux environments).
* **Access Controls:** Secure the storage access configurations on your host server to avoid exposing uploaded binary model files publicly.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this toolkit, feel free to open an issue or submit a Pull Request. High-priority areas for development include:

* Integrating rigorous unit testing suites covering endpoint input validation and inference handling.
* Developing a production-ready multi-stage `Dockerfile` for containerized orchestration.
* Hardening the file upload handling layers with explicit MIME-type checks and payload limits.

```

```
