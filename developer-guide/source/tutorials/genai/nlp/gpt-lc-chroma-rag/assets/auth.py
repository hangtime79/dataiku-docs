import dataiku

def get_api_key(secret_name: str) -> str:
    
    client = dataiku.api_client()
    auth_info = client.get_auth_info(with_secrets=True)
    secret_value = None
    for secret in auth_info["secrets"]:
            if secret["key"] == secret_name:
                    secret_value = secret["value"]
                    break
    if not secret_value:
            raise Exception("Secret not found")
    else:
           return secret_value
