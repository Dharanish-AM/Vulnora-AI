import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("app.core.database")

class Database:
    def __init__(self, db_path: str = "vulnora.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize the database schema."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Scans table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        project_path TEXT NOT NULL,
                        smell_score REAL,
                        duration REAL,
                        files_scanned INTEGER
                    )
                """)
                
                # Issues table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS issues (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scan_id INTEGER NOT NULL,
                        file_path TEXT NOT NULL,
                        line_number INTEGER,
                        severity TEXT,
                        vulnerability_type TEXT,
                        description TEXT,
                        snippet TEXT,
                        suggested_fix TEXT,
                        FOREIGN KEY (scan_id) REFERENCES scans (id)
                    )
                """)
                
                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def save_scan(self, project_path: str, scan_data: Dict[str, Any]) -> int:
        """Save a scan result and return the scan ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Insert scan record
                cursor.execute("""
                    INSERT INTO scans (timestamp, project_path, smell_score, duration, files_scanned)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    project_path,
                    scan_data.get("smell_score", 0),
                    scan_data.get("scan_duration", 0),
                    scan_data.get("files_scanned", 0)
                ))
                
                scan_id = cursor.lastrowid
                
                # Insert issues
                issues = scan_data.get("issues", [])
                for issue in issues:
                    # Handle both dict and object (if pydantic model)
                    if not isinstance(issue, dict):
                        issue = issue.dict()
                        
                    cursor.execute("""
                        INSERT INTO issues (
                            scan_id, file_path, line_number, severity, 
                            vulnerability_type, description, snippet, suggested_fix
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        scan_id,
                        issue.get("file_path", ""),
                        issue.get("line_number", 0),
                        issue.get("severity", "Medium"),
                        issue.get("vulnerability_type", "Unknown"),
                        issue.get("description", ""),
                        issue.get("snippet", ""),
                        issue.get("suggested_fix", "")
                    ))
                
                conn.commit()
                logger.info(f"Saved scan {scan_id} with {len(issues)} issues")
                return scan_id
        except Exception as e:
            logger.error(f"Failed to save scan: {e}")
            return -1

    def get_all_scans(self) -> List[Dict[str, Any]]:
        """Retrieve all scan history summaries."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM scans ORDER BY id DESC")
                rows = cursor.fetchall()
                scans = []
                for row in rows:
                    data = dict(row)
                    if 'duration' in data:
                        data['scan_duration'] = data.pop('duration')
                    scans.append(data)
                return scans
        except Exception as e:
            logger.error(f"Failed to fetch scans: {e}")
            return []

    def get_scan_details(self, scan_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve full details for a specific scan."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get scan info
                cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
                scan_row = cursor.fetchone()
                
                if not scan_row:
                    return None
                
                scan_data = dict(scan_row)
                if 'duration' in scan_data:
                    scan_data['scan_duration'] = scan_data.pop('duration')
                
                # Get issues
                cursor.execute("SELECT * FROM issues WHERE scan_id = ?", (scan_id,))
                issue_rows = cursor.fetchall()
                
                scan_data["issues"] = [dict(row) for row in issue_rows]
                
                return scan_data
        except Exception as e:
            logger.error(f"Failed to fetch scan details: {e}")
            return None
