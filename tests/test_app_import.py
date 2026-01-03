# Simple smoke test for app.py logic
import importlib.util
import sys
import os

def test_import():
    app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    spec = importlib.util.spec_from_file_location("app", app_path)
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    assert hasattr(app, 'compute_fulfillment_metrics'), "Missing compute_fulfillment_metrics function"

if __name__ == "__main__":
    test_import()
    print("Smoke test passed.")
