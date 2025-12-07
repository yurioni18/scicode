# SciCode Dataset Flattening Script

## Overview

`flatten_scicode.py` transforms the SciCode benchmark from **problem-level** format to **sub-step-level** format, making each record self-contained for evaluation.

**Transformation:**
- **Input:** `problems_all.jsonl` - 80 problems with multiple sub-steps each
- **Output:** `scicode_flat.jsonl` - 341 individual sub-step records

## How to Run

### Basic Usage

```bash
# Navigate to the directory containing problems_all.jsonl
cd /home/user/scicode

# Run the script
python3 flatten_scicode.py
```

### Expected Output

```
Reading from: problems_all.jsonl
Writing to: scicode_flat.jsonl
------------------------------------------------------------
Processed 10 problems, 69 sub-steps...
Processed 20 problems, 84 sub-steps...
...
Processed 80 problems, 341 sub-steps...
------------------------------------------------------------
✓ Successfully flattened 80 problems
✓ Generated 341 sub-step records
✓ Output written to: scicode_flat.jsonl
✓ Output file size: 1.65 MB
```

### Make Script Executable (Optional)

```bash
chmod +x flatten_scicode.py
./flatten_scicode.py
```

## Output Format

Each line in `scicode_flat.jsonl` contains one JSON record with these fields:

```json
{
  "benchmark_name": "SciCode",
  "problem_id": "10",
  "problem_name": "ewald_summation",
  "step_number": "10.1",
  "prompt_text": "[self-contained instruction combining problem context + I/O spec + step task]",
  "function_header": "def get_alpha(recvec, alpha_scaling=5):\n    '''...",
  "test_cases": ["test code string 1", "test code string 2", ...],
  "general_tests": ["end-to-end test 1", "end-to-end test 2", ...],
  "required_dependencies": "import numpy as np\nfrom scipy.special import erfc",
  "return_line": "return alpha"
}
```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `benchmark_name` | Always "SciCode" |
| `problem_id` | Numeric problem identifier (e.g., "10") |
| `problem_name` | Problem name (e.g., "ewald_summation") |
| `step_number` | Sub-step identifier (e.g., "10.1") |
| `prompt_text` | Self-contained instruction combining:<br>• Problem description with formulas<br>• I/O specifications<br>• Sub-step-specific task |
| `function_header` | Function signature with docstring for this sub-step |
| `test_cases` | Array of unit test strings for this sub-step |
| `general_tests` | Array of end-to-end test strings (from problem-level) |
| `required_dependencies` | Import statements needed |
| `return_line` | Expected return statement |

## Reading the Output

### Python Example

```python
import json

# Read all flattened records
records = []
with open('scicode_flat.jsonl', 'r') as f:
    for line in f:
        record = json.loads(line)
        records.append(record)

print(f"Total sub-steps: {len(records)}")

# Access first record
first = records[0]
print(f"Problem: {first['problem_name']}")
print(f"Step: {first['step_number']}")
print(f"Prompt length: {len(first['prompt_text'])} chars")
```

### Command Line Examples

```bash
# Count total records
wc -l scicode_flat.jsonl

# View first record (pretty-printed)
head -n 1 scicode_flat.jsonl | python3 -m json.tool

# Extract all problem IDs
cat scicode_flat.jsonl | jq -r '.problem_id' | sort -u

# Find all sub-steps for problem 10
cat scicode_flat.jsonl | jq -r 'select(.problem_id == "10") | .step_number'

# Count sub-steps per problem
cat scicode_flat.jsonl | jq -r '.problem_id' | sort | uniq -c
```

## Features

✅ **Robust error handling** - Gracefully handles missing fields
✅ **Progress reporting** - Shows status every 10 problems
✅ **Null-safe** - Handles None values in JSON fields
✅ **Memory efficient** - Streams line-by-line processing
✅ **UTF-8 support** - Preserves special characters and LaTeX formulas

## Troubleshooting

### Error: Input file 'problems_all.jsonl' not found

**Solution:** Run the script from the directory containing `problems_all.jsonl` or specify the full path.

### JSON Decode Errors

**Solution:** The script will skip malformed lines and continue processing, showing a warning message.

### Import Errors

**Solution:** The script uses only Python standard library modules (json, sys, pathlib, typing). No external dependencies required.

## Statistics

- **Total problems:** 80
- **Total sub-steps:** 341
- **Average sub-steps per problem:** 4.26
- **Output file size:** ~1.65 MB

## License

Same license as the original SciCode benchmark dataset.
