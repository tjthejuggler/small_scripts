import subprocess
import time

# Change this to your phones' device IDs
PHONE_DEVICE_IDS = ['a34cfc72571bdba9', '5cc14f5b_6e5e_4ef5_ac30_741569a43709']

def is_device_connected(device_id):
    result = subprocess.run(['kdeconnect-cli', '-a', device_id], capture_output=True, text=True)
    return 'is connected' in result.stdout

def refresh_connection():
    # do this 3 times
    for i in range(5):
        subprocess.run(['kdeconnect-cli', '--refresh'])
        time.sleep(1)

def main():
    while True:
        for device_id in PHONE_DEVICE_IDS:
            if not is_device_connected(device_id):
                refresh_connection()
                print(f'Refreshing connection for device {device_id}...')
        time.sleep(60)  # Check the connection every 60 seconds

if __name__ == '__main__':
    main()
