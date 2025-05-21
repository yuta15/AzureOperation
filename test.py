from azure.mgmt.storage import StorageManagementClient


client = StorageManagementClient()
client.storage_accounts.begin_create
