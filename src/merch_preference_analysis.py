"""
Merchandise Category Preference & Demand Gap Analysis Module.

Analyzes product category interests, single-item priority choices,
and extracts unreleased product gap insights from qualitative feedback.
"""

import pandas as pd
from typing import Dict, Any, List
from src.data_preprocessing import parse_multiselect


def analyze_merchandise_preferences(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates category preferences, single item priority, and unreleased items.
    """
    category_col = 'Which type of merchandise are you most interested in purchasing?'
    single_item_col = 'If you could only buy one item of merch next semester, which specific product would it be?'
    unreleased_col = 'Is there an item you’ve always wanted to see in IISERM but no club/community has ever released?'
    
    total_respondents = len(df)
    
    # 1. Category Interest Multi-Select Ranking
    exploded_categories = parse_multiselect(df[category_col])
    category_counts = exploded_categories.value_counts()
    category_pct = (category_counts / total_respondents * 100).round(2)
    categories_df = pd.DataFrame({'Count': category_counts, 'Percentage_of_Respondents': category_pct})
    
    # 2. Single Must-Have Item Analysis (Normalized grouping)
    single_items = df[single_item_col].dropna().str.strip().str.lower()
    
    def generalize_item(item: str) -> str:
        if any(w in item for w in ['tshirt', 't shirt', 't-shirt', 'tee']):
            return 'T-Shirt (Half Sleeve / Oversized)'
        elif any(w in item for w in ['hoodie', 'hoddie', 'sweatshirt']):
            return 'Hoodie / Sweatshirt'
        elif 'jacket' in item:
            return 'Full-Zip Jacket'
        elif any(w in item for w in ['laptop bag', 'laptop sleeve', 'laptop case', 'backpack', 'crossbody']):
            return 'Laptop Bag / Sleeve / Backpack'
        elif any(w in item for w in ['cap', 'hat']):
            return 'Cap / Hat'
        elif 'plush' in item:
            return 'Plushie / Collectible'
        elif any(w in item for w in ['mug', 'keychain', 'sticker', 'pin', 'socks', 'pad']):
            return 'Accessories (Mug, Keychain, Stickers, Mousepad)'
        else:
            return 'Other / Custom Request'

    grouped_single_items = single_items.apply(generalize_item).value_counts()
    single_item_pct = (grouped_single_items / len(single_items) * 100).round(2)
    single_items_df = pd.DataFrame({'Count': grouped_single_items, 'Percentage': single_item_pct})
    
    # 3. Unreleased Desired Items (Filtered non-empty text responses)
    unreleased_responses = df[unreleased_col].dropna().tolist()
    cleaned_unreleased = [
        r.strip() for r in unreleased_responses 
        if r.strip() and r.strip().lower() not in ['nil', 'no', 'none', 'i don\'t think so', '∅', '.']
    ]
    
    return {
        'categories_df': categories_df,
        'single_items_df': single_items_df,
        'unreleased_items': cleaned_unreleased
    }


if __name__ == '__main__':
    from src.data_preprocessing import preprocess_dataset
    data = preprocess_dataset('data/iiserm_merch_survey_data.csv')
    res = analyze_merchandise_preferences(data['df_raw'])
    print("=== CATEGORY DEMAND RANKING ===")
    print(res['categories_df'])
    print("\n=== SINGLE MUST-HAVE ITEM ===")
    print(res['single_items_df'])
