import paramiko
from scp import SCPClient
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
        scp.put('tokens.txt')
        scp.put('tgtgClass.py')
        scp.close()

        stdin,stdout,stderr = ssh.exec_command('python3 -c "print(\'Hello, world!\')"')
        print(stdout.read().decode())   
        

        
    
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
HOSTNAME = "ec2-54-163-195-23.compute-1.amazonaws.com"
USERNAME = "ubuntu"
    
ssh_to_ec2(KEY_PATH, HOSTNAME, USERNAME)