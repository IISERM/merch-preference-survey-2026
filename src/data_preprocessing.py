"""
Data Preprocessing Module for IISER Mohali Merchandise Preference Survey 2026.

This module loads the raw survey CSV data, normalizes column headers,
parses multi-select delimited strings into lists, encodes Likert responses into
numerical matrices, and cleans open-ended qualitative text fields.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


# Likert Scale Mappings
APPAREL_DESIGN_MAP = {
    'Not Preferred': 1,
    'Preferred': 2,
    'Highly Preferred': 3
}

DECISION_FACTOR_MAP = {
    'Not at all': 1,
    'Low Priority': 2,
    'Maybe/Sometimes': 3,
    'High Priority': 4,
    'Absolutely/Of course': 5
}


def load_raw_data(file_path: str) -> pd.DataFrame:
    """Loads raw CSV survey dataset from the specified file path."""
    return pd.read_csv(file_path)


def parse_multiselect(series: pd.Series, delimiter: str = ';') -> pd.Series:
    """
    Parses a Series containing delimited multi-select strings into exploded lists.
    Returns a cleaned Series of individual selections.
    """
    return series.dropna().str.split(delimiter).explode().str.strip()


def encode_apparel_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies apparel design element rating columns and converts Likert choices
    to numerical values (1=Not Preferred, 2=Preferred, 3=Highly Preferred).
    """
    design_cols = [c for c in df.columns if 'Please rate the importance of the following design elements' in c]
    encoded_df = pd.DataFrame(index=df.index)
    for col in design_cols:
        short_name = col.split('[')[1].replace(']', '').strip()
        encoded_df[short_name] = df[col].map(APPAREL_DESIGN_MAP)
    return encoded_df


def encode_decision_factors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies purchase decision driver columns and converts Likert choices
    to numerical values (1=Not at all to 5=Absolutely/Of course).
    """
    factor_cols = [c for c in df.columns if 'What matters the most when buying a merch?' in c]
    encoded_df = pd.DataFrame(index=df.index)
    for col in factor_cols:
        short_name = col.split('[')[1].replace(']', '').strip()
        encoded_df[short_name] = df[col].map(DECISION_FACTOR_MAP)
    return encoded_df


def preprocess_dataset(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Executes full preprocessing pipeline on raw survey data.
    
    Returns a dictionary containing:
    - 'df_raw': Original DataFrame
    - 'apparel_ratings': Numeric DataFrame of design element ratings
    - 'decision_factors': Numeric DataFrame of purchasing decision factors
    """
    df_raw = load_raw_data(file_path)
    apparel_ratings = encode_apparel_ratings(df_raw)
    decision_factors = encode_decision_factors(df_raw)
    
    return {
        'df_raw': df_raw,
        'apparel_ratings': apparel_ratings,
        'decision_factors': decision_factors
    }


if __name__ == '__main__':
    data_dict = preprocess_dataset('data/iiserm_merch_survey_data.csv')
    print("Preprocessing completed successfully.")
    print(f"Total respondents: {len(data_dict['df_raw'])}")
