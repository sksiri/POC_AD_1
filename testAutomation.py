import os
import subprocess
from config import UNC_BASE_PATH, FOLDER_NAME, PERMISSIONS_MAP

# Function to create a folder at the specified UNC path
# Returns the full folder path if successful, otherwise None
# Prints status messages for folder creation or existence

def create_unc_folder(base_path, folder_name):
    folder_path = os.path.join(base_path, folder_name)
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")
        return folder_path
    except Exception as e:
        print(f"Failed to create folder: {e}")
        return None

# Function to set NTFS permissions on a folder for a given AD group
# permission_type: 'FullControl' or 'ReadWrite' (maps to NTFS rights)
# Uses PowerShell to apply permissions
# Prints status messages for success or failure

def set_ntfs_permission(folder_path, ad_group, permission_type):
    # Map custom permission label to actual NTFS rights
    if permission_type == "FullControl":
        rights = "FullControl"
    elif permission_type == "ReadWrite":
        rights = "ReadAndExecute, Write"
    elif permission_type == "ReadOnly":
        rights = "ReadAndExecute"
    else:
        print(f"Unsupported permission: {permission_type} for group {ad_group}")
        return
    # PowerShell script to set the NTFS permission
    ps_script = f'''
    $path = "{folder_path}"
    $acl = Get-Acl $path
    $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("{ad_group}", "{rights}", "ContainerInherit,ObjectInherit", "None", "Allow")
    $acl.SetAccessRule($rule)
    Set-Acl -Path $path -AclObject $acl
    '''
    try:
        subprocess.run(["powershell", "-Command", ps_script], check=True)
        print(f"Permission '{permission_type}' applied to group: {ad_group}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set permissions for {ad_group}: {e}")

# Main function to create the folder and set permissions for each AD group
# permissions_map: dict of {ad_group: permission_type}

def main(base_path, folder_name, permissions_map):
    folder_path = create_unc_folder(base_path, folder_name)
    if folder_path:
        for group, perm in permissions_map.items():
            set_ntfs_permission(folder_path, group, perm)

# Entry point for script execution
# Defines UNC path, folder name, and AD group permissions
# Calls main() to perform folder creation and permission assignment

if __name__ == "__main__":
    main(UNC_BASE_PATH, FOLDER_NAME, PERMISSIONS_MAP)