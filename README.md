# Heart Risk Predictor (Flask)

A small Flask web application that loads a pre-trained scikit-learn model to predict a patient's heart disease risk from basic clinical inputs.

Short description (for GitHub repo description):
Heart disease risk prediction web app (Flask) using a saved scikit-learn model.

**Features**
- Simple web UI to enter patient details and get a prediction
- Upload a `.sav` joblib model via the web UI or place it in the `models/` folder
- Diagnostic loader to validate model compatibility (`diag_load.py`)

**Repository structure**
- `app.py` - main Flask application
- `diag_load.py` - diagnostic script to load the saved model and attempt a dummy prediction
- `models/` - put `heart_risk_prediction_regression_model.sav` here (or upload via UI)
- `templates/` - HTML templates for the form, upload, and results
- `requirements.txt` - Python dependencies

---

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

2. Install dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. (Optional) Run the diagnostic loader to check your model
```powershell
python diag_load.py
```

4. Run the Flask app (development server)
```powershell
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Model compatibility notes

- The app expects a joblib-saved scikit-learn estimator named `heart_risk_prediction_regression_model.sav` in the `models/` directory (or upload it via `/upload-model`).
- The web form sends 7 features to the model in this order: `gender`, `age`, `tc`, `hdl`, `smoke`, `bpm`, `diab`.
- If your model was saved with a different scikit-learn version, you may see warnings when unpickling. If you encounter errors or inconsistent results, consider re-saving the model using the scikit-learn version in your environment or pin the dependency in `requirements.txt` (for example `scikit-learn==1.6.1`).

---

## Security & deployment notes

- `app.py` currently uses `app.secret_key = "replace-with-a-secure-random-key"`. For production, set a strong secret key from an environment variable and run behind a WSGI server (Waitress/gunicorn) rather than the Flask development server.
- Do not expose uploaded model files publicly without proper access controls.

---

## Customizing the app

- If your model expects different feature ordering or preprocessing, apply the same preprocessing to inputs in `app.py` before calling `model.predict()`.
- To support models that output probabilities, adjust post-processing in `getresults()` in `app.py`.

---

## Contributing

- Feel free to open issues or PRs. Suggested improvements:
   - Add unit tests for input validation and model prediction
   - Add Dockerfile for containerized deployment
   - Harden upload handling and add file scanning / size limits

---

## License

- Add a license file (e.g., `MIT`) before publishing if you want to allow reuse.

---

If you'd like, I can also:
- Pin `scikit-learn` in `requirements.txt` to match the model's original version
- Update `app.py` to read `SECRET_KEY` from an environment variable and add a `.env.example`
- Create a `LICENSE` file and `.gitignore` optimized for Python projects

Tell me which of the above you'd like me to do next and I'll apply the changes.
