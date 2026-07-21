import pandas as pd


def clean_data(
    df,
    remove_duplicates=True,
    fill_missing=True,
    strip_spaces=True,
    drop_empty=False
):

    # Create a copy so the original data is not modified
    df = df.copy()

    rows_before = len(df)

    # ----------------------------
    # Remove extra spaces
    # ----------------------------
    if strip_spaces:

        # Clean column names
        df.columns = df.columns.str.strip()

        # Clean text values
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip()

    # ----------------------------
    # Remove duplicate rows
    # ----------------------------
    if remove_duplicates:
        df = df.drop_duplicates()

    # ----------------------------
    # Convert numeric-like text to numbers
    # ----------------------------
    for col in df.columns:

        if df[col].dtype == "object":

            converted = pd.to_numeric(df[col], errors="coerce")

            # If most values become numeric, keep it as numeric
            if converted.notna().sum() > len(df) / 2:
                df[col] = converted

    # ----------------------------
    # Fill missing values
    # ----------------------------
    if fill_missing:

        for col in df.columns:

            if pd.api.types.is_numeric_dtype(df[col]):

                mean_value = df[col].mean()

                if pd.notna(mean_value):
                    df[col] = df[col].fillna(mean_value)

            else:

                mode = df[col].mode()

                if not mode.empty:
                    df[col] = df[col].fillna(mode.iloc[0])

    # ----------------------------
    # Drop empty rows
    # ----------------------------
    if drop_empty:
        df = df.dropna(how="all")

    rows_after = len(df)

    return df, rows_before, rows_after