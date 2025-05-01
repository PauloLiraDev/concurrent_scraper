# For local tests only
import os
import sys
import subprocess

def run_command(command):
    """Execute a command and return its exit code."""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True)
    return result.returncode

def main():
    """Run all tests and checks before pushing to git."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    commands = [
        # Formatação e lint
        "black src/ --check",
        "ruff check src/",
        
        # Testes unitários
        "python -m pytest src/tests/test_unit.py -v",
        
        # Testes de integração (usando mock)
        "python -m pytest src/tests/test_integration.py -v",
    ]
    
    # Executa cada comando
    failed = False
    for cmd in commands:
        exit_code = run_command(cmd)
        if exit_code != 0:
            print(f"❌ Command failed: {cmd}")
            failed = True
        else:
            print(f"✅ Command passed: {cmd}")
    
    # Verifica se algum comando falhou
    if failed:
        print("❌ Some tests or checks failed. Please fix the issues before pushing.")
        sys.exit(1)
    else:
        print("✅ All tests and checks passed. Ready to push!")
        sys.exit(0)

if __name__ == "__main__":
    main()