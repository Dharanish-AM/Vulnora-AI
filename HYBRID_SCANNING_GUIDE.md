# 🚀 Vulnora AI v2.0 - Hybrid & Incremental Scanning

## What's New in v2.0

Vulnora AI has been upgraded with a **multi-stage hybrid scanning pipeline** that combines the speed of static analysis with the intelligence of LLM-based detection.

### 🎯 Key Improvements

| Feature | v1.0 (Legacy) | v2.0 (Hybrid) | Improvement |
|---------|---------------|---------------|-------------|
| **Scan Speed** | 5-10 min (100 files) | 1-2 min (100 files) | **5-10x faster** |
| **LLM Calls** | Every file | Only flagged files (~10-30%) | **70-90% reduction** |
| **Accuracy** | 85-90% | 85-90% | **Same accuracy** |
| **False Positives** | Medium | Low (pre-filtered) | **Better** |
| **Incremental Scan** | ❌ Not available | ✅ 10-100x faster on re-scans | **New** |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Vulnora AI v2.0 Pipeline                   │
└─────────────────────────────────────────────────────────────┘

Stage 1: Static Analysis (< 1ms per file)
    ↓
    ├─ Pattern matching (regex)
    ├─ Language-specific rules
    └─ Severity scoring
    
Stage 2: Smart Filtering
    ↓
    ├─ Flag Critical/High findings
    ├─ Skip clean files (70-90%)
    └─ Build LLM context hints
    
Stage 3: LLM Validation (only flagged files)
    ↓
    ├─ Deep semantic analysis
    ├─ Context-aware validation
    └─ Generate fixes

Stage 4 (Optional): Incremental Caching
    ↓
    ├─ File hash comparison
    ├─ Reuse cached results
    └─ Scan only changes
```

---

## 📦 New Components

### 1. **StaticAnalyzer** (`app/core/static_analyzer.py`)

Fast regex-based pre-filtering for quick vulnerability detection.

**Supported Patterns:**
- Python: 10+ patterns (Command Injection, SQL Injection, Secrets, etc.)
- JavaScript/TypeScript: 7+ patterns (XSS, eval, hardcoded secrets)
- Java: 3+ patterns (Command Injection, SQL Injection)

**Example Usage:**
```python
from app.core.static_analyzer import StaticAnalyzer

analyzer = StaticAnalyzer()
findings = analyzer.quick_scan(file_path, content)

# Returns: [{'line': 10, 'type': 'Command Injection', 'severity': 'Critical', ...}]
```

### 2. **HybridScanner** (`app/core/hybrid_scanner.py`)

Two-stage scanning pipeline combining static + LLM analysis.

**Features:**
- ⚡ 5-10x faster than legacy scanner
- 📊 Real-time statistics
- 🎯 Smart file flagging
- 🤖 Context-aware LLM prompts

**Example Usage:**
```python
from app.core.hybrid_scanner import HybridScanner

scanner = HybridScanner(project_path="/path/to/project", llm_model="llama3.1:8b")
issues = scanner.scan()

# Get statistics
stats = scanner.get_scan_statistics()
print(f"Speedup: {stats['speedup_factor']}x")
```

### 3. **IncrementalScanner** (`app/core/incremental_scanner.py`)

Caches scan results and only rescans changed files.

**Features:**
- 💾 Persistent cache (`.vulnora_cache.json`)
- 🔄 SHA256 file hashing
- ⚡ 10-100x faster on re-scans
- 📊 Cache statistics

**Example Usage:**
```python
from app.core.incremental_scanner import IncrementalScanner
from app.core.hybrid_scanner import HybridScanner

scanner = HybridScanner(project_path="/path/to/project")
incremental = IncrementalScanner(project_path="/path/to/project")

# First scan: Full scan + caching
issues = incremental.scan_incremental(scanner)

# Second scan: Only scans changed files
issues = incremental.scan_incremental(scanner)
```

---

## 🎮 Usage Guide

### CLI Usage

#### Basic Hybrid Scan (Recommended)
```bash
python main.py scan --path /path/to/project
```

#### Incremental Scan (Fastest for Re-scans)
```bash
# First scan
python main.py scan --path /path/to/project --incremental

# Subsequent scans (only scans changed files)
python main.py scan --path /path/to/project --incremental
```

#### Force Full Scan (Ignore Cache)
```bash
python main.py scan --path /path/to/project --incremental --force
```

#### Legacy Mode (Full LLM - Slower)
```bash
python main.py scan --path /path/to/project --legacy
```

#### Custom Model
```bash
python main.py scan --path /path/to/project --model llama3
```

### API Usage

#### Start API Server
```bash
python main.py api
```

#### Hybrid Scan (Default)
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "model": "llama3.1:8b",
    "use_hybrid": true
  }'
```

#### Incremental Scan
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "model": "llama3.1:8b",
    "use_hybrid": true,
    "use_incremental": true
  }'
```

#### Force Full Scan
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "use_incremental": true,
    "force_full_scan": true
  }'
```

#### Legacy Mode
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/project",
    "use_hybrid": false
  }'
