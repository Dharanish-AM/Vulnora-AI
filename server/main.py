import uvicorn
import argparse
import os
import sys

def start_api():
    """Start the FastAPI backend."""
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)


def main():
    parser = argparse.ArgumentParser(description="Vulnora AI - Security Scanner")
    parser.add_argument("mode", nargs='?', default="api", choices=["api", "scan"], help="Mode to run: api or scan (default: api)")
    parser.add_argument("--path", help="Path to project for CLI scan")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        start_api()
    elif args.mode == "scan":
        if not args.path:
            print("Error: --path is required for scan mode")
            sys.exit(1)
        
        from app.core.scanner import ProjectScanner
        print(f"Scanning {args.path}...")
        
        try:
            scanner = ProjectScanner(project_path=args.path)
            issues = scanner.scan()
            
            print(f"\nScan complete. Found {len(issues)} issues.")
            for issue in issues:
                print(f"[{issue.severity}] {issue.rule_id}: {issue.description} - {issue.file_path}:{issue.line_number}")
                
        except Exception as e:
            print(f"Error during scan: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
