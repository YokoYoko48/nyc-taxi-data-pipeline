import os
import logging
import requests
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path

# 1. Setup Logging
logging.basicConfig(
    filename='pipeline_run.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
TAXI_TYPES = {
    "Yellow Taxi": "yellow_tripdata",
    "Green Taxi": "green_tripdata",
    "FHV": "fhv_tripdata",
    "High Volume FHV": "fhvhv_tripdata"
}

def setup_directories():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Directories setup completed.")

def extract_data(year, months):
    '''Extract metadata from Parquet files'''
    pipeline_data = []
    
    for name, prefix in TAXI_TYPES.items():
        for month in months:
            fname = f"{prefix}_{year}-{month:02d}.parquet"
            file_path = DATA_DIR / fname
            
            if not file_path.exists():
                url = f"{BASE_URL}/{fname}"
                try:
                    res = requests.get(url, timeout=120)
                    res.raise_for_status()
                    file_path.write_bytes(res.content)
                    logging.info(f"Downloaded: {fname}")
                except Exception as error:
                    logging.error(f"Failed to download {fname}: {error}")
                    continue
            
            pf = pq.ParquetFile(file_path)
            pipeline_data.append({
                "Taxi Category": name,
                "YearMonth": f"{year}-{month:02d}",
                "Trip Count": pf.metadata.num_rows
            })
            
    return pd.DataFrame(pipeline_data)

def validate_data(df):
    '''Validate data quality'''
    logging.info("Starting Data Validation...")
    if df.isnull().values.any():
        logging.warning("Data contains null values!")
        df = df.dropna()
        
    invalid_rows = df[df["Trip Count"] < 0]
    if not invalid_rows.empty:
        logging.error(f"Found {len(invalid_rows)} rows with negative Trip Count.")
        raise ValueError("Data Validation Failed: Negative Trip Count")
        
    logging.info("Data Validation Passed.")
    return df

def transform_and_load(df):
    '''Transform and save curated output'''
    df_final = df.groupby("Taxi Category", as_index=False)["Trip Count"].sum()
    df_final = df_final.sort_values("Trip Count", ascending=False).reset_index(drop=True)
    
    total_trips = df_final["Trip Count"].sum()
    df_final["Share (%)"] = (df_final["Trip Count"] / total_trips * 100).round(2)
    
    output_path = OUTPUT_DIR / "curated_taxi_summary.csv"
    df_final.to_csv(output_path, index=False)
    logging.info(f"Curated output saved to {output_path}")
    
    return df_final

def main():
    logging.info("--- Starting NYC Taxi Data Pipeline ---")
    setup_directories()
    
    YEAR = 2024
    MONTHS = range(1, 7) 
    
    df_raw = extract_data(YEAR, MONTHS)
    df_valid = validate_data(df_raw)
    df_final = transform_and_load(df_valid)
    
    logging.info("--- Pipeline Execution Completed Successfully ---")
    print("Pipeline Execution Completed. Final Results:")
    print(df_final)

if __name__ == "__main__":
    main()
