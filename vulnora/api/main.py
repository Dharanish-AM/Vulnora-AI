from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import os
import time
from vulnora.core.scanner import ProjectScanner
from vulnora.models.issue import ScanResult

app = FastAPI(title="Vulnora AI API", version="1.0.0")

class ScanRequest(BaseModel):
    path: str
    model: str = "llama3.1:8b"

@app.get("/")
def read_root():
    return {"message": "Vulnora AI API is running"}

@app.post("/scan", response_model=ScanResult)
def scan_project(request: ScanRequest):
    if not os.path.exists(request.path) or not os.path.isdir(request.path):
        raise HTTPException(status_code=400, detail="Invalid project path")

    start_time = time.time()
    
    try:
        scanner = ProjectScanner(project_path=request.path, llm_model=request.model)
        issues = scanner.scan()
        
        # Calculate smell score (simple heuristic: issues per file)
        # In a real app, this would be more complex
        total_files = len(scanner.files_to_scan)
        smell_score = (len(issues) / total_files) * 10 if total_files > 0 else 0.0
        
        duration = time.time() - start_time
        
        return ScanResult(
            project_path=request.path,
            issues=issues,
            smell_score=round(smell_score, 2),
            scan_duration=round(duration, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
