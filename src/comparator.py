import yaml
import os

def _normalize_kdes(yaml_data: dict) -> dict:
    normalized = {}
    if not isinstance(yaml_data, dict):
        return normalized
        
    for key, value in yaml_data.items():
        name = None
        reqs = []
        
        # Handle dict-based output
        if isinstance(value, dict):
            name = value.get('name', str(key))
            reqs = value.get('requirements', [])
            
        # Handle list-based output
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    # Look for name variations
                    for n_key in ['name', 'Name', 'NAME']:
                        if n_key in item:
                            name = item[n_key]
                            break
                    # Look for requirements variations
                    for r_key in ['requirements', 'Requirements', 'REQUIREMENTS']:
                        if r_key in item:
                            reqs = item[r_key]
                            break
                elif isinstance(item, str):
                    if item.lower().startswith('name:'):
                        name = item.split(':', 1)[1].strip()
                        
        if not name:
            name = str(key)
            
        if not isinstance(reqs, list):
            reqs = [reqs]
            
        # Clean requirements
        clean_reqs = []
        for r in reqs:
            if isinstance(r, dict):
                clean_reqs.extend([f"{k}: {v}" for k, v in r.items()])
            else:
                clean_reqs.append(str(r).strip())
                
        if name:
            normalized[name.strip().lower()] = {
                'original_name': name.strip(),
                'requirements': clean_reqs
            }
    return normalized

def load_yamls(yaml_path1: str, yaml_path2: str) -> tuple[dict, dict]:
    """
    Automatically takes two YAML files as input from Task-1, loads them,
    and returns a tuple of normalized dictionaries.
    """
    if not os.path.exists(yaml_path1):
        raise FileNotFoundError(f"YAML file not found: {yaml_path1}")
    if not os.path.exists(yaml_path2):
        raise FileNotFoundError(f"YAML file not found: {yaml_path2}")
        
    with open(yaml_path1, 'r') as f1, open(yaml_path2, 'r') as f2:
        data1 = yaml.safe_load(f1) or {}
        data2 = yaml.safe_load(f2) or {}
        
    norm1 = _normalize_kdes(data1)
    norm2 = _normalize_kdes(data2)
    return norm1, norm2

def compare_names(yaml_path1: str, yaml_path2: str, output_path: str):
    """
    Identifies differences in the two YAML files with respect to names of key data elements.
    Output is a TEXT file with differing names, or 'NO DIFFERENCES IN REGARDS TO ELEMENT NAMES'.
    """
    norm1, norm2 = load_yamls(yaml_path1, yaml_path2)
    
    names1 = set(norm1.keys())
    names2 = set(norm2.keys())
    
    diff_names_lower = names1.symmetric_difference(names2)
    
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as out:
        if not diff_names_lower:
            out.write("NO DIFFERENCES IN REGARDS TO ELEMENT NAMES\n")
        else:
            for n_lower in sorted(diff_names_lower):
                # Retrieve the original name from whichever dict has it
                orig_name = norm1[n_lower]['original_name'] if n_lower in norm1 else norm2[n_lower]['original_name']
                out.write(f"{orig_name}\n")

def compare_requirements(yaml_path1: str, yaml_path2: str, output_path: str):
    """
    Identifies differences in the two YAML files with respect to:
    (i) names of key data elements
    (ii) requirements for the key data elements
    Output is a TEXT file with tuples.
    """
    norm1, norm2 = load_yamls(yaml_path1, yaml_path2)
    
    file1_name = os.path.basename(yaml_path1)
    file2_name = os.path.basename(yaml_path2)
    
    differences = []
    
    all_names = set(norm1.keys()).union(set(norm2.keys()))
    
    for n_lower in sorted(all_names):
        in_1 = n_lower in norm1
        in_2 = n_lower in norm2
        
        # Absent in one of the files
        if in_1 and not in_2:
            orig_name = norm1[n_lower]['original_name']
            differences.append(f"{orig_name},ABSENT-IN-{file2_name},PRESENT-IN-{file1_name},NA")
        elif in_2 and not in_1:
            orig_name = norm2[n_lower]['original_name']
            differences.append(f"{orig_name},ABSENT-IN-{file1_name},PRESENT-IN-{file2_name},NA")
        else:
            # Present in both, check requirements
            orig_name = norm1[n_lower]['original_name']
            reqs1 = set(norm1[n_lower]['requirements'])
            reqs2 = set(norm2[n_lower]['requirements'])
            
            # Requirements in 1 but not 2
            for req in sorted(reqs1 - reqs2):
                differences.append(f"{orig_name},ABSENT-IN-{file2_name},PRESENT-IN-{file1_name},{req}")
            
            # Requirements in 2 but not 1
            for req in sorted(reqs2 - reqs1):
                differences.append(f"{orig_name},ABSENT-IN-{file1_name},PRESENT-IN-{file2_name},{req}")
                
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as out:
        if not differences:
            out.write("NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS\n")
        else:
            for diff in differences:
                out.write(f"{diff}\n")