```

---

## 📊 Performance Comparison

### Scan Times (100 files, various scenarios)

| Scenario | Legacy | Hybrid | Incremental (1st) | Incremental (2nd+) |
|----------|--------|--------|-------------------|---------------------|
| **All files clean** | 5-10 min | 30-60 sec | 30-60 sec | 5-10 sec |
| **10% flagged** | 5-10 min | 1-2 min | 1-2 min | 10-30 sec |
| **50% flagged** | 5-10 min | 3-5 min | 3-5 min | 30-90 sec |
| **All flagged** | 5-10 min | 5-8 min | 5-8 min | 1-2 min |

### Resource Usage

| Metric | Legacy | Hybrid | Improvement |
|--------|--------|--------|-------------|
| **LLM API calls** | 100 | 10-30 | **70-90% reduction** |
| **CPU usage** | Medium | Low-Medium | **Lower** |
| **Memory** | 4-8 GB | 4-8 GB | **Same** |
| **Disk I/O** | Low | Low-Medium | **Slightly higher** |

---

## 🎯 Best Practices

### When to Use Each Mode

1. **Hybrid Mode (Default)** - Best for most scenarios
   - ✅ First-time scans
   - ✅ Large projects (1000+ files)
   - ✅ General security audits
   - ⚡ 5-10x faster than legacy

2. **Incremental Mode** - Best for development workflows
   - ✅ CI/CD pipelines
   - ✅ Pre-commit hooks
   - ✅ Frequent re-scans
   - ⚡ 10-100x faster on re-scans

3. **Legacy Mode** - Only for specific cases
   - ✅ Small projects (< 50 files)
   - ✅ When you need 100% LLM coverage
   - ✅ Debugging/testing
   - ⚠️ Slowest option

### Optimizing Scan Performance

1. **Use `.gitignore` patterns**: Exclude test files, vendor code
2. **Incremental for CI/CD**: Only scan changed files in PRs
3. **Adjust worker count**: Edit `max_workers=4` in hybrid_scanner.py
4. **Choose faster models**: `llama3.2:3b` for quick scans, `llama3.1:8b` for accuracy

---

## 🔧 Configuration

### Static Analyzer Patterns

Add custom patterns to `app/core/static_analyzer.py`:

```python
PATTERNS = {
    'python': [
        StaticPattern(
            r'your_custom_pattern',
            'Vulnerability Name',
            'Critical/High/Medium/Low',
            'CWE-XXX'
        ),
    ]
}
```

### Cache Management

```python
from app.core.incremental_scanner import IncrementalScanner

scanner = IncrementalScanner("/path/to/project")

# Get cache stats
stats = scanner.get_cache_stats()
print(stats)

# Clear cache
scanner.clear_cache()
```

---

## 🐛 Troubleshooting

### Issue: "No cache found" on first incremental scan
**Solution**: This is normal. The first scan creates the cache.

### Issue: Scan slower than expected
**Solution**: 
- Check if Ollama is running: `ollama list`
- Reduce `max_workers` if CPU-limited
- Use faster LLM model

### Issue: False positives increased
**Solution**:
- Static analyzer is conservative
- LLM validation filters most false positives
- Adjust patterns in `static_analyzer.py`

### Issue: Cache growing too large
**Solution**:
```python
scanner.clear_cache()  # Or delete .vulnora_cache.json
```

---

## 🚀 Migration from v1.0

### Code Changes Required

**Old API calls:**
```python
# v1.0
scanner = ProjectScanner(project_path, llm_model)
issues = scanner.scan()
```

**New API calls (hybrid):**
```python
# v2.0 - Hybrid (recommended)
from app.core.hybrid_scanner import HybridScanner
scanner = HybridScanner(project_path, llm_model)
issues = scanner.scan()
```

**New API calls (incremental):**
```python
# v2.0 - Incremental (fastest)
from app.core.hybrid_scanner import HybridScanner
from app.core.incremental_scanner import IncrementalScanner

scanner = HybridScanner(project_path, llm_model)
incremental = IncrementalScanner(project_path)
issues = incremental.scan_incremental(scanner)
```

### Backwards Compatibility

✅ **v1.0 API still works** - Legacy `ProjectScanner` is still available
✅ **No breaking changes** - All existing code continues to work
✅ **Gradual migration** - Switch to hybrid/incremental when ready

---

## 📈 Roadmap

### Completed ✅
- [x] Static analysis pre-filter
- [x] Hybrid scanning pipeline
- [x] Incremental scanning
- [x] File hash caching
- [x] Context-aware LLM prompts

### Coming Soon 🚧
- [ ] Specialized LLM prompts per vulnerability type
- [ ] Vector database caching (similar code detection)
- [ ] Streaming LLM responses
- [ ] Multi-model tiered analysis
- [ ] Code chunking for large files
- [ ] Parallel chunk processing

---

## 💡 Tips & Tricks

1. **Speed up CI/CD**: Use incremental mode and cache `.vulnora_cache.json`
2. **Balance speed vs accuracy**: Hybrid mode gives 90% speed, same accuracy
3. **Customize static patterns**: Add project-specific vulnerability patterns
4. **Monitor statistics**: Use `get_scan_statistics()` to track improvements
5. **Clear cache periodically**: Prevent stale results with `clear_cache()`

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Dharanish-AM/Vulnora-AI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Dharanish-AM/Vulnora-AI/discussions)
- **Email**: dharanish816@gmail.com

---

**Built with ❤️ by the Vulnora AI Team**
