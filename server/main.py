import uvicorn
import argparse
import os
import sys

def start_api():
    """Start the FastAPI backend."""
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)


def main():
    parser = argparse.ArgumentParser(
        description="Vulnora AI - Security Scanner v2.0 (Hybrid & Incremental)"
    )
    parser.add_argument(
        "mode", 
        nargs='?', 
        default="api", 
        choices=["api", "scan"], 
        help="Mode to run: api or scan (default: api)"
    )
    parser.add_argument("--path", help="Path to project for CLI scan")
    parser.add_argument("--model", default="llama3.1:8b", help="LLM model to use")
    parser.add_argument("--hybrid", action="store_true", default=True, help="Use hybrid scanning (default)")
    parser.add_argument("--legacy", action="store_true", help="Use legacy full LLM scanning")
    parser.add_argument("--incremental", action="store_true", help="Enable incremental scanning")
    parser.add_argument("--force", action="store_true", help="Force full scan (ignore cache)")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        print("🚀 Starting Vulnora AI API Server v2.0...")
        print("📡 Hybrid scanning: Enabled")
        print("⚡ Incremental scanning: Available via API")
        print("🌐 Server will be available at: http://localhost:8000")
        start_api()
    elif args.mode == "scan":
        if not args.path:
            print("❌ Error: --path is required for scan mode")
            sys.exit(1)
        
        print(f"🔍 Scanning {args.path}...")
        print(f"🤖 Using model: {args.model}")
        
        try:
            # Choose scanner type
            if args.legacy:
                from app.core.scanner import ProjectScanner
                print("📊 Mode: Legacy (Full LLM)")
                scanner = ProjectScanner(project_path=args.path, llm_model=args.model)
                issues = scanner.scan()
            elif args.incremental:
                from app.core.hybrid_scanner import HybridScanner
                from app.core.incremental_scanner import IncrementalScanner
                print("📊 Mode: Hybrid + Incremental")
                scanner = HybridScanner(project_path=args.path, llm_model=args.model)
                incremental = IncrementalScanner(project_path=args.path)
                issues = incremental.scan_incremental(scanner, force_full_scan=args.force)
            else:
                from app.core.hybrid_scanner import HybridScanner
                print("📊 Mode: Hybrid (Static + LLM)")
                scanner = HybridScanner(project_path=args.path, llm_model=args.model)
                issues = scanner.scan()
            
            print(f"\n✅ Scan complete. Found {len(issues)} issues.\n")
            
            # Display results
            if issues:
                severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
                sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.severity, 4))
                
                for issue in sorted_issues:
                    severity_emoji = {
                        "Critical": "🔴",
                        "High": "🟠",
                        "Medium": "🟡",
                        "Low": "🔵"
                    }.get(issue.severity, "⚪")
                    
                    print(f"{severity_emoji} [{issue.severity}] {issue.rule_id}: {issue.vulnerability_type}")
                    print(f"   📁 {issue.file_path}:{issue.line_number}")
                    print(f"   📝 {issue.description}")
                    print()
            else:
                print("🎉 No vulnerabilities found! Your code looks secure.")
                
        except Exception as e:
            print(f"❌ Error during scan: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()
