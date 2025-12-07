#!/usr/bin/env python3
"""
Flatten SciCode benchmark dataset from problem-level to sub-step-level format.

This script transforms problems_all.jsonl (80 problems with multiple sub-steps)
into scicode_flat.jsonl (341 individual sub-step records).

Each output record contains a self-contained prompt combining:
- Problem description and formulas
- I/O specifications
- Sub-step-specific instructions
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def construct_prompt_text(
    problem_description: str,
    problem_io: str,
    step_description: str
) -> str:
    """
    Construct a self-contained prompt by concatenating problem context with step instructions.

    Args:
        problem_description: Main problem description with formulas
        problem_io: Function I/O specification
        step_description: Specific sub-step task description

    Returns:
        Concatenated prompt text with double newlines between sections
    """
    parts = [
        problem_description.strip(),
        problem_io.strip(),
        step_description.strip()
    ]
    return "\n\n".join(parts)


def flatten_problem(problem: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Flatten a single problem into multiple sub-step records.

    Args:
        problem: Problem JSON object from problems_all.jsonl

    Returns:
        List of flattened sub-step records
    """
    # Extract problem-level fields with defaults for missing values
    problem_id = (problem.get("problem_id") or "").strip()
    problem_name = (problem.get("problem_name") or "").strip()
    problem_description_main = (problem.get("problem_description_main") or "").strip()
    problem_io = (problem.get("problem_io") or "").strip()
    required_dependencies = (problem.get("required_dependencies") or "").strip()
    general_tests = problem.get("general_tests", [])
    sub_steps = problem.get("sub_steps", [])

    flattened_records = []

    for sub_step in sub_steps:
        # Extract sub-step-level fields
        step_number = (sub_step.get("step_number") or "").strip()
        step_description_prompt = (sub_step.get("step_description_prompt") or "").strip()
        function_header = (sub_step.get("function_header") or "").strip()
        test_cases = sub_step.get("test_cases", [])
        return_line = (sub_step.get("return_line") or "").strip()

        # Construct the self-contained prompt
        prompt_text = construct_prompt_text(
            problem_description_main,
            problem_io,
            step_description_prompt
        )

        # Create flattened record
        record = {
            "benchmark_name": "SciCode",
            "problem_id": problem_id,
            "problem_name": problem_name,
            "step_number": step_number,
            "prompt_text": prompt_text,
            "function_header": function_header,
            "test_cases": test_cases,
            "general_tests": general_tests,
            "required_dependencies": required_dependencies,
            "return_line": return_line
        }

        flattened_records.append(record)

    return flattened_records


def main():
    """
    Main function to flatten the SciCode dataset.
    """
    # Define file paths
    input_file = Path("problems_all.jsonl")
    output_file = Path("scicode_flat.jsonl")

    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        print("Please ensure problems_all.jsonl is in the current directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading from: {input_file}")
    print(f"Writing to: {output_file}")
    print("-" * 60)

    total_problems = 0
    total_substeps = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:

            for line_num, line in enumerate(infile, 1):
                try:
                    # Parse problem JSON
                    problem = json.loads(line)
                    total_problems += 1

                    # Flatten problem into sub-step records
                    flattened_records = flatten_problem(problem)
                    total_substeps += len(flattened_records)

                    # Write each flattened record as one line
                    for record in flattened_records:
                        json.dump(record, outfile, ensure_ascii=False)
                        outfile.write('\n')

                    # Progress update
                    if total_problems % 10 == 0:
                        print(f"Processed {total_problems} problems, "
                              f"{total_substeps} sub-steps...")

                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse line {line_num}: {e}",
                          file=sys.stderr)
                    continue
                except Exception as e:
                    print(f"Warning: Error processing line {line_num}: {e}",
                          file=sys.stderr)
                    continue

    except IOError as e:
        print(f"Error: Failed to read/write files: {e}", file=sys.stderr)
        sys.exit(1)

    # Print summary
    print("-" * 60)
    print(f"✓ Successfully flattened {total_problems} problems")
    print(f"✓ Generated {total_substeps} sub-step records")
    print(f"✓ Output written to: {output_file}")

    # Verify output
    if output_file.exists():
        output_size = output_file.stat().st_size / 1024 / 1024  # MB
        print(f"✓ Output file size: {output_size:.2f} MB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
