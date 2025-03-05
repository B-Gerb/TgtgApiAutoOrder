import paramiko
from scp import SCPClient
from tgtgClass import tgtgTesting
import os
import sys
from datetime import datetime



def startUPSSH(key_path, hostname, username="ubuntu"):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(key_path)


        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key
        )



        stdin, stdout, stderr = ssh.exec_command("sudo apt install python3-requests")

        print(stdout.read().decode())
        print(stderr.read().decode()) 
        ssh.close()

    except:
        print("Failed to install tgtg")
        return False

    

def ssh_to_ec2(key_path, hostname, username="ubuntu"):
    try:
        # Initialize SSH client
        ssh = paramiko.SSHClient()
        
        # Automatically add host keys
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Get the private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        
        # Connect to the EC2 instance
        print(f"Connecting to {hostname}...")
        ssh.connect(
            hostname=hostname,
            username=username,
            pkey=private_key
        )
        print("Successfully connected to EC2 instance!")
        scp = SCPClient(ssh.get_transport())
        ssh.exec_command("rm -rf tgtgClass.py")
        ssh.exec_command("rm -rf commands.txt")
        ssh.exec_command("rm -rf myenv")
        if os.path.exists("tgtgClass.py"):
            scp.put("tgtgClass.py")
        elif os.path.exists("src/tgtgClass.py"):
            scp.put("src/tgtgClass.py")
        else:
            print("tgtgClass.py not found")
            sys.exit(1)
        if os.path.exists("commands.txt"):
            scp.put("commands.txt")
        elif os.path.exists("src/commands.txt"):
            scp.put("src/commands.txt")
        else:
            print("commands.txt not found")
            sys.exit(1)

        stdin, stdout, stderr = ssh.exec_command("python3 -m venv myenv")
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin, stdout, stderr = ssh.exec_command("myenv/bin/pip install tgtg requests")
        print(stdout.read().decode())
        print(stderr.read().decode())


        command = "cat commands.txt | myenv/bin/python tgtgClass.py"
        ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
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
if os.path.exists("KeyForTesting.pem"):

    KEY_PATH = "KeyForTesting.pem"
elif os.path.exists("src/KeyForTesting.pem"):
    KEY_PATH = "src/KeyForTesting.pem"
else:
    print("KeyForTesting.pem not found")
    sys.exit(1)
HOSTNAME = "ec2-54-236-130-174.compute-1.amazonaws.com"
USERNAME = "ubuntu"

#startUPSSH(KEY_PATH, HOSTNAME, USERNAME)
ssh_to_ec2(KEY_PATH, HOSTNAME, USERNAME)