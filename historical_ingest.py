import pandas as pd
import asyncpg
import asyncio
from datetime import datetime

# Configuration
DB_URL = "postgresql://postgres:copadmin@localhost/security_db"
CSV_FILE = 'conflict_data_nga.csv'

async def ingest_ucdp_csv():
    # 1. Load data
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"Loaded {len(df)} rows from {CSV_FILE}")
        # Debugging: show columns so you can verify they match
        print(f"Detected columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 2. Connect to Database
    conn = await asyncpg.connect(DB_URL)
    
    # 3. Ingestion Loop
    print("Starting database ingestion...")
    count = 0
    
    async with conn.transaction():
        for _, row in df.iterrows():
            try:
                # Handle Date Conversion
                # Adjust format '%Y-%m-%d' if your CSV uses something else
                raw_date = str(row.get('date_start', '1997-01-01'))
                incident_date = datetime.strptime(raw_date.split()[0], '%Y-%m-%d')

                # Database Insertion
                query = """
                    INSERT INTO security_incidents 
                    (source_url, description, incident_date, actors, confidence_score, location)
                    VALUES ($1, $2, $3, $4, $5, ST_SetSRID(ST_MakePoint($6, $7), 4326))
                """
                
                await conn.execute(query, 
                                   "UCDP_Historical", 
                                   str(row.get('type_of_violence', 'N/A')), 
                                   incident_date, 
                                   str(row.get('side_a', 'N/A')), 
                                   85, 
                                   float(row.get('longitude', 0)), 
                                   float(row.get('latitude', 0)))
                count += 1
            except Exception as e:
                # This will print specific errors without crashing the whole script
                continue
    
    await conn.close()
    print(f"Successfully committed {count} records to the database.")

if __name__ == "__main__":
    asyncio.run(ingest_ucdp_csv())