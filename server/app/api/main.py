from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import time
import logging
from app.core.scanner import ProjectScanner
from app.core.hybrid_scanner import HybridScanner
from app.core.incremental_scanner import IncrementalScanner
from app.models.issue import ScanResult
from app.core.database import Database
from app.core.reporter import PDFReporter
from fastapi.responses import FileResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app.api")

app = FastAPI(title="Vulnora AI API", version="1.0.0")
db = Database()
reporter = PDFReporter()

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
    use_hybrid: bool = True  # Use hybrid scanning by default
    use_incremental: bool = False  # Incremental scanning opt-in
    force_full_scan: bool = False  # Force full scan even with incremental

@app.get("/")
def read_root():
    return {
        "message": "Vulnora AI API is running",
        "version": "2.0.0",
        "features": {
            "hybrid_scanning": True,
            "incremental_scanning": True,
            "static_analysis": True
        }
    }

@app.post("/scan", response_model=ScanResult)
def scan_project(request: ScanRequest):
    logger.info(f"🚀 Received scan request for project: {request.path}")
    logger.info(f"Using model: {request.model}")
    logger.info(f"Hybrid scanning: {request.use_hybrid}, Incremental: {request.use_incremental}")
    
    if not os.path.exists(request.path) or not os.path.isdir(request.path):
        logger.error(f"❌ Invalid project path: {request.path}")
        raise HTTPException(status_code=400, detail="Invalid project path")

    start_time = time.time()
    
    try:
        # Choose scanner based on request
        if request.use_hybrid:
            scanner = HybridScanner(project_path=request.path, llm_model=request.model)
        else:
            # Legacy scanner for compatibility
            scanner = ProjectScanner(project_path=request.path, llm_model=request.model)
        
        # Apply incremental scanning if requested
        if request.use_incremental:
            incremental = IncrementalScanner(project_path=request.path)
            issues = incremental.scan_incremental(
                scanner=scanner,
                force_full_scan=request.force_full_scan
            )
        else:
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
        
        logger.info(f"✅ Scan completed in {duration:.2f}s")
        logger.info(f"📊 Results: {len(issues)} issues found. Smell Score: {smell_score:.2f}")
        
        result = ScanResult(
            project_path=request.path,
            issues=issues,
            smell_score=round(smell_score, 2),
            scan_duration=round(duration, 2),
            files_scanned=total_files
        )
        
        # Save to database
        scan_id = db.save_scan(request.path, result.dict())
        result.scan_id = scan_id
        logger.info(f"💾 Saved scan result with ID: {scan_id}")
        
        return result
        
    except Exception as e:
        logger.exception(f"Scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.get("/history")
def get_history():
    """Get scan history."""
    return db.get_all_scans()

@app.get("/history/{scan_id}")
def get_scan_details(scan_id: int):
    """Get details of a specific scan."""
    scan = db.get_scan_details(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan

@app.get("/export/{scan_id}")
def export_report(scan_id: int):
    """Generate and download a PDF report for a scan."""
    scan = db.get_scan_details(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    try:
        report_path = reporter.generate_report(scan)
        return FileResponse(
            report_path, 
            media_type="application/pdf", 
            filename=os.path.basename(report_path)
        )
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report")
