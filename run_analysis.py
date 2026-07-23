#!/usr/bin/env python3
"""
Master Execution Script: IISER Mohali Merchandise Preference Survey 2026 Analysis.

Runs the complete data processing, demographic profiling, apparel specification matrix,
purchasing decision driver analysis, and qualitative theme extraction pipeline.
"""

import os
import sys

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_preprocessing import preprocess_dataset
from src.demographic_analysis import analyze_demographics
from src.merch_preference_analysis import analyze_merchandise_preferences
from src.apparel_analysis import analyze_apparel
from src.consumer_psychology_analysis import analyze_consumer_psychology


def main():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'iiserm_merch_survey_data.csv')
    if not os.path.exists(data_path):
        print(f"Error: Dataset file not found at {data_path}")
        sys.exit(1)
        
    print("=" * 80)
    print("IISER MOHALI MERCHANDISE PREFERENCE SURVEY 2026 - STATISTICAL REPORT")
    print("=" * 80)
    
    # 1. Preprocessing
    data = preprocess_dataset(data_path)
    df_raw = data['df_raw']
    apparel_ratings = data['apparel_ratings']
    decision_factors = data['decision_factors']
    
    # 2. Demographic Analysis
    demo_res = analyze_demographics(df_raw)
    print(f"\n[1] DEMOGRAPHICS & TARGET AUDIENCE PROFILE (N = {demo_res['total_respondents']})")
    print("-" * 60)
    print("\nAcademic Program / Batch Distribution:")
    print(demo_res['affiliation_df'].to_string())
    print("\nFields of Study / Academic Disciplines:")
    print(demo_res['fields_df'].to_string())
    print("\nAnnual Merchandise Purchases Statistics:")
    for k, v in demo_res['purchase_stats'].items():
        print(f"  - {k.capitalize()}: {v}")
        
    # 3. Merchandise Preferences
    merch_res = analyze_merchandise_preferences(df_raw)
    print("\n\n[2] MERCHANDISE CATEGORY DEMAND & PRIORITIES")
    print("-" * 60)
    print("\nCategory Purchase Interest Ranking:")
    print(merch_res['categories_df'].to_string())
    print("\nSingle Must-Have Item Priority (Next Semester):")
    print(merch_res['single_items_df'].to_string())
    print("\nUnreleased & Desired Merch Gap Items (Sample):")
    for item in merch_res['unreleased_items'][:10]:
        print(f"  • {item}")
        
    # 4. Apparel Specifications & Design Matrix
    apparel_res = analyze_apparel(df_raw, apparel_ratings)
    print("\n\n[3] APPAREL SPECIFICATIONS, FIT & DESIGN MATRIX")
    print("-" * 60)
    print("\nPreferred Fabric / Material:")
    print(apparel_res['materials_df'].to_string())
    print("\nSize Distribution:")
    print(apparel_res['sizes_df'].to_string())
    print("\nApparel Design Placement Matrix (1=Not Preferred, 2=Preferred, 3=Highly Preferred):")
    print(apparel_res['apparel_matrix_df'].to_string(index=False))
    print("\nSweatshirt / Hoodie Willingness to Pay (WTP):")
    print(apparel_res['wtp_df'].to_string())
    print("\nFit & Cut Requests (Sample):")
    for req in apparel_res['fit_requests'][:8]:
        print(f"  • {req}")
        
    # 5. Consumer Psychology & Decision Drivers
    psych_res = analyze_consumer_psychology(df_raw, decision_factors)
    print("\n\n[4] CONSUMER PSYCHOLOGY & PURCHASING DECISION DRIVERS")
    print("-" * 60)
    print("\nPurchase Decision Drivers (1=Not at all to 5=Absolutely/Of course):")
    print(psych_res['decision_matrix_df'].to_string(index=False))
    print("\nBrand Loyalty / Blind Purchasing Habit:")
    print(psych_res['blind_loyalty_df'].to_string())
    print("\nDesign Theme Ranking:")
    print(psych_res['themes_df'].to_string())
    
    print("\n" * 2)
    print("=" * 80)
    print("END OF STATISTICAL REPORT")
    print("=" * 80)


if __name__ == '__main__':
    main()
