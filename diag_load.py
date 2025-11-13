"""Diagnostic loader for the heart risk model.

Run this to validate the `.sav` model file and attempt a dummy prediction.
"""
import joblib
import traceback
import numpy as np

MODEL_PATH = r"models/heart_risk_prediction_regression_model.sav"

def main():
    print("MODEL PATH:", MODEL_PATH)
    try:
        m = joblib.load(MODEL_PATH)
        print("Loaded model type:", type(m))
        try:
            from sklearn.pipeline import Pipeline
            if isinstance(m, Pipeline):
                print("Pipeline steps:")
                for name, step in m.steps:
                    print(" -", name, "->", type(step))
        except Exception:
            pass

        try:
            print("Model repr:", repr(m)[:1000])
        except Exception:
            print("Could not generate repr() for model (missing attributes?).")

        try:
            attrs = [a for a in dir(m) if 'posit' in a.lower() or 'coef' in a.lower() or 'intercept' in a.lower()]
            print("Selected attributes:", attrs)
        except Exception:
            print("Could not inspect model attributes safely.")

        try:
            print("Full dir() sample (first 60):", sorted(dir(m))[:60])
        except Exception:
            print("Could not list dir() of model safely.")

        # The web app expects 7 features: gender, age, tc, hdl, smoke, bpm, diab
        X = np.zeros((1, 7))
        print("Attempting predict with shape", X.shape)
        try:
            y = m.predict(X)
            print("Predict output:", y)
        except Exception:
            print("Exception during predict():")
            traceback.print_exc()
    except Exception:
        print("Exception during load():")
        traceback.print_exc()

if __name__ == '__main__':
    main()