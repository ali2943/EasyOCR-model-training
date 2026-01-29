#!/usr/bin/env python3
"""
Test script to validate the FastAPI application structure
This script checks that all endpoints are properly defined and the app structure is correct.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_structure():
    """Test the FastAPI app structure without requiring heavy dependencies"""
    
    print("=" * 70)
    print("FastAPI Application Structure Test")
    print("=" * 70)
    
    # Check that app directory exists
    app_dir = Path(__file__).parent / "app"
    assert app_dir.exists(), "app directory not found"
    print("✓ app/ directory exists")
    
    # Check that main.py exists
    main_file = app_dir / "main.py"
    assert main_file.exists(), "app/main.py not found"
    print("✓ app/main.py exists")
    
    # Check static files
    static_dir = app_dir / "static"
    assert static_dir.exists(), "static directory not found"
    print("✓ app/static/ directory exists")
    
    html_file = static_dir / "index.html"
    assert html_file.exists(), "index.html not found"
    print("✓ app/static/index.html exists")
    
    css_file = static_dir / "style.css"
    assert css_file.exists(), "style.css not found"
    print("✓ app/static/style.css exists")
    
    js_file = static_dir / "script.js"
    assert js_file.exists(), "script.js not found"
    print("✓ app/static/script.js exists")
    
    # Check sample dataset
    dataset_dir = Path(__file__).parent / "data" / "sample_dataset"
    assert dataset_dir.exists(), "sample dataset directory not found"
    print("✓ data/sample_dataset/ directory exists")
    
    labels_file = dataset_dir / "labels.txt"
    assert labels_file.exists(), "labels.txt not found"
    print("✓ data/sample_dataset/labels.txt exists")
    
    # Verify labels format
    with open(labels_file, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0, "labels.txt is empty"
        for i, line in enumerate(lines):
            parts = line.strip().split('\t')
            assert len(parts) == 2, f"Line {i+1} doesn't have correct format (filename<TAB>text)"
            filename, text = parts
            assert filename.endswith(('.jpg', '.png', '.jpeg')), f"Invalid image extension: {filename}"
            assert len(text) > 0, f"Empty text for {filename}"
    
    print(f"✓ labels.txt has {len(lines)} valid entries")
    
    # Check that images exist
    image_count = 0
    for line in lines:
        filename = line.strip().split('\t')[0]
        image_path = dataset_dir / filename
        assert image_path.exists(), f"Image not found: {filename}"
        image_count += 1
    
    print(f"✓ All {image_count} images exist in dataset")
    
    # Verify main.py has the expected routes
    with open(main_file, 'r') as f:
        main_content = f.read()
        
        # Check for expected routes
        expected_routes = [
            '@app.get("/', # Just check for the start of the route
            '@app.get("/api/health")',
            '@app.get("/api/datasets")',
            '@app.post("/api/upload")',
            '@app.post("/api/train")',
            '@app.get("/api/status"',
            '@app.post("/api/reset")',
            '@app.get("/api/sample-dataset")'
        ]
        
        for route in expected_routes:
            assert route in main_content, f"Route not found: {route}"
            print(f"✓ Route defined: {route}")
    
    # Check HTML content
    with open(html_file, 'r') as f:
        html_content = f.read()
        assert '<title>EasyOCR Training Dashboard</title>' in html_content
        assert 'script.js' in html_content
        assert 'style.css' in html_content
        print("✓ HTML file is properly structured")
    
    # Check CSS content
    with open(css_file, 'r') as f:
        css_content = f.read()
        assert 'primary-color' in css_content
        assert '.btn' in css_content
        print("✓ CSS file contains styling definitions")
    
    # Check JavaScript content
    with open(js_file, 'r') as f:
        js_content = f.read()
        assert 'fetch' in js_content
        assert '/api/train' in js_content
        assert '/api/status' in js_content
        print("✓ JavaScript file contains API calls")
    
    print("\n" + "=" * 70)
    print("All Structure Tests Passed!")
    print("=" * 70)
    print("\nTo run the FastAPI app, first install dependencies:")
    print("  pip install -r requirements.txt")
    print("\nThen start the server:")
    print("  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\nAccess the UI at:")
    print("  http://localhost:8000")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    try:
        test_app_structure()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
