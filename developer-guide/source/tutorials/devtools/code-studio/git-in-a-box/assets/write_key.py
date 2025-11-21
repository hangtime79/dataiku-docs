import dataiku

client = dataiku.api_client()
auth_info = client.get_auth_info(with_secrets=True)

SSH_KEY = None
for secret in auth_info['secrets']:
    if secret['key'] == 'ssh_key':
        SSH_KEY = secret['value'] + '\\n'


print(len(SSH_KEY))
SSH_KEY = SSH_KEY.replace('\\n', '\n')
print(len(SSH_KEY))

import os

try:
    os.mkdir('/home/dataiku/.ssh/')
except:
    print('Directory already exists')


with open('/home/dataiku/.ssh/id_rsa', 'w') as f:
    f.write(SSH_KEY)

os.chmod('/home/dataiku/.ssh/id_rsa', 0o600)
print('Key written to /home/dataiku/.ssh/id_rsa')
