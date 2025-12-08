#!/usr/bin/env python3
"""
Script to flatten sci-code JSONL data into CSV format.
Each sub-step becomes a row with the problem information repeated.
"""
import json
import csv

def flatten_jsonl_to_csv(input_file, output_file):
    """
    Read JSONL file and flatten to CSV format.
    Each sub_step becomes a separate row.
    """
    rows = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                problem = json.loads(line)

                # Extract problem-level fields
                problem_name = problem.get('problem_name', '')
                problem_id = problem.get('problem_id', '')
                problem_description_main = problem.get('problem_description_main', '')
                problem_io = problem.get('problem_io', '')
                required_dependencies = problem.get('required_dependencies', '')

                # Process each sub_step
                sub_steps = problem.get('sub_steps', [])

                if not sub_steps:
                    # If no sub_steps, still add the problem as one row
                    rows.append({
                        'problem_id': problem_id,
                        'problem_name': problem_name,
                        'problem_description_main': problem_description_main,
                        'problem_io': problem_io,
                        'required_dependencies': required_dependencies,
                        'step_number': '',
                        'step_description_prompt': '',
                        'function_header': '',
                        'test_cases': '',
                        'return_line': ''
                    })
                else:
                    for sub_step in sub_steps:
                        # Convert test_cases list to JSON string for CSV
                        test_cases = sub_step.get('test_cases', [])
                        test_cases_str = json.dumps(test_cases) if test_cases else ''

                        rows.append({
                            'problem_id': problem_id,
                            'problem_name': problem_name,
                            'problem_description_main': problem_description_main,
                            'problem_io': problem_io,
                            'required_dependencies': required_dependencies,
                            'step_number': sub_step.get('step_number', ''),
                            'step_description_prompt': sub_step.get('step_description_prompt', ''),
                            'function_header': sub_step.get('function_header', ''),
                            'test_cases': test_cases_str,
                            'return_line': sub_step.get('return_line', '')
                        })

    # Write to CSV
    if rows:
        fieldnames = [
            'problem_id',
            'problem_name',
            'problem_description_main',
            'problem_io',
            'required_dependencies',
            'step_number',
            'step_description_prompt',
            'function_header',
            'test_cases',
            'return_line'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Successfully wrote {len(rows)} rows to {output_file}")
        return len(rows)
    else:
        print("No data to write")
        return 0

if __name__ == '__main__':
    input_file = 'problems_all.jsonl'
    output_file = 'scicode_flattened.csv'

    num_rows = flatten_jsonl_to_csv(input_file, output_file)
    print(f"Total rows: {num_rows}")
