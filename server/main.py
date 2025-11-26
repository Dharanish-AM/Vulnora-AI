import uvicorn
import argparse
import os
import sys

def start_api():
    """Start the FastAPI backend."""
    uvicorn.run("vulnora.api.main:app", host="0.0.0.0", port=8000, reload=True)


def main():
    parser = argparse.ArgumentParser(description="Vulnora AI - Security Scanner")
    parser.add_argument("mode", choices=["api", "scan"], help="Mode to run: api or scan")
    parser.add_argument("--path", help="Path to project for CLI scan")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        start_api()
    elif args.mode == "scan":
        if not args.path:
            print("Error: --path is required for scan mode")
            sys.exit(1)
        # TODO: Import and run scanner
        print(f"Scanning {args.path}...")

if __name__ == "__main__":
    main()
