import paramiko
from scp import SCPClient
from tgtgClass import tgtgTesting
import os
import sys
from datetime import datetime



def startUPSSH(key_path, hostname, username="azureuser"):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key    
        )
        
        stdin, stdout, stderr = ssh.exec_command("sudo apt update && sudo apt install -y python3-requests python3-flask python3-venv")
        scp = SCPClient(ssh.get_transport())
        ssh.exec_command("rm -rf creatingCommandsOffsite.py")
        ssh.exec_command("rm -rf tgtgClass.py")
        ssh.exec_command("rm -rf commands.txt")
        if os.path.exists("creatingCommandsOffsite.py"):
            scp.put("creatingCommandsOffsite.py")
        elif os.path.exists("src/creatingCommandsOffsite.py"):
            scp.put("src/creatingCommandsOffsite.py")
        else:
            print("creatingCommandsOffsite.py not found")
            sys.exit(1)
        
        if os.path.exists("tgtgClass.py"):
            scp.put("tgtgClass.py")
        elif os.path.exists("src/tgtgClass.py"):
            scp.put("src/tgtgClass.py")
        else:
            print("tgtgClass.py not found")
            sys.exit(1)
        scp.close()
        print(stdout.read().decode())
        print(stderr.read().decode())
        ssh.close()
    except Exception as e:
        print(f"Failed to install tgtg: {e}")
        return False

    

def ssh_to_azure(key_path, hostname, username="azureuser"):
    try:
        # Initialize SSH client
        ssh = paramiko.SSHClient()
        # Automatically add host keys
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Get the private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        
        # Connect to the Azure VM
        print(f"Connecting to {hostname}...")
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key
        )
        print("Successfully connected to Azure VM!")
        
        scp = SCPClient(ssh.get_transport())
        
        # Clean up old files if they exist
        ssh.exec_command("rm -rf tgtgClass.py")
        ssh.exec_command("rm -rf commands.txt")
        ssh.exec_command("rm -rf myenv")
        
        # Upload tgtgClass.py
        if os.path.exists("tgtgClass.py"):
            scp.put("tgtgClass.py")
        elif os.path.exists("src/tgtgClass.py"):
            scp.put("src/tgtgClass.py")
        else:
            print("tgtgClass.py not found")
            sys.exit(1)
        
        # Upload commands.txt
        if os.path.exists("commands.txt"):
            scp.put("commands.txt")
        elif os.path.exists("src/commands.txt"):
            scp.put("src/commands.txt")
        else:
            print("commands.txt not found")
            sys.exit(1)
        
        # Set up Python virtual environment
        stdin, stdout, stderr = ssh.exec_command("python3 -m venv myenv")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Install required packages
        stdin, stdout, stderr = ssh.exec_command("myenv/bin/pip install tgtg requests")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Run the script
        command = "cat commands.txt | myenv/bin/python tgtgClass.py"
        ssh.exec_command(command)
        
        scp.close()
        
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as ssh_exception:
        print(f"SSH exception occurred: {ssh_exception}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ssh' in locals():
            ssh.close()
            print("SSH connection closed.")

# Your EC2 details
if os.path.exists("TGTG_key.pem"):

    KEY_PATH = "TGTG_key.pem"
elif os.path.exists("src/TGTG_key.pem"):
    KEY_PATH = "src/TGTG_key.pem"
else:
    print("TGTG_key.pem not found")
    sys.exit(1)
HOSTNAME = "20.84.48.177"
USERNAME = "azureuser"
startUPSSH(KEY_PATH, HOSTNAME, USERNAME)
#ssh_to_azure(KEY_PATH, HOSTNAME, USERNAME)
