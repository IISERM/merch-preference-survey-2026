"""
Consumer Psychology, Purchasing Drivers & Theme Analysis Module.

Evaluates decision drivers (Likert 1-5 scale), brand loyalty / blind buying habits,
theme popularity rankings, and qualitative creative feedback.
"""

import pandas as pd
from typing import Dict, Any
from src.data_preprocessing import parse_multiselect, encode_decision_factors


def analyze_consumer_psychology(df_raw: pd.DataFrame, decision_factors: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes statistical indicators for purchasing drivers, brand loyalty, and theme preferences.
    """
    blind_col = 'Will you buy any merch blindly of a particular IISERM club/community?'
    theme_col = 'What theme or concept should the merch design revolve around?'
    general_idea_col = 'Describe your in-general merch design idea.'
    turing_idea_col = 'Describe your Turing-specific merch design idea.'
    
    total_respondents = len(df_raw)
    
    # 1. Purchase Decision Factor Matrix (1-5 Likert Scale)
    factor_summary = []
    for col in decision_factors.columns:
        series = decision_factors[col].dropna()
        mean_val = series.mean()
        std_val = series.std()
        
        # High or Absolute Priority (scores 4 and 5)
        high_priority_pct = ((series >= 4).sum() / len(series) * 100)
        
        factor_summary.append({
            'Decision_Factor': col,
            'Mean_Score': round(mean_val, 2),
            'Std_Dev': round(std_val, 2),
            'High_or_Absolute_Priority_Pct': round(high_priority_pct, 2)
        })
        
    decision_matrix_df = pd.DataFrame(factor_summary).sort_values(by='Mean_Score', ascending=False).reset_index(drop=True)
    
    # 2. Blind Loyalty / Brand Loyalty Analysis
    blind_counts = df_raw[blind_col].value_counts(dropna=False)
    valid_blind_total = df_raw[blind_col].dropna().count()
    blind_pct = (blind_counts / valid_blind_total * 100).round(2)
    blind_loyalty_df = pd.DataFrame({'Count': blind_counts, 'Percentage_Valid': blind_pct})
    
    # 3. Theme Preferences Ranking
    exploded_themes = parse_multiselect(df_raw[theme_col])
    theme_counts = exploded_themes.value_counts()
    theme_pct = (theme_counts / total_respondents * 100).round(2)
    themes_df = pd.DataFrame({'Count': theme_counts, 'Percentage_of_Respondents': theme_pct})
    
    # 4. Design Ideas (Qualitative extraction)
    general_ideas = [r.strip() for r in df_raw[general_idea_col].dropna().tolist() if r.strip() and r.strip().lower() not in ['no', 'nil']]
    turing_ideas = [r.strip() for r in df_raw[turing_idea_col].dropna().tolist() if r.strip() and r.strip().lower() not in ['no', 'nil']]
    
    return {
        'decision_matrix_df': decision_matrix_df,
        'blind_loyalty_df': blind_loyalty_df,
        'themes_df': themes_df,
        'general_ideas': general_ideas,
        'turing_ideas': turing_ideas
    }


if __name__ == '__main__':
    from src.data_preprocessing import preprocess_dataset
    data = preprocess_dataset('data/iiserm_merch_survey_data.csv')
    res = analyze_consumer_psychology(data['df_raw'], data['decision_factors'])
    print("=== DECISION DRIVER MATRIX ===")
    print(res['decision_matrix_df'])
    print("\n=== BLIND LOYALTY ===")
    print(res['blind_loyalty_df'])
    print("\n=== THEMES RANKING ===")
    print(res['themes_df'])
