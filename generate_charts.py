#!/usr/bin/env python3
"""
Chart Generator Script for IISER Mohali Merchandise Preference Survey 2026.

Generates high-resolution visualization charts for survey demographics, category demand,
apparel placement preferences, pricing corridors, decision drivers, and design themes.
Saves figure outputs into assets/charts/.
"""

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_preprocessing import preprocess_dataset
from src.demographic_analysis import analyze_demographics
from src.merch_preference_analysis import analyze_merchandise_preferences
from src.apparel_analysis import analyze_apparel
from src.consumer_psychology_analysis import analyze_consumer_psychology


def setup_style():
    """Configures clean, modern Matplotlib plot styling."""
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#e2e8f0'
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['grid.color'] = '#f1f5f9'
    plt.rcParams['grid.linestyle'] = '--'


def generate_all_charts():
    setup_style()
    
    # Directory setup
    out_dir = os.path.join(os.path.dirname(__file__), 'assets', 'charts')
    os.makedirs(out_dir, exist_ok=True)
    
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'iiserm_merch_survey_data.csv')
    data = preprocess_dataset(data_path)
    df_raw = data['df_raw']
    apparel_ratings = data['apparel_ratings']
    decision_factors = data['decision_factors']
    
    # ---------------------------------------------------------
    # Chart 1: Demographics & Fields of Study
    # ---------------------------------------------------------
    demo = analyze_demographics(df_raw)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    aff_df = demo['affiliation_df'].copy()
    aff_labels = [str(x) if pd.notnull(x) else 'Unspecified' for x in aff_df.index]
    colors1 = ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', '#eff6ff', '#cbd5e1']
    bars1 = ax1.bar(aff_labels, aff_df['Count'], color=colors1[:len(aff_df)], edgecolor='#1e40af', linewidth=0.8)
    ax1.set_title('Respondent Distribution by Batch / Program', fontsize=12, fontweight='bold', pad=12)
    ax1.set_ylabel('Number of Respondents', fontsize=10)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f"{int(yval)}", ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax1.set_ylim(0, max(aff_df['Count']) + 3)
    
    fields_df = demo['fields_df'].sort_values(by='Count', ascending=True)
    field_labels = [str(x) for x in fields_df.index]
    bars2 = ax2.barh(field_labels, fields_df['Percentage_of_Respondents'], color='#0284c7', edgecolor='#0369a1', linewidth=0.8)
    ax2.set_title('Academic Discipline / Fields of Interest (%)', fontsize=12, fontweight='bold', pad=12)
    ax2.set_xlabel('% of Respondents (N=55)', fontsize=10)
    for bar in bars2:
        xval = bar.get_width()
        ax2.text(xval + 1, bar.get_y() + bar.get_height()/2, f"{xval:.1f}%", ha='left', va='center', fontsize=9, fontweight='bold')
    ax2.set_xlim(0, 75)
    
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'demographics.png'), dpi=300)
    plt.close()
    print("Saved assets/charts/demographics.png")
    
    # ---------------------------------------------------------
    # Chart 2: Category Demand Rankings
    # ---------------------------------------------------------
    merch = analyze_merchandise_preferences(df_raw)
    cats_df = merch['categories_df'].head(10).sort_values(by='Percentage_of_Respondents', ascending=True)
    cat_labels = [str(x) for x in cats_df.index]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(cat_labels, cats_df['Percentage_of_Respondents'], color='#2563eb', edgecolor='#1d4ed8')
    ax.set_title('Merchandise Category Interest Level (%)', fontsize=13, fontweight='bold', pad=14)
    ax.set_xlabel('% of Respondents Interested in Category', fontsize=10)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", ha='left', va='center', fontsize=9.5, fontweight='bold')
    ax.set_xlim(0, 90)
    
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'category_demand.png'), dpi=300)
    plt.close()
    print("Saved assets/charts/category_demand.png")
    
    # ---------------------------------------------------------
    # Chart 3: Apparel Design Element Placement Matrix
    # ---------------------------------------------------------
    apparel = analyze_apparel(df_raw, apparel_ratings)
    matrix_df = apparel['apparel_matrix_df'].sort_values(by='Mean_Score', ascending=True)
    matrix_labels = [str(x) for x in matrix_df['Design_Element']]
    
    colors3 = []
    for elem in matrix_labels:
        if 'back' in elem.lower() and 'hero' in elem.lower():
            colors3.append('#16a34a')
        elif 'front' in elem.lower() and 'hero' in elem.lower():
            colors3.append('#dc2626')
        elif 'iiserm' in elem.lower() or 'logo' in elem.lower():
            colors3.append('#2563eb')
        else:
            colors3.append('#64748b')
            
    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(matrix_labels, matrix_df['Mean_Score'], color=colors3, height=0.65)
    ax.set_title('Apparel Placement Preference Scores (1 = Not Preferred, 3 = Highly Preferred)', fontsize=12, fontweight='bold', pad=14)
    ax.set_xlabel('Mean Score (Scale 1.0 to 3.0)', fontsize=10)
    ax.set_xlim(1.0, 2.6)
    ax.axvline(2.0, color='#94a3b8', linestyle=':', label='Neutral Preference Benchmark (2.0)')
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.02, bar.get_y() + bar.get_height()/2, f"{w:.2f}", ha='left', va='center', fontsize=9.5, fontweight='bold')
        
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'apparel_design_matrix.png'), dpi=300)
    plt.close()
    print("Saved assets/charts/apparel_design_matrix.png")
    
    # ---------------------------------------------------------
    # Chart 4: Sweatshirt Pricing Willingness-to-Pay (WTP)
    # ---------------------------------------------------------
    wtp_df = apparel['wtp_df']
    order = ['200 - 400 INR', '400 - 600 INR', '600 - 800 INR', '800 - 1000 INR', '1000 - 1500 INR']
    wtp_ordered = wtp_df.reindex(order).dropna()
    wtp_labels = [str(x) for x in wtp_ordered.index]
    
    fig, ax = plt.subplots(figsize=(9, 5))
    colors4 = ['#93c5fd', '#2563eb', '#1d4ed8', '#f59e0b', '#ef4444']
    bars = ax.bar(wtp_labels, wtp_ordered['Percentage'], color=colors4, edgecolor='#1e293b', linewidth=0.8)
    ax.set_title('Sweatshirt / Hoodie Willingness to Pay (WTP) Distribution', fontsize=13, fontweight='bold', pad=14)
    ax.set_ylabel('% of Respondents', fontsize=10)
    ax.set_xlabel('Price Corridor (INR)', fontsize=10)
    ax.set_ylim(0, 42)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold')
        
    ax.annotate('Optimal Corridor\n(500 - 750 INR)', xy=(1.5, 33), xytext=(2.2, 35),
                arrowprops=dict(facecolor='#0f172a', shrink=0.08, width=1.5, headwidth=6),
                fontsize=10, fontweight='bold', color='#1e293b')
                
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'sweatshirt_pricing_wtp.png'), dpi=300)
    plt.close()
    print("Saved assets/charts/sweatshirt_pricing_wtp.png")
    
    # ---------------------------------------------------------
    # Chart 5: Purchasing Decision Drivers Matrix
    # ---------------------------------------------------------
    psych = analyze_consumer_psychology(df_raw, decision_factors)
    drivers_df = psych['decision_matrix_df'].sort_values(by='Mean_Score', ascending=True)
    driver_labels = [str(x) for x in drivers_df['Decision_Factor']]
    
    colors5 = ['#ef4444' if 'club' in d.lower() else ('#16a34a' if s >= 4.3 else '#2563eb') 
               for d, s in zip(driver_labels, drivers_df['Mean_Score'])]
               
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(driver_labels, drivers_df['Mean_Score'], color=colors5, height=0.6)
    ax.set_title('Merchandise Purchase Decision Drivers (Scale 1.0 to 5.0)', fontsize=13, fontweight='bold', pad=14)
    ax.set_xlabel('Mean Score (1 = Not at all, 5 = Absolutely/Of course)', fontsize=10)
    ax.set_xlim(1.0, 5.2)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.05, bar.get_y() + bar.get_height()/2, f"{w:.2f}", ha='left', va='center', fontsize=9.5, fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'decision_drivers.png'), dpi=300)
    plt.close()
    print("Saved assets/charts/decision_drivers.png")
    
    # ---------------------------------------------------------
    # Chart 6: Design Theme Preferences
    # ---------------------------------------------------------
    themes_df = psych['themes_df'].head(8).sort_values(by='Percentage_of_Respondents', ascending=True)
    theme_labels = [str(x) for x in themes_df.index]
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(theme_labels, themes_df['Percentage_of_Respondents'], color='#0284c7', edgecolor='#0369a1')
    ax.set_title('Preferred Design Themes & Concepts (%)', fontsize=13, fontweight='bold', pad=14)
    ax.set_xlabel('% of Respondents', fontsize=10)
    ax.set_xlim(0, 75)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", ha='left', va='center', fontsize=9.5, fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'themes_ranking.png'), dpi=300)
    plt.close()
    print("Saved assets/charts/themes_ranking.png")
    
    print("\nAll charts successfully generated in assets/charts/")


if __name__ == '__main__':
    generate_all_charts()
