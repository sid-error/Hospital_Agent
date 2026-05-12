import json
import os
from google.adk.evaluation.eval_set import EvalSet
from pydantic import ValidationError

def debug_eval_json(file_path):
    print(f"--- Debugging {file_path} ---")
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        try:
            content = f.read()
            # ADK EvalSet uses camelCase by default in its alias generator
            # model_validate_json handles the alias mapping automatically
            eval_set = EvalSet.model_validate_json(content)
            print("Successfully validated EvalSet JSON!")
            print(f"Eval Set ID: {eval_set.eval_set_id}")
            print(f"Number of Cases: {len(eval_set.eval_cases)}")
            for case in eval_set.eval_cases:
                print(f" - Case: {case.eval_id}")
        except json.JSONDecodeError as e:
            print(f"JSON Syntax Error: {e}")
        except ValidationError as e:
            print("Validation Error (Schema mismatch):")
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    debug_eval_json("eval/test.json")
