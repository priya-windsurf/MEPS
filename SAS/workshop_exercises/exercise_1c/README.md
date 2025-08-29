# Exercise 1c: SAS to Python Conversion

This directory contains the conversion of Exercise1c.sas from SAS to Python.

## Files

- `Exercise1c.sas` - Original SAS code
- `Exercise1c_OUTPUT.TXT` - Expected SAS output
- `exercise_1c.py` - Python conversion using samplics library
- `validate_exercise_1c.py` - Validation script to compare outputs
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Setup

1. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Python conversion:
```bash
python exercise_1c.py
```

2. Validate the output against expected SAS results:
```bash
python validate_exercise_1c.py
```

## Conversion Details

The Python script converts the following SAS procedures to Python equivalents using the samplics library:

- `PROC SURVEYMEANS` → `samplics.TaylorEstimator` for survey means and totals
- `PROC SURVEYFREQ` → Custom frequency analysis with survey weights
- SAS formats → Python categorical variables and custom formatting
- Domain analysis → Subset analysis with survey design

### Key Features

- Handles complex survey design with strata, PSUs, and weights
- Calculates survey-adjusted means, totals, and percentages
- Computes weighted medians and quantiles
- Provides domain analysis by age groups
- Matches SAS output format for easy comparison

### Data Requirements

The script expects MEPS 2018 Full-year consolidated file (h209) with variables:
- `TOTEXP18` - Total health care expenses
- `AGELAST` - Person's age last time eligible
- `VARSTR` - Variance estimation stratum
- `VARPSU` - Variance estimation PSU
- `PERWT18F` - Final person weight
- `PANEL` - Panel number

If the actual MEPS data is not available, the script will create sample data for demonstration purposes.

## Validation

The validation script compares key statistics between Python and SAS outputs:

- Percentage of persons with expenses
- Mean expenses overall and by age group
- Median expenses by age group
- Survey design parameters (strata, clusters, sample sizes)

The validation uses a 5% relative tolerance for statistical comparisons to account for differences in survey estimation methods between SAS and Python.
