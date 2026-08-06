import json
import os

def identify_json_defect():
    target_file = "existenzCoreMaster.json"
    
    if not os.path.exists(target_file):
        print(f"[-] Defect: Cannot locate '{target_file}' in this directory.")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        raw_payload = f.read()

    try:
        data = json.loads(raw_payload)
        print("[+] Success! Your master JSON structure is 100% syntactically perfect.")
    except json.JSONDecodeError as e:
        print("\n" + "="*50)
        print("💥 CRITICAL JSON SYNTAX ERROR LOCATED!")
        print(f"   Reason:      {e.msg}")
        print(f"   Line Number: {e.lineno}")
        print(f"   Column:      {e.colno}")
        print(f"   Character:   {e.pos}")
        print("="*50)
        
        # Pull the exact broken lines so you can view them without layout alignment biases
        lines = raw_payload.splitlines()
        start = max(0, e.lineno - 3)
        end = min(len(lines), e.lineno + 3)
        
        print("\n--- EXACT RAW CODE VISUALIZER ---")
        for i in range(start, end):
            current_line = i + 1
            marker = ">>> " if current_line == e.lineno else "    "
            print(f"{marker}Line {current_line:03d}: {lines[i]}")
        print("----------------------------------\n")

if __name__ == "__main__":
    identify_json_defect()
