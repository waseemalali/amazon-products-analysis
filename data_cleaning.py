# ============================================
# Amazon Products Data Cleaning
# ============================================

# 1. Import Libraries
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "data" / "amazon.csv"
OUTPUT_PATH = BASE_DIR / "data" / "amazon_cleaned.csv"

# ============================================
# 2. Load Dataset
# ============================================

df = pd.read_csv(INPUT_PATH)

print("="*50)
print("First 5 Rows")
print(df.head())

print("="*50)
print("Dataset Shape")
print(df.shape)

print("="*50)
print("Columns")
print(df.columns)

print("="*50)
print("Data Types")
print(df.info())

# ============================================
# 3. Clean Column Names
# ============================================

df.columns = df.columns.str.strip()

print("\nColumns after cleaning:")
print(df.columns)

# ============================================
# 4. Check Missing Values
# ============================================

print("\nMissing Values")
print(df.isnull().sum())

# ============================================
# 5. Check Duplicates
# ============================================

print("\nDuplicate Rows:", df.duplicated().sum())

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# ============================================
# 6. Clean Price Columns
# ============================================

price_columns = [
    "discounted_price",
    "actual_price"
]

for col in price_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(r"[^\d.]", "", regex=True)
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# ============================================
# 7. Clean Discount Percentage
# ============================================

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"],
    errors="coerce"
)

df["discount_percentage"] = df["discount_percentage"] / 100

# ============================================
# 8. Clean Rating
# ============================================

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

# ============================================
# 9. Clean Rating Count
# ============================================

df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df["rating_count"] = pd.to_numeric(
    df["rating_count"],
    errors="coerce"
)

# ============================================
# 10. Create Main Category
# ============================================

df["Main_Category"] = (
    df["category"]
    .astype(str)
    .str.split("|")
    .str[0]
)

# ============================================
# 11. Missing Values After Cleaning
# ============================================

print("\nMissing Values After Cleaning")
print(df.isnull().sum())

# ============================================
# 12. Remove Missing Rows
# ============================================

rows_before = len(df)

df.dropna(inplace=True)

rows_after = len(df)

print("\nRows Before:", rows_before)
print("Rows After :", rows_after)
print("Rows Removed:", rows_before - rows_after)

# ============================================
# 13. Check Data Types
# ============================================

print("\nFinal Data Types")
print(df.info())

# ============================================
# 14. Descriptive Statistics
# ============================================

print("\nNumerical Statistics")
print(df.describe())

print("\nCategorical Statistics")
print(df.describe(include="object"))

# ============================================
# 15. Save Clean Dataset
# ============================================


# Save Clean Dataset
df.to_csv(OUTPUT_PATH, index=False)

print("Dataset cleaned successfully.")
print(f"Saved to: {OUTPUT_PATH}")