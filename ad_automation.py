import os
from ldap3 import Server, Connection, ALL, MODIFY_ADD

# Get credentials and AD info from environment variables
AD_SERVER = os.environ['AD_SERVER']
AD_USER = os.environ['AD_USER']
AD_PASSWORD = os.environ['AD_PASSWORD']
BASE_DN = os.environ['AD_BASE_DN']

# Group and user details
SECURITY_GROUP = "MySecurityGroup"
ADMIN_GROUP = "MyAdminGroup"
USER_CN = "TestUser"
USER_PASSWORD = "P@ssw0rd123!"

server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)

# Create Security Group
conn.add(f"CN={SECURITY_GROUP},{BASE_DN}", ['group'], {'sAMAccountName': SECURITY_GROUP, 'groupType': '-2147483646'})
# Create Admin Group
conn.add(f"CN={ADMIN_GROUP},{BASE_DN}", ['group'], {'sAMAccountName': ADMIN_GROUP, 'groupType': '-2147483646'})
# Create User
conn.add(f"CN={USER_CN},{BASE_DN}", ['user'], {
    'sAMAccountName': USER_CN,
    'userPrincipalName': f"{USER_CN}@yourdomain.com",
    'displayName': USER_CN,
    'userPassword': USER_PASSWORD
})
# Enable user account
conn.modify(f"CN={USER_CN},{BASE_DN}", {'userAccountControl': [(MODIFY_ADD, [512])]})
# Add user to Security Group
conn.modify(f"CN={SECURITY_GROUP},{BASE_DN}", {'member': [(MODIFY_ADD, [f"CN={USER_CN},{BASE_DN}"]) ]})

print("AD objects created and user added to group.")

conn.unbind()
