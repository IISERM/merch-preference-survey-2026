"""
Demographic & Purchasing Behavior Analysis Module.

Analyzes respondent distribution by academic program/batch, fields of interest,
and annual merchandise purchasing volume statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from src.data_preprocessing import parse_multiselect


def analyze_demographics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes statistical metrics and distributions for demographic fields.
    """
    affiliation_col = 'Your affiliation with institute?\n(batch or program, in case of students)'
    field_col = 'Which area(s)/field(s) are you interested in?'
    purchase_col = 'How many merch do you buy per year?'
    
    total_respondents = len(df)
    
    # 1. Affiliation breakdown
    affiliation_counts = df[affiliation_col].value_counts(dropna=False)
    affiliation_pct = (affiliation_counts / total_respondents * 100).round(2)
    affiliation_df = pd.DataFrame({'Count': affiliation_counts, 'Percentage': affiliation_pct})
    
    # 2. Fields of Interest breakdown
    exploded_fields = parse_multiselect(df[field_col])
    field_counts = exploded_fields.value_counts()
    field_pct = (field_counts / total_respondents * 100).round(2)
    fields_df = pd.DataFrame({'Count': field_counts, 'Percentage_of_Respondents': field_pct})
    
    # 3. Annual Purchases per year statistics
    purchase_series = df[purchase_col].dropna()
    purchase_stats = {
        'mean': round(purchase_series.mean(), 2),
        'std': round(purchase_series.std(), 2),
        'median': round(purchase_series.median(), 2),
        'q25': round(purchase_series.quantile(0.25), 2),
        'q75': round(purchase_series.quantile(0.75), 2),
        'iqr': round(purchase_series.quantile(0.75) - purchase_series.quantile(0.25), 2),
        'min': int(purchase_series.min()),
        'max': int(purchase_series.max())
    }
    
    return {
        'total_respondents': total_respondents,
        'affiliation_df': affiliation_df,
        'fields_df': fields_df,
        'purchase_stats': purchase_stats
    }


if __name__ == '__main__':
    from src.data_preprocessing import preprocess_dataset
    data = preprocess_dataset('data/iiserm_merch_survey_data.csv')
    res = analyze_demographics(data['df_raw'])
    print("=== AFFILIATION ===")
    print(res['affiliation_df'])
    print("\n=== FIELDS OF INTEREST ===")
    print(res['fields_df'])
    print("\n=== PURCHASING STATS ===")
    print(res['purchase_stats'])
