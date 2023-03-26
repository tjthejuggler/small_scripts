import subprocess
import time

# Change this to your phone's device ID
PHONE_DEVICE_ID = 'a34cfc72571bdba9'

def is_device_connected(device_id):
    result = subprocess.run(['kdeconnect-cli', '-a', device_id], capture_output=True, text=True)
    return 'is connected' in result.stdout

def refresh_connection():
    #do this 3 times
    for i in range(5):
        subprocess.run(['kdeconnect-cli', '--refresh'])
        time.sleep(1)


def main():
    while True:
        if not is_device_connected(PHONE_DEVICE_ID):
            refresh_connection()
            print('Refreshing connection...')
        time.sleep(60)  # Check the connection every 60 seconds

if __name__ == '__main__':
    main()