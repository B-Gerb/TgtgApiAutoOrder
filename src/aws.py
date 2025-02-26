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
        scp.put("tgtgClass.py")
        scp.put("commands.txt")
        stdin, stdout, stderr = ssh.exec_command("python3 -m venv myenv")
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin, stdout, stderr = ssh.exec_command("myenv/bin/pip install tgtg requests")
        print(stdout.read().decode())
        print(stderr.read().decode())


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
KEY_PATH = "KeyForTesting.pem"
HOSTNAME = "ec2-54-236-130-174.compute-1.amazonaws.com"
USERNAME = "ubuntu"

#startUPSSH(KEY_PATH, HOSTNAME, USERNAME)
ssh_to_ec2(KEY_PATH, HOSTNAME, USERNAME)