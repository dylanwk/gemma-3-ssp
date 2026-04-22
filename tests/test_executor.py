import pytest
import os
import pandas as pd
import zipfile
from src.executor import (
    take_two_text_files,
    determine_controls,
    execute_kubescape,
    generate_csv
)

@pytest.fixture
def dummy_files(tmp_path):
    f1 = os.path.join(tmp_path, "diff_names.txt")
    f2 = os.path.join(tmp_path, "diff_reqs.txt")
    with open(f1, 'w') as out1, open(f2, 'w') as out2:
        out1.write("NO DIFFERENCES IN REGARDS TO ELEMENT NAMES")
        out2.write("NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS")
        
    return f1, f2

def test_take_two_text_files(dummy_files):
    f1, f2 = dummy_files
    c1, c2 = take_two_text_files(f1, f2)
    assert "NO DIFFERENCES" in c1
    assert "NO DIFFERENCES" in c2

def test_determine_controls(dummy_files, tmp_path):
    f1, f2 = dummy_files
    out = os.path.join(tmp_path, "controls.txt")
    determine_controls(f1, f2, out)
    
    with open(out, 'r') as f:
        assert f.read().strip() == "NO DIFFERENCES FOUND"
        
def test_determine_controls_with_diff(tmp_path):
    f1 = os.path.join(tmp_path, "diff_names.txt")
    f2 = os.path.join(tmp_path, "diff_reqs.txt")
    with open(f1, 'w') as out1, open(f2, 'w') as out2:
        out1.write("Some KDE")
        out2.write("Some KDE,ABSENT-IN-1,PRESENT-IN-2,NA")
        
    out = os.path.join(tmp_path, "controls.txt")
    determine_controls(f1, f2, out)
    
    with open(out, 'r') as f:
        assert f.read().strip() == "C-0016,C-0017"

@pytest.fixture
def dummy_zip(tmp_path):
    z_path = os.path.join(tmp_path, "test.zip")
    with zipfile.ZipFile(z_path, 'w') as z:
        z.writestr("test.yaml", "apiVersion: v1\nkind: Pod\n")
    return z_path

def test_execute_kubescape_dummy(tmp_path, dummy_zip):
    # Testing with dummy JSON or empty to ensure DataFrame returns
    c_file = os.path.join(tmp_path, "controls.txt")
    with open(c_file, 'w') as f:
        f.write("NO DIFFERENCES FOUND")
        
    df = execute_kubescape(c_file, dummy_zip)
    assert isinstance(df, pd.DataFrame)
    assert "FilePath" in df.columns

def test_generate_csv(tmp_path):
    df = pd.DataFrame([{"FilePath": "test.zip", "Compliance score": 99}])
    out_csv = os.path.join(tmp_path, "out.csv")
    generate_csv(df, out_csv)
    
    assert os.path.exists(out_csv)
    df_loaded = pd.read_csv(out_csv)
    assert "Compliance score" in df_loaded.columns
    assert "Severity" in df_loaded.columns  # Was added automatically
