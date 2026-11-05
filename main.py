from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(
    title="Zoo Visitors API",
    description="API ข้อมูลสถิติผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
    version="1.0.0"
)

RESOURCE_ID = "0ecc96cf-d914-42a1-b184-dbbd013c3c9c"

@app.get("/")
def home():
    return {
        "message": "Zoo Visitors API is running",
        "docs": "/docs",
        "endpoint": "/api/zoo-visitors"
    }

@app.get("/api/zoo-visitors")
def get_zoo_visitors():
    url = f"https://data.go.th/api/3/action/datastore_search?resource_id={RESOURCE_ID}"
    
    # เพิ่ม User-Agent เพื่อป้องกันโดน Data.go.th บล็อก (403 Forbidden)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        records = data.get("result", {}).get("records", [])
        
        return {
            "dataset": "ข้อมูลรายงานสถิติผู้เข้าชมสวนสัตว์",
            "source": "Data.go.th",
            "resource_id": RESOURCE_ID,
            "fiscal_year": 2569,
            "total_records": len(records),
            "data": records
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงข้อมูล: {str(e)}"
        )