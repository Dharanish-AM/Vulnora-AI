#!/usr/bin/env python3
"""
Quick test script to verify Vulnora AI v2.0 hybrid scanning
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_static_analyzer():
    """Test static analyzer"""
    print("\n" + "="*60)
    print("🧪 Testing StaticAnalyzer...")
    print("="*60)
    
    from app.core.static_analyzer import StaticAnalyzer
    
    analyzer = StaticAnalyzer()
    
    # Test code with vulnerabilities
    test_code = """
import os
import subprocess

def vulnerable_function():
    user_input = input("Enter command: ")
    os.system("ls " + user_input)  # Command Injection
    
    api_key = "1234567890123456789012345"  # Hardcoded Secret
    
    cmd = "echo " + user_input
    subprocess.Popen(cmd, shell=True)  # Command Injection via Shell
"""
    
    findings = analyzer.quick_scan("test.py", test_code)
    
    print(f"✅ Found {len(findings)} static findings:")
    for finding in findings:
        print(f"   Line {finding['line']}: {finding['type']} ({finding['severity']})")
    
    assert len(findings) >= 2, "Should find at least 2 vulnerabilities"
    print("✅ StaticAnalyzer test passed!")
    return True


def test_hybrid_scanner():
    """Test hybrid scanner on test_project"""
    print("\n" + "="*60)
    print("🧪 Testing HybridScanner...")
    print("="*60)
    
    from app.core.hybrid_scanner import HybridScanner
    
    # Use the test_project directory
    test_project_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_project"
    )
    
    if not os.path.exists(test_project_path):
        print(f"⚠️  Test project not found at {test_project_path}")
        return False
    
    scanner = HybridScanner(
        project_path=test_project_path,
        llm_model="llama3.1:8b"
    )
    
    print(f"📂 Scanning: {test_project_path}")
    
    try:
        issues = scanner.scan()
        
        print(f"\n✅ Scan complete!")
        print(f"📊 Results:")
        print(f"   - Total files: {scanner.stats['total_files']}")
        print(f"   - Clean files: {scanner.stats['clean_files']}")
        print(f"   - Flagged files: {scanner.stats['flagged_files']}")
        print(f"   - Static findings: {scanner.stats['static_findings']}")
        print(f"   - LLM validated issues: {len(issues)}")
        
        stats = scanner.get_scan_statistics()
        print(f"   - Speedup factor: {stats['speedup_factor']}x")
        
        if issues:
            print(f"\n🔍 Issues found:")
            for issue in issues[:5]:  # Show first 5
                print(f"   - {issue.severity}: {issue.vulnerability_type} at line {issue.line_number}")
        
        print("\n✅ HybridScanner test passed!")
        return True
        
    except Exception as e:
        print(f"❌ HybridScanner test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_incremental_scanner():
    """Test incremental scanner"""
    print("\n" + "="*60)
    print("🧪 Testing IncrementalScanner...")
    print("="*60)
    
    from app.core.hybrid_scanner import HybridScanner
    from app.core.incremental_scanner import IncrementalScanner
    
    test_project_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_project"
    )
    
    if not os.path.exists(test_project_path):
        print(f"⚠️  Test project not found at {test_project_path}")
        return False
    
    scanner = HybridScanner(project_path=test_project_path)
    incremental = IncrementalScanner(project_path=test_project_path)
    
    # Clear cache for clean test
    incremental.clear_cache()
    
    print("📝 First scan (should create cache)...")
    issues1 = incremental.scan_incremental(scanner)
    
    stats1 = incremental.get_cache_stats()
    print(f"   - Cache created: {stats1['cache_exists']}")
    print(f"   - Cached files: {stats1['cached_files']}")
    print(f"   - Issues found: {len(issues1)}")
    
    print("\n📝 Second scan (should use cache)...")
    issues2 = incremental.scan_incremental(scanner)
    
    stats2 = incremental.get_cache_stats()
    print(f"   - Total scans: {stats2['total_scans']}")
    print(f"   - Issues found: {len(issues2)}")
    
    assert stats2['total_scans'] == 2, "Should have 2 scans recorded"
    assert len(issues1) == len(issues2), "Should have same number of issues"
    
    print("\n✅ IncrementalScanner test passed!")
    return True


def main():
    """Run all tests"""
    print("🚀 Vulnora AI v2.0 - Test Suite")
    print("="*60)
    
    results = []
    
    # Test 1: Static Analyzer
    try:
        results.append(("StaticAnalyzer", test_static_analyzer()))
    except Exception as e:
        print(f"❌ StaticAnalyzer test crashed: {e}")
        results.append(("StaticAnalyzer", False))
    
    # Test 2: Hybrid Scanner (requires Ollama)
    try:
        results.append(("HybridScanner", test_hybrid_scanner()))
    except Exception as e:
        print(f"❌ HybridScanner test crashed: {e}")
        results.append(("HybridScanner", False))
    
    # Test 3: Incremental Scanner
    try:
        results.append(("IncrementalScanner", test_incremental_scanner()))
    except Exception as e:
        print(f"❌ IncrementalScanner test crashed: {e}")
        results.append(("IncrementalScanner", False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📊 {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
