import os
import asyncio
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("back-end2")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "labdb")
PORT = int(os.getenv("PORT", 5000))

app = FastAPI(title="back-end2-db-service")

class SubmissionIn(BaseModel):
    name: str
    email: str

class SubmissionOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime  # Changed from str to datetime

pool: Optional[asyncpg.pool.Pool] = None

@app.on_event("startup")
async def startup():
    global pool
    try:
        logger.info("Connecting to Postgres %s:%s db=%s user=%s", DB_HOST, DB_PORT, DB_NAME, DB_USER)
        pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            min_size=1,
            max_size=10,
            timeout=10
        )
        # test simple
        async with pool.acquire() as conn:
            await conn.execute("""CREATE TABLE IF NOT EXISTS submissions (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )""")
        logger.info("Connected to Postgres and ensured table exists.")
    except Exception as exc:
        logger.exception("Failed to connect or init DB: %s", exc)
        raise

@app.on_event("shutdown")
async def shutdown():
    global pool
    if pool:
        await pool.close()
        logger.info("Postgres pool closed")

@app.get("/healthz")
async def health():
    return {"ok": True}

@app.get("/api/submissions", response_model=List[SubmissionOut])
async def get_submissions():
    global pool
    if not pool:
        logger.error("DB pool is not initialized")
        raise HTTPException(status_code=500, detail="DB pool not initialized")
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch('SELECT id, name, email, created_at FROM submissions ORDER BY id DESC')
            return [SubmissionOut(**dict(r)) for r in rows]
    except Exception as e:
        logger.exception("Error fetching submissions: %s", e)
        raise HTTPException(status_code=500, detail="Error querying DB")

@app.post("/api/submit")
async def create_submission(payload: SubmissionIn):
    if not payload.name or not payload.email:
        raise HTTPException(status_code=400, detail="name and email required")
    if not pool:
        logger.error("DB pool is not initialized (POST)")
        raise HTTPException(status_code=500, detail="DB pool not initialized")
    try:
        async with pool.acquire() as conn:
            await conn.execute('INSERT INTO submissions(name, email) VALUES($1, $2)', payload.name, payload.email)
            return {"message": "created"}
    except Exception as e:
        logger.exception("Error inserting submission: %s", e)
        raise HTTPException(status_code=500, detail="Error inserting to DB")
