import os
import random
import subprocess
import string

def git_commit(message, files):
    # Suppress output to keep terminal clean
    subprocess.run(["git", "add"] + files, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", message], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ensure_project_structure():
    dirs = ["src", "tests"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    files = {
        "src/calculator.py": "class Calculator:\n    def __init__(self):\n        self.value = 0\n",
        "src/utils.py": "import random\n\ndef get_random_number():\n    return random.randint(1, 100)\n",
        "tests/test_calculator.py": "import unittest\nfrom src.calculator import Calculator\n\nclass TestCalculator(unittest.TestCase):\n    def test_init(self):\n        calc = Calculator()\n        self.assertEqual(calc.value, 0)\n"
    }
    
    for filepath, content in files.items():
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(content)
    
    return list(files.keys())

def generate_random_code():
    actions = ["function", "comment", "variable"]
    action = random.choice(actions)
    
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    if action == "function":
        return f"\n\ndef dummy_func_{suffix}():\n    # This is a random function {suffix}\n    pass\n"
    elif action == "comment":
        return f"\n# Random comment update {suffix} to simulate activity\n"
    elif action == "variable":
        val = random.randint(1, 1000)
        return f"\nrandom_var_{suffix} = {val}\n"

def main():
    print("Initializing dummy project...")
    project_files = ensure_project_structure()
    
    # Initial commit for the structure if not already tracked
    try:
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", "Initialize dummy project structure"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass

    print("Starting 1000 code edit commits...")
    for i in range(1, 1001):
        target_file = random.choice(project_files)
        
        with open(target_file, "a") as f:
            f.write(generate_random_code())
        
        message = f"Refactor {os.path.basename(target_file)}: implemented feature #{i}"
        
        if i % 100 == 0:
            print(f"Progress: {i}/1000 commits created.")

        try:
            git_commit(message, [target_file])
        except subprocess.CalledProcessError as e:
            print(f"Error creating commit {i}: {e}")
            break
    
    print("Finished creating 1000 code edit commits.")

if __name__ == "__main__":
    main()
