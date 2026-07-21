"""
Apparel Specifications, Fit, Placement & Pricing Analysis Module.

Analyzes fabric preferences, apparel fits (oversized, baggy, boxy), size distribution,
design element placement matrix (Likert ratings), and Willingness to Pay (WTP) ranges.
"""

import pandas as pd
from typing import Dict, Any
from src.data_preprocessing import parse_multiselect, encode_apparel_ratings


def analyze_apparel(df_raw: pd.DataFrame, apparel_ratings: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes statistical summaries for apparel materials, sizes, design placement, and WTP.
    """
    material_col = 'Which material/fabric do you prefer for apparel items (T-shirts/Hoodies)?'
    size_col = 'What specific size range are you most likely to purchase for apparel (T-shirts/Hoodies)?'
    wtp_col = 'What is the price you would be willing to pay for a "good" Sweatshirt?'
    non_conv_apparel_col = 'What apparel/clothing do you look for other than conventional T-shirts, hoodies, and sweatshirts as merch?'
    
    total_respondents = len(df_raw)
    
    # 1. Fabric / Material Preferences
    exploded_materials = parse_multiselect(df_raw[material_col])
    mat_counts = exploded_materials.value_counts()
    mat_pct = (mat_counts / total_respondents * 100).round(2)
    materials_df = pd.DataFrame({'Count': mat_counts, 'Percentage_of_Respondents': mat_pct})
    
    # 2. Size Distribution
    exploded_sizes = parse_multiselect(df_raw[size_col])
    size_counts = exploded_sizes.value_counts()
    size_pct = (size_counts / total_respondents * 100).round(2)
    sizes_df = pd.DataFrame({'Count': size_counts, 'Percentage_of_Respondents': size_pct})
    
    # 3. Apparel Design Placement Matrix Statistics
    rating_summary = []
    for col in apparel_ratings.columns:
        series = apparel_ratings[col].dropna()
        mean_val = series.mean()
        std_val = series.std()
        counts = series.value_counts(normalize=True) * 100
        
        rating_summary.append({
            'Design_Element': col,
            'Mean_Score': round(mean_val, 2),
            'Std_Dev': round(std_val, 2),
            'Not_Preferred_Pct': round(counts.get(1, 0.0), 2),
            'Preferred_Pct': round(counts.get(2, 0.0), 2),
            'Highly_Preferred_Pct': round(counts.get(3, 0.0), 2)
        })
        
    apparel_matrix_df = pd.DataFrame(rating_summary).sort_values(by='Mean_Score', ascending=False).reset_index(drop=True)
    
    # 4. Sweatshirt WTP Distribution
    wtp_counts = df_raw[wtp_col].value_counts()
    wtp_pct = (wtp_counts / total_respondents * 100).round(2)
    wtp_df = pd.DataFrame({'Count': wtp_counts, 'Percentage': wtp_pct})
    
    # 5. Non-conventional Apparel & Cut Requests (Oversized, Baggy, Drop shoulder)
    fit_responses = df_raw[non_conv_apparel_col].dropna().tolist()
    cleaned_fits = [r.strip() for r in fit_responses if r.strip() and r.strip().lower() not in ['nil', 'no', 'none']]
    
    return {
        'materials_df': materials_df,
        'sizes_df': sizes_df,
        'apparel_matrix_df': apparel_matrix_df,
        'wtp_df': wtp_df,
        'fit_requests': cleaned_fits
    }


if __name__ == '__main__':
    from src.data_preprocessing import preprocess_dataset
    data = preprocess_dataset('data/iiserm_merch_survey_data.csv')
    res = analyze_apparel(data['df_raw'], data['apparel_ratings'])
    print("=== DESIGN PLACEMENT MATRIX ===")
    print(res['apparel_matrix_df'])
    print("\n=== SWEATSHIRT WTP ===")
    print(res['wtp_df'])
