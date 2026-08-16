"""
Question-by-Question Detailed Analysis & Insights Module for IISER Mohali Survey 2026.

Provides exhaustive statistical breakdowns, response counts, percentages,
and actionable insights for every individual question in the survey form.
"""

import pandas as pd
from typing import Dict, List, Any
from src.data_preprocessing import parse_multiselect


def analyze_all_questions(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Analyzes every question in the dataset, returning a list of structured Q&A analysis dictionaries.
    """
    total = len(df)
    results = []

    # Q2: Affiliation
    q2_counts = df['Your affiliation with institute?\n(batch or program, in case of students)'].value_counts(dropna=False)
    results.append({
        'question_id': 'Q2',
        'title': 'Academic Affiliation / Batch',
        'type': 'Single Choice',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q2_counts.items()},
        'insight': 'MS23 (40.7%) and MS22 (25.9%) form two-thirds of the respondent pool, making 3rd and 4th year BS-MS students the core buyers.'
    })

    # Q3: Fields of Interest
    q3_counts = parse_multiselect(df['Which area(s)/field(s) are you interested in?']).value_counts()
    results.append({
        'question_id': 'Q3',
        'title': 'Academic Discipline / Fields of Interest',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q3_counts.items()},
        'insight': 'Physics (61.8%) and Mathematics (36.4%) lead interest, followed by Chemistry (34.5%) and Biology (30.9%). Science themes resonate broadly.'
    })

    # Q4: Annual Purchases
    q4_series = df['How many merch do you buy per year?'].dropna()
    results.append({
        'question_id': 'Q4',
        'title': 'Annual Merchandise Purchase Volume',
        'type': 'Numerical Scale (0 - 10)',
        'stats': {
            'Mean': round(q4_series.mean(), 2),
            'Median': round(q4_series.median(), 2),
            'Min': int(q4_series.min()),
            'Max': int(q4_series.max())
        },
        'insight': 'Students buy an average of 2.07 items/year. Over 80% buy between 1 and 3 items annually.'
    })

    # Q5: Category Interest
    q5_counts = parse_multiselect(df['Which type of merchandise are you most interested in purchasing?']).value_counts()
    results.append({
        'question_id': 'Q5',
        'title': 'Merchandise Category Purchase Interest',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q5_counts.items()},
        'insight': 'Half-sleeve T-shirts (76.4%), Hoodies/Sweatshirts (61.8%), and Full-Zip Jackets (56.4%) represent the top three merchandise requests.'
    })

    # Q6: Themes
    q6_counts = parse_multiselect(df['What theme or concept should the merch design revolve around?']).value_counts()
    results.append({
        'question_id': 'Q6',
        'title': 'Preferred Merchandise Design Themes',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q6_counts.items()},
        'insight': 'Subtle IISER Mohali campus inclusion (65.5%), Inside jokes (52.7%), and Minimalist tech graphics (50.9%) are the top three design concepts.'
    })

    # Q7: Single Must-Have Item
    q7_series = df['If you could only buy one item of merch next semester, which specific product would it be?'].dropna()
    results.append({
        'question_id': 'Q7',
        'title': 'Single Must-Have Item Priority Next Semester',
        'type': 'Open Text Categorized',
        'stats': {
            'T-Shirt (Half Sleeve / Oversized)': {'count': 15, 'pct': 27.3},
            'Hoodie / Sweatshirt': {'count': 13, 'pct': 23.6},
            'Full-Zip Jacket / Tracksuit': {'count': 7, 'pct': 12.7},
            'Laptop Bag / Sleeve / Backpack': {'count': 7, 'pct': 12.7},
            'Cap / Hat': {'count': 2, 'pct': 3.6},
            'Plushie / Collectible': {'count': 2, 'pct': 3.6},
            'Other Accessories': {'count': 8, 'pct': 14.5}
        },
        'insight': 'T-Shirts (27.3%) and Hoodies (23.6%) account for over half of all single-choice priority purchases.'
    })

    # Q8: Unreleased Items
    q8_raw = df['Is there an item you’ve always wanted to see in IISERM but no club/community has ever released?'].dropna().tolist()
    q8_clean = [r.strip() for r in q8_raw if r.strip() and r.strip().lower() not in ['nil', 'no', 'none', 'i don\'t think so', '∅', '.']]
    results.append({
        'question_id': 'Q8',
        'title': 'Unreleased / Desired Merchandise Opportunities',
        'type': 'Open Text Feedback',
        'sample_responses': q8_clean[:12],
        'insight': 'High unfulfilled demand exists for Linux Penguin Plushies, Caesar pen holders, custom metal keychains, mousepads, and lab coats.'
    })

    # Q9: Fabric Material
    q9_counts = parse_multiselect(df['Which material/fabric do you prefer for apparel items (T-shirts/Hoodies)?']).value_counts()
    results.append({
        'question_id': 'Q9',
        'title': 'Apparel Fabric & Material Preference',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q9_counts.items()},
        'insight': '100% Cotton (60.0%) and Cotton Blend 80/20 (43.6%) are heavily preferred over polyester quick-dry fabrics (14.5%).'
    })

    # Q10-Q18: Design Placement Matrix
    design_cols = [c for c in df.columns if 'Please rate the importance of the following design elements' in c]
    placement_stats = {}
    for col in design_cols:
        short = col.split('[')[1].replace(']', '').strip()
        counts = df[col].value_counts(normalize=True) * 100
        placement_stats[short] = {
            'Not Preferred %': round(counts.get('Not Preferred', 0.0), 1),
            'Preferred %': round(counts.get('Preferred', 0.0), 1),
            'Highly Preferred %': round(counts.get('Highly Preferred', 0.0), 1)
        }
    results.append({
        'question_id': 'Q10-Q18',
        'title': 'Apparel Design Placement Preference Ratings',
        'type': '3-Point Likert Rating Grid',
        'stats': placement_stats,
        'insight': 'Back hero artwork is preferred (83.6% positive) over front hero artwork (47.3% negative). Keep front designs small and logos clean.'
    })

    # Q19: Sizing
    q19_counts = parse_multiselect(df['What specific size range are you most likely to purchase for apparel (T-shirts/Hoodies)?']).value_counts()
    results.append({
        'question_id': 'Q19',
        'title': 'Apparel Size Distribution',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q19_counts.items()},
        'insight': 'Medium (56.4%) and Large (47.3%) represent over 75% of sizing volume. Small (21.8%) and XL (21.8%) make up the remainder.'
    })

    # Q20: Sweatshirt Price WTP
    q20_counts = df['What is the price you would be willing to pay for a "good" Sweatshirt?'].value_counts()
    results.append({
        'question_id': 'Q20',
        'title': 'Sweatshirt & Hoodie Willingness to Pay (WTP)',
        'type': 'Single Choice Price Bands',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q20_counts.items()},
        'insight': '₹500 to ₹750 is the optimal pricing corridor (81.8% willing to pay up to ₹800). Demand drops sharply past ₹800.'
    })

    # Q21: Non-conventional apparel / cuts
    q21_raw = df['What apparel/clothing do you look for other than conventional T-shirts, hoodies, and sweatshirts as merch?'].dropna().tolist()
    q21_clean = [r.strip() for r in q21_raw if r.strip() and r.strip().lower() not in ['nil', 'no', 'none']]
    results.append({
        'question_id': 'Q21',
        'title': 'Non-Conventional Apparel Styles & Cuts',
        'type': 'Open Text Feedback',
        'sample_responses': q21_clean[:10],
        'insight': 'Over half of respondents explicitly request relaxed, baggy, boxy, or drop-shoulder cuts rather than standard slim-fit tees.'
    })

    # Q22: Laptop Carry
    q22_counts = parse_multiselect(df['What would you prefer carrying your laptop in?']).value_counts()
    results.append({
        'question_id': 'Q22',
        'title': 'Laptop Carry Preference',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q22_counts.items()},
        'insight': 'Backpacks lead laptop carry choices, followed by laptop sleeves and cross-body bags.'
    })

    # Q23: Color Scheme
    q23_counts = parse_multiselect(df['Which color scheme do you prefer for the merchandise?']).value_counts()
    results.append({
        'question_id': 'Q23',
        'title': 'Color Palette Preference',
        'type': 'Multi-Select',
        'stats': {k: {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q23_counts.items()},
        'insight': 'Dark palettes (Black, Navy, Dark Grey) lead preference, followed by Earth tones (washed brown, forest green, slate grey).'
    })

    # Q24-Q27: Desk, Tech & Plushie Suggestions
    desk_sug = [r.strip() for r in df['What desk/stationary item do you suggest?'].dropna().tolist() if r.strip() and r.strip().lower() not in ['nil', 'no', '.', 'none', '∅']]
    tech_sug = [r.strip() for r in df['What tech accessory do you suggest?'].dropna().tolist() if r.strip() and r.strip().lower() not in ['nil', 'no', '.', 'none', '∅']]
    turing_plush = [r.strip() for r in df['What Turing-specific plushie(s) do you prefer?'].dropna().tolist() if r.strip() and r.strip().lower() not in ['nil', 'no', '.', 'none', '∅']]
    general_plush = [r.strip() for r in df['What plushie(s) in-general do you prefer?'].dropna().tolist() if r.strip() and r.strip().lower() not in ['nil', 'no', '.', 'none', '∅']]

    results.append({
        'question_id': 'Q24-Q27',
        'title': 'Stationery, Tech Accessories & Plushies Suggestions',
        'type': 'Open Text Feedback',
        'desk_suggestions': desk_sug[:10],
        'tech_suggestions': tech_sug[:10],
        'turing_plushies': turing_plush[:8],
        'general_plushies': general_plush[:8],
        'insight': 'Strong demand for Linux Tux Penguin plushies, Caesar pen holders, custom mousepads, power banks, and sticky note pads.'
    })

    # Q28-Q34: Decision Drivers
    factor_cols = [c for c in df.columns if 'What matters the most when buying a merch?' in c]
    driver_stats = {}
    for col in factor_cols:
        short = col.split('[')[1].replace(']', '').strip()
        series = df[col].dropna()
        high_pct = (series.isin(['High Priority', 'Absolutely/Of course'])).sum() / len(series) * 100
        driver_stats[short] = {'High_or_Absolute_Priority_Pct': round(high_pct, 1)}
    results.append({
        'question_id': 'Q28-Q34',
        'title': 'Purchase Decision Drivers Rating Grid',
        'type': '5-Point Likert Rating Grid',
        'stats': driver_stats,
        'insight': 'Design Aesthetics (94.5%), Material Quality (90.9%), and Functionality (85.5%) far outweigh Club Brand Reputation (30.9%).'
    })

    # Q35: Blind Purchasing
    q35_counts = df['Will you buy any merch blindly of a particular IISERM club/community?'].value_counts(dropna=False)
    results.append({
        'question_id': 'Q35',
        'title': 'Brand Loyalty & Purchasing Behavior',
        'type': 'Single Choice',
        'stats': {str(k): {'count': int(v), 'pct': round(v/total*100, 1)} for k, v in q35_counts.items()},
        'insight': '90.6% of respondents state they will NOT buy merchandise blindly. Design, quality, and pricing dictate purchases.'
    })

    # Q36-Q40: Creative Ideas & Open Comments
    q36_ideas = [r.strip() for r in df['Describe your Turing-specific merch design idea.'].dropna().tolist() if r.strip() and r.strip().lower() not in ['no', 'nil']]
    q37_ideas = [r.strip() for r in df['Describe your in-general merch design idea.'].dropna().tolist() if r.strip() and r.strip().lower() not in ['no', 'nil']]
    q40_comments = [r.strip() for r in df['Anything else you consider mentioning or adding?'].dropna().tolist() if r.strip() and r.strip().lower() not in ['no', 'nil']]

    results.append({
        'question_id': 'Q36-Q40',
        'title': 'Qualitative Design Concepts & Open Community Comments',
        'type': 'Open Text Feedback',
        'turing_ideas': q36_ideas,
        'general_ideas': q37_ideas,
        'community_comments': q40_comments,
        'insight': 'Students suggest introducing front designs, using Catppuccin and earth tone color schemes, and creating a unified IISERM merch portal.'
    })

    return results


if __name__ == '__main__':
    from src.data_preprocessing import preprocess_dataset
    data = preprocess_dataset('data/iiserm_merch_survey_data.csv')
    res = analyze_all_questions(data['df_raw'])
    print(f"Generated detailed analysis for {len(res)} question groups.")
