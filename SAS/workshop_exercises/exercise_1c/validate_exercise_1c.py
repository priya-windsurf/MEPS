"""
Validation script to compare Python output with expected SAS output.

This script parses both the Python output and the SAS expected output
and compares key statistics to ensure the conversion is accurate.
"""

import re
import subprocess
import sys
from pathlib import Path

def run_python_script():
    """
    Run the Python conversion script and capture output.
    """
    try:
        result = subprocess.run(
            [sys.executable, 'exercise_1c.py'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode != 0:
            print(f"Error running Python script: {result.stderr}")
            return None
        
        return result.stdout
    except Exception as e:
        print(f"Failed to run Python script: {e}")
        return None

def parse_sas_output():
    """
    Parse the expected SAS output file.
    """
    sas_file = Path(__file__).parent / "Exercise1c_OUTPUT.TXT"
    
    try:
        with open(sas_file, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"SAS output file not found: {sas_file}")
        return None

def extract_key_statistics(text, source=""):
    """
    Extract key statistics from output text.
    """
    stats = {}
    
    freq_match = re.search(r'Any Expense\s+\d+\s+\d+\s+\d+\s+([\d.]+)\s+([\d.]+)', text)
    if freq_match:
        stats['pct_any_expense'] = float(freq_match.group(1))
        stats['pct_any_expense_se'] = float(freq_match.group(2))
    
    no_exp_match = re.search(r'No Expense\s+\d+\s+\d+\s+\d+\s+([\d.]+)\s+([\d.]+)', text)
    if no_exp_match:
        stats['pct_no_expense'] = float(no_exp_match.group(1))
        stats['pct_no_expense_se'] = float(no_exp_match.group(2))
    
    overall_mean_match = re.search(r'TOTEXP18\s+TOTAL HEALTH CARE\s+\d+\s+([\d.]+)\s+([\d.]+)', text)
    if overall_mean_match:
        stats['overall_mean'] = float(overall_mean_match.group(1))
        stats['overall_mean_se'] = float(overall_mean_match.group(2))
    
    overall_median_match = re.search(r'50 Median\s+([\d.]+)\s+([\d.]+)', text)
    if overall_median_match:
        stats['overall_median'] = float(overall_median_match.group(1))
        stats['overall_median_se'] = float(overall_median_match.group(2))
    
    domain_mean_match = re.search(r'Any Expense\s+TOTEXP18\s+TOTAL HEALTH CARE\s+\d+\s+([\d.]+)\s+([\d.]+)', text)
    if domain_mean_match:
        stats['domain_mean_any_expense'] = float(domain_mean_match.group(1))
        stats['domain_mean_any_expense_se'] = float(domain_mean_match.group(2))
    
    age_0_64_match = re.search(r'Any Expense\s+0-64\s+TOTEXP18\s+TOTAL HEALTH CARE\s+\d+\s+([\d.]+)\s+([\d.]+)', text)
    if age_0_64_match:
        stats['mean_age_0_64'] = float(age_0_64_match.group(1))
        stats['mean_age_0_64_se'] = float(age_0_64_match.group(2))
    
    age_65_plus_match = re.search(r'65\+\s+TOTEXP18\s+TOTAL HEALTH CARE\s+\d+\s+([\d.]+)\s+([\d.]+)', text)
    if age_65_plus_match:
        stats['mean_age_65_plus'] = float(age_65_plus_match.group(1))
        stats['mean_age_65_plus_se'] = float(age_65_plus_match.group(2))
    
    age_0_64_median_match = re.search(r'Any Expense\s+0-64\s+TOTEXP18\s+TOTAL HEALTH CARE\s+50 Median\s+([\d.]+)', text)
    if age_0_64_median_match:
        stats['median_age_0_64'] = float(age_0_64_median_match.group(1))
    
    age_65_plus_median_match = re.search(r'65\+\s+TOTEXP18\s+TOTAL HEALTH CARE\s+50 Median\s+([\d.]+)', text)
    if age_65_plus_median_match:
        stats['median_age_65_plus'] = float(age_65_plus_median_match.group(1))
    
    strata_match = re.search(r'Number of Strata\s+(\d+)', text)
    if strata_match:
        stats['n_strata'] = int(strata_match.group(1))
    
    clusters_match = re.search(r'Number of Clusters\s+(\d+)', text)
    if clusters_match:
        stats['n_clusters'] = int(clusters_match.group(1))
    
    obs_match = re.search(r'Number of Observations\s+(\d+)', text)
    if obs_match:
        stats['n_observations'] = int(obs_match.group(1))
    
    obs_used_match = re.search(r'Number of Observations Used\s+(\d+)', text)
    if obs_used_match:
        stats['n_observations_used'] = int(obs_used_match.group(1))
    
    sum_weights_match = re.search(r'Sum of Weights\s+([\d,]+)', text)
    if sum_weights_match:
        stats['sum_weights'] = float(sum_weights_match.group(1).replace(',', ''))
    
    if source:
        print(f"\nExtracted statistics from {source}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    return stats

def compare_statistics(python_stats, sas_stats, tolerance=0.05):
    """
    Compare statistics between Python and SAS outputs.
    
    Args:
        python_stats: Dictionary of statistics from Python output
        sas_stats: Dictionary of statistics from SAS output
        tolerance: Relative tolerance for comparison (default 5%)
    
    Returns:
        Dictionary with comparison results
    """
    results = {
        'passed': [],
        'failed': [],
        'missing': []
    }
    
    expected_sas_values = {
        'pct_any_expense': 86.6703,
        'pct_any_expense_se': 0.3605,
        'pct_no_expense': 13.3297,
        'pct_no_expense_se': 0.3605,
        'domain_mean_any_expense': 6995.631273,
        'domain_mean_any_expense_se': 138.898348,
        'mean_age_0_64': 5650.452557,
        'mean_age_0_64_se': 133.161971,
        'mean_age_65_plus': 12866.0,
        'mean_age_65_plus_se': 328.976784,
        'median_age_0_64': 1401.335930,
        'median_age_65_plus': 5877.252297,
        'n_strata': 117,
        'n_clusters': 257,
        'n_observations': 30461,
        'n_observations_used': 29415,
        'sum_weights': 326327888
    }
    
    reference_stats = sas_stats if sas_stats else expected_sas_values
    
    for key, expected_value in reference_stats.items():
        if key in python_stats:
            python_value = python_stats[key]
            
            if expected_value != 0:
                rel_diff = abs(python_value - expected_value) / abs(expected_value)
            else:
                rel_diff = abs(python_value - expected_value)
            
            if rel_diff <= tolerance:
                results['passed'].append({
                    'statistic': key,
                    'expected': expected_value,
                    'actual': python_value,
                    'rel_diff': rel_diff
                })
            else:
                results['failed'].append({
                    'statistic': key,
                    'expected': expected_value,
                    'actual': python_value,
                    'rel_diff': rel_diff
                })
        else:
            results['missing'].append(key)
    
    return results

def print_validation_results(results):
    """
    Print validation results in a formatted way.
    """
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)
    
    print(f"\nPASSED TESTS: {len(results['passed'])}")
    for test in results['passed']:
        print(f"  ✓ {test['statistic']}: Expected {test['expected']:.6f}, Got {test['actual']:.6f} (diff: {test['rel_diff']:.4f})")
    
    print(f"\nFAILED TESTS: {len(results['failed'])}")
    for test in results['failed']:
        print(f"  ✗ {test['statistic']}: Expected {test['expected']:.6f}, Got {test['actual']:.6f} (diff: {test['rel_diff']:.4f})")
    
    print(f"\nMISSING STATISTICS: {len(results['missing'])}")
    for stat in results['missing']:
        print(f"  ? {stat}: Not found in Python output")
    
    total_tests = len(results['passed']) + len(results['failed'])
    if total_tests > 0:
        pass_rate = len(results['passed']) / total_tests * 100
        print(f"\nOVERALL PASS RATE: {pass_rate:.1f}% ({len(results['passed'])}/{total_tests})")
    
    return len(results['failed']) == 0 and len(results['missing']) == 0

def main():
    """
    Main validation function.
    """
    print("Running Python conversion script...")
    python_output = run_python_script()
    
    if python_output is None:
        print("Failed to run Python script. Validation aborted.")
        return False
    
    print("Loading SAS expected output...")
    sas_output = parse_sas_output()
    
    print("Extracting statistics from outputs...")
    python_stats = extract_key_statistics(python_output, "Python output")
    sas_stats = extract_key_statistics(sas_output, "SAS output") if sas_output else {}
    
    print("Comparing statistics...")
    results = compare_statistics(python_stats, sas_stats)
    
    validation_passed = print_validation_results(results)
    
    if validation_passed:
        print("\n🎉 VALIDATION PASSED: Python output matches expected SAS output!")
        return True
    else:
        print("\n❌ VALIDATION FAILED: Python output does not match expected SAS output.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
