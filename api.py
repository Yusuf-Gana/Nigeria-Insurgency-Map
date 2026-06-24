from fastapi import FastAPI
import asyncpg
import json

app = FastAPI(title="Nigeria Security OSINT API")

# Updated with your local postgres credentials
DB_URL = "postgresql://postgres:copadmin@localhost/security_db"

@app.get("/api/incidents")
async def get_incidents():
    conn = await asyncpg.connect(DB_URL)
    
    query = """
        SELECT 
            id, 
            description, 
            confidence_score, 
            ST_AsGeoJSON(location) as geojson 
        FROM security_incidents;
    """
    rows = await conn.fetch(query)
    await conn.close()

    features = []
    for row in rows:
        features.append({
            "type": "Feature",
            "geometry": json.loads(row['geojson']),
            "properties": {
                "id": row['id'],
                "description": row['description'],
                "confidence": row['confidence_score']
            }
        })
        
    return {"type": "FeatureCollection", "features": features}