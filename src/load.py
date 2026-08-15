def count_rows():
    """
    Count the total number of transaction rows without loading
    the complete dataset into memory.
    """
    row_count = 0

    for chunk in pd.read_csv(CSV_FILE, usecols=["step"], chunksize=500_000):
        row_count += len(chunk)

    return row_count