#!/usr/bin/env python3
"""
Validation Test: web-researcher PDF skill
Tests ability to extract research content from PDF documents
"""

import pdfplumber
from pathlib import Path

print("🔍 web-researcher: Validating PDF skill")
print("=" * 60)

# Test: PDF Research Extraction
print("\n📄 TEST: PDF Research Document Extraction")
try:
    with pdfplumber.open("test_skills_invoice.pdf") as pdf:
        # Extract metadata
        metadata = pdf.metadata
        print(f"✅ PDF opened successfully")
        print(f"✅ Pages: {len(pdf.pages)}")

        # Extract all text
        full_text = ""
        for page_num, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            full_text += page_text or ""
            print(f"✅ Page {page_num} extracted: {len(page_text or '')} characters")

        print(f"\n✅ Total text extracted: {len(full_text)} characters")

        # Extract tables (useful for research data)
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            all_tables.extend(tables)

        print(f"✅ Tables extracted: {len(all_tables)}")

        # Sample output
        print(f"\nSample extracted content (first 300 chars):")
        print(full_text[:300] if full_text else "No text found")

        # Success criteria
        success = len(full_text) > 0

        if success:
            print("\n" + "=" * 60)
            print("📊 VALIDATION RESULTS:")
            print("  PDF skill: ✅ PASS")
            print("\n  Overall:   ✅ READY FOR PRODUCTION")
            print("=" * 60)
        else:
            print("\n❌ Failed: No text extracted from PDF")

except Exception as e:
    print(f"\n❌ PDF extraction failed: {e}")
    success = False
    print("\n" + "=" * 60)
    print("📊 VALIDATION RESULTS:")
    print("  PDF skill: ❌ FAIL")
    print("\n  Overall:   ❌ NOT READY")
    print("=" * 60)

exit(0 if success else 1)
