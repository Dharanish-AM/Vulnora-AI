from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import time
import logging
from vulnora.core.scanner import ProjectScanner
from vulnora.models.issue import ScanResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("vulnora.api")

app = FastAPI(title="Vulnora AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    path: str
    model: str = "llama3.1:8b"

@app.get("/")
def read_root():
    return {"message": "Vulnora AI API is running"}

@app.post("/scan", response_model=ScanResult)
def scan_project(request: ScanRequest):
    logger.info(f"Received scan request for project: {request.path} with model: {request.model}")
    if not os.path.exists(request.path) or not os.path.isdir(request.path):
        logger.error(f"Invalid project path: {request.path}")
        raise HTTPException(status_code=400, detail="Invalid project path")

    start_time = time.time()
    
    try:
        scanner = ProjectScanner(project_path=request.path, llm_model=request.model)
        issues = scanner.scan()
        
        # Calculate smell score (weighted risk score)
        weights = {
            "Critical": 10,
            "High": 5,
            "Medium": 2,
            "Low": 1
        }
        smell_score = sum(weights.get(issue.severity, 1) for issue in issues)
        total_files = len(scanner.files_to_scan)
        
        duration = time.time() - start_time
        
        logger.info(f"Scan completed in {duration:.2f}s. Found {len(issues)} issues. Smell Score: {smell_score:.2f}")
        
        return ScanResult(
            project_path=request.path,
            issues=issues,
            smell_score=round(smell_score, 2),
            scan_duration=round(duration, 2),
            files_scanned=total_files
        )
        
    except Exception as e:
        logger.exception(f"Scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
