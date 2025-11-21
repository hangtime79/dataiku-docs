import dataiku

client = dataiku.api_client()
user_list = []
dss_users = client.list_users()
for user in dss_users:
    if user.get("activeWebSocketSesssions",None):
        user_list.append(user["displayName"])
print(user_list)