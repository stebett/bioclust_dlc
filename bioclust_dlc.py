import os
import shutil
import subprocess
from pathlib import Path

jord_server = "jord.biologie.ens.fr"
bioclust_server = "bioclusts01.bioclust.biologie.ens.fr"



def main(script_directory):
    # List tasks and let the user select one
    task_path = list_tasks(script_directory)
    if not task_path:
        return

    # Input parameters
    user = input("Enter your username to connect to jord: ")
    local_project_path = Path(input("Enter the local path of the DLC project: ")).resolve()
    remote_path = Path(input("Enter the working directory on the remote: ")) # Do not resolve, it's remote!

    # Testing
    user = "bettani"
    local_project_path = Path("/mnt/d/ExperimentV2-StefanoBettani-2024-01-24").resolve()
    remote_path = Path("/kingdoms/nbc/workspace29/bettani/dlc-projects")

    print("\n-----------------------\n")

    # Copy project to remote
    print("[*] Copying dlc project to remote")
    remote_project_path = copy_project_to_remote(user, local_project_path, remote_path)

    # Modify DLC project path in config file
    print("[*] Updating remote project path")
    modify_dlc_project_path(user, local_project_path, remote_project_path)

    print("[*] Copying task files")
    remote_task_path = upload_task(user, script_directory, remote_project_path, task_path)

    print("[*] Updating task files")
    modify_task_project_path(user, script_directory, remote_project_path, task_path, remote_task_path)

    # Submit task to bioclust
    print(f"[*] Granting permission to the script file")
    grant_permissions(user, jord_server, remote_task_path)

    # Submit jobs
    print(f"[*] Submitting task {task_path.name} to bioclust.")
    submit_jobs(user, jord_server, bioclust_server, remote_task_path)


# TODO: check if this can be done with --chmod flag in rsync
def grant_permissions(username, server, task_path_on_cluster):
    # Give permissions to execute
    print("[*] Getting permission to execute")
    subprocess.run(f"ssh {username}@{server} '"
                   f"mv {task_path_on_cluster}/bash-script.sh ~/bash-script.sh && "
                   f"chmod a+x ~/bash-script.sh && "
                   f"mv ~/bash-script.sh {task_path_on_cluster}/bash-script.sh'", shell=True, check=True)

def submit_jobs(username, server, bioclust, task_path_on_cluster):
    # Submit jobs on bioclust
    print("[*] Submitting jobs")
    subprocess.run(f"ssh -J {username}@{server} {username}@{bioclust} '"
                   f"cd {task_path_on_cluster} && "
                   f"mkdir -p logs && "
                   f"condor_submit submission.sub && "
                   f"condor_wait -echo logs/log'", shell=True, check=True)



def list_tasks(script_directory):
    # List all task directories in the script directory
    script_directory = Path(script_directory).resolve()
    tasks = [d for d in script_directory.iterdir() if d.is_dir() and d.name.startswith('task-')]
    
    if not tasks:
        print("No task directories found.")
        return None
    
    print("Select a task:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.name}")
    
    selected_index = int(input("Enter the number corresponding to the task: ")) - 1
    
    if 0 <= selected_index < len(tasks):
        return tasks[selected_index]
    else:
        print("Invalid selection. Exiting.")
        return None

def copy_project_to_remote(username, local_project_path, remote_path):
    # Copy project to remote using rsync
    rsync_command = f"rsync -r --update {local_project_path} {username}@{jord_server}:{remote_path}"
    subprocess.run(rsync_command, shell=True, check=True)
    return Path(remote_path) / local_project_path.name

def modify_dlc_project_path(username, local_project_path, remote_project_path):
    # Modify DLC project path in config file
    config_path = Path(local_project_path) / 'config.yaml'
    tmp_config_path = shutil.copy(config_path, Path('/tmp') / config_path.name)  

    # Modify the DLC project path in the temporary config file
    with tmp_config_path.open(mode='r') as tmp_config_file:
        config_lines = tmp_config_file.readlines()

    for i, line in enumerate(config_lines):
        if line.strip().startswith('project_path:'):
            config_lines[i] = f'project_path: {remote_project_path}\n'
            break

    with tmp_config_path.open(mode='w') as tmp_config_file:
        tmp_config_file.writelines(config_lines)

    # Upload the modified config file to the server
    rsync_command = f"rsync --update {tmp_config_path} {username}@{jord_server}:{remote_project_path}/config.yaml"
    subprocess.run(rsync_command, shell=True, check=True)

    # Remove the temporary config file
    tmp_config_path.unlink()


def upload_task(username, script_directory, remote_project_path, task_path):
    # upload the task to the project path with rsync
    rsync_command = f"rsync -r --update {task_path} {username}@{jord_server}:{remote_project_path.parent}"
    subprocess.run(rsync_command, shell=True, check=True)
    return remote_project_path.parent / task_path.name

def modify_task_project_path(username, script_directory, remote_project_path, local_task_path, remote_task_path):
    tmp_config_path = shutil.copy(local_task_path / "python-script.py", Path('/tmp') / local_task_path.name)  
    # Modify the DLC project path in the temporary config file
    with tmp_config_path.open(mode='r') as tmp_config_file:
        config_lines = tmp_config_file.readlines()

    for i, line in enumerate(config_lines):
        if line.strip().startswith('config_path = '):
            config_lines[i] = f'config_path = {remote_project_path}/config.yaml\n'
            print("[*] Updated config_path in task script")
            break

    with tmp_config_path.open(mode='w') as tmp_config_file:
        tmp_config_file.writelines(config_lines)

    # Upload the modified config file to the server
    remote_script_path = remote_task_path / "python-script.py"
    rsync_command = f"rsync --update {tmp_config_path} {username}@{jord_server}:{remote_script_path}"
    subprocess.run(rsync_command, shell=True, check=True)

    # Remove the temporary config file
    tmp_config_path.unlink()


if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = Path(__file__).resolve().parent
    main(script_directory)

