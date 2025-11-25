import os
import subprocess

def vulnerable_function():
    user_input = input("Enter command: ")
    # VULNERABLE: Command injection
    os.system("ls " + user_input)
    
    # VULNERABLE: Hardcoded secret
    api_key = "1234567890123456789012345"
    
    # VULNERABLE: Taint flow
    cmd = "echo " + user_input
    subprocess.Popen(cmd, shell=True)

if __name__ == "__main__":
    vulnerable_function()
