#!/usr/bin/env python3
"""
Validation Test: code-archaeologist PDF + XLSX skills
Tests ability to analyze legacy documentation and historical metrics
"""

import pdfplumber
import pandas as pd
import openpyxl
from pathlib import Path

print("🏺 code-archaeologist: Validating PDF + XLSX skills")
print("=" * 60)

# Test 1: PDF Legacy Documentation
print("\n📄 TEST 1: PDF Legacy Documentation Analysis")
try:
    with pdfplumber.open("test_skills_invoice.pdf") as pdf:
        text = pdf.pages[0].extract_text()
        tables = pdf.pages[0].extract_tables()

        print(f"✅ PDF opened successfully")
        print(f"✅ Text extracted: {len(text)} characters")
        print(f"✅ Tables found: {len(tables)}")

        # Simulate historical analysis
        if "invoice" in text.lower() or "date" in text.lower():
            print(f"✅ Historical context detected (invoice/date references)")

        pdf_success = True
except Exception as e:
    print(f"❌ PDF analysis failed: {e}")
    pdf_success = False

# Test 2: Excel Historical Metrics
print("\n📊 TEST 2: Excel Historical Metrics Analysis")
try:
    # Test with pandas (data analysis)
    df = pd.read_excel("test_skills_spreadsheet.xlsx")
    print(f"✅ Excel file loaded with pandas")
    print(f"✅ Rows: {len(df)}, Columns: {len(df.columns)}")
    print(f"✅ Column names: {list(df.columns)}")

    # Calculate basic statistics (simulating trend analysis)
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print(f"✅ Numeric columns found: {len(numeric_cols)}")
        for col in numeric_cols[:3]:  # First 3 numeric columns
            mean_val = df[col].mean()
            print(f"   - {col}: mean = {mean_val:.2f}")

    # Test with openpyxl (formula-intensive work)
    wb = openpyxl.load_workbook("test_skills_spreadsheet.xlsx")
    ws = wb.active
    print(f"✅ Excel file loaded with openpyxl")
    print(f"✅ Active sheet: {ws.title}")
    print(f"✅ Dimensions: {ws.dimensions}")

    # Check for formulas
    formula_count = 0
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                formula_count += 1

    print(f"✅ Formulas detected: {formula_count}")

    xlsx_success = True
except Exception as e:
    print(f"❌ Excel analysis failed: {e}")
    xlsx_success = False

# Final Results
print("\n" + "=" * 60)
print("📊 VALIDATION RESULTS:")
print(f"  PDF skill:  {'✅ PASS' if pdf_success else '❌ FAIL'}")
print(f"  XLSX skill: {'✅ PASS' if xlsx_success else '❌ FAIL'}")
print(f"\n  Overall:    {'✅ READY FOR PRODUCTION' if (pdf_success and xlsx_success) else '❌ NOT READY'}")
print("=" * 60)

exit(0 if (pdf_success and xlsx_success) else 1)
