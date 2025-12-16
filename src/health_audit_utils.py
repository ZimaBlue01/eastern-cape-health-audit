"""
Eastern Cape Health Audit – Core Utilities

This module contains reusable data cleaning, sampling,
classification, and analysis logic extracted from the Q4 analysis.

ETHICAL NOTE:
-------------
This code is intended to SUPPORT healthcare decision-making,
not replace clinical judgment. Automated classifications should
never be used as the sole basis for treatment or triage decisions,
especially in under-resourced healthcare environments.
"""

import pandas as pd
import numpy as np


# --------------------------------------------------
# 1. DATA CLEANING
# --------------------------------------------------

def clean_health_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the clinic patient dataset by:
    - Removing duplicate rows
    - Filling missing numeric values with column means
    - Normalizing BMI and disease_score using min-max scaling
    """
    cleaned = df.copy()

    # Remove duplicates
    cleaned = cleaned.drop_duplicates()

    # Fill missing numeric values
    numeric_cols = ["age", "BMI", "blood_pressure", "disease_score"]
    for col in numeric_cols:
        cleaned[col] = cleaned[col].fillna(cleaned[col].mean())

    # Min-max normalization
    for col in ["BMI", "disease_score"]:
        cleaned[f"{col}_normalized"] = (
            cleaned[col] - cleaned[col].min()
        ) / (cleaned[col].max() - cleaned[col].min())

    return cleaned


# --------------------------------------------------
# 2. RANDOM SAMPLING
# --------------------------------------------------

def sample_patients(df: pd.DataFrame, n: int = 20, seed: int = 42) -> pd.DataFrame:
    """
    Randomly samples n patients from the dataset for comparison
    against population-level statistics.
    """
    return df.sample(n=n, random_state=seed)


# --------------------------------------------------
# 3. FREQUENCY DISTRIBUTION
# --------------------------------------------------

def age_frequency_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Returns a frequency distribution of patient ages.
    """
    return df["age"].value_counts().sort_index()


# --------------------------------------------------
# 4. NAÏVE BAYES–STYLE CLASSIFICATION
# --------------------------------------------------

def classify_patient(row: pd.Series) -> str:
    """
    Classifies a patient as 'Critical' or 'Stable' using
    a simple probabilistic-style rule:

    - High normalized disease score AND
    - High normalized BMI
    → Critical
    """
    if (
        row["disease_score_normalized"] > 0.6
        and row["BMI_normalized"] > 0.6
    ):
        return "Critical"
    return "Stable"


def apply_risk_classification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the classification logic to the entire dataset.
    """
    classified = df.copy()
    classified["risk_status"] = classified.apply(classify_patient, axis=1)
    return classified


# --------------------------------------------------
# 5. FULL PIPELINE
# --------------------------------------------------

def full_audit_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs the full audit pipeline:
    cleaning → normalization → classification
    """
    cleaned = clean_health_data(df)
    classified = apply_risk_classification(cleaned)
    return classified

