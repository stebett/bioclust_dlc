import os
import shutil
import subprocess
from pathlib import Path


def task_name(task):
    return task.replace('task-', '')


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
        return tasks[selected_index].name
    else:
        print("Invalid selection. Exiting.")
        return None

def copy_project_to_cluster(local_project_path, cluster_path):
    # Copy project to cluster using rsync
    rsync_command = f"rsync -r --update {local_project_path} {cluster_path}"
    subprocess.run(rsync_command, shell=True, check=True)
    return Path(cluster_path) / Path(local_project_path).name

def modify_dlc_project_path(local_project_path, cluster_path):
    # Modify DLC project path in config file
    config_path = Path(local_project_path) / 'config.yaml'
    tmp_config_path = shutil.copy(config_path, Path('/tmp') / config_path.name)  

    # Modify the DLC project path in the temporary config file
    with tmp_config_path.open(mode='r') as tmp_config_file:
        config_lines = tmp_config_file.readlines()

    for i, line in enumerate(config_lines):
        if line.strip().startswith('project_path:'):
            config_lines[i] = f'project_path: {cluster_path}\n'
            break

    with tmp_config_path.open(mode='w') as tmp_config_file:
        tmp_config_file.writelines(config_lines)

    # Upload the modified config file to the server
    rsync_command = f"rsync --update {tmp_config_path} {cluster_path}/config.yaml"
    subprocess.run(rsync_command, shell=True, check=True)

    # Remove the temporary config file
    tmp_config_path.unlink()

def submit_task_to_bioclust(cluster_path, task):
    # Submit the task on bioclust
    submission_script_path = Path(cluster_path) / 'cluster' / task / f'submission-{task}.sub'
    condor_submit_command = f"condor_submit {submission_script_path}"
    subprocess.run(condor_submit_command, shell=True, check=True)



def upload_task(script_directory, cluster_project_path, task):
    # upload the task to the project path with rsync
    rsync_command = f"rsync -r --update {script_directory / task} {cluster_path.parent}"
    subprocess.run(rsync_command, shell=True, check=True)

def modify_task_project_path(script_directory, cluster_project_path, task):
    tmp_config_path = shutil.copy(script_directory / task / f"{task_name(task)}.py" , Path('/tmp') / task)  

    # Modify the DLC project path in the temporary config file
    with tmp_config_path.open(mode='r') as tmp_config_file:
        config_lines = tmp_config_file.readlines()

    for i, line in enumerate(config_lines):
        if line.strip().startswith('config_path = '):
            config_lines[i] = f'config_path = {cluster_project_path}/config.yaml\n'
            print("Updated config_path in task script")
            break

    with tmp_config_path.open(mode='w') as tmp_config_file:
        tmp_config_file.writelines(config_lines)

    # Upload the modified config file to the server
    rsync_command = f"rsync --update {tmp_config_path} {cluster_project_path.parent / task / task_name(task)}.py"
    subprocess.run(rsync_command, shell=True, check=True)

    # Remove the temporary config file
    tmp_config_path.unlink()

def main(script_directory):
    # List tasks and let the user select one
    task = list_tasks(script_directory)
    
    
    if not task:
        return

    # Input parameters
    local_project_path = Path(input("Enter the local path of the DLC project: ")).resolve()
    cluster_path = Path(input("Enter the working directory on the cluster: ")).resolve()

    # Copy project to cluster
    cluster_project_path = copy_project_to_cluster(local_project_path, cluster_path)

    # Modify DLC project path in config file
    modify_dlc_project_path(local_project_path, cluster_project_path)

    upload_task(script_directory, cluster_project_path, task)
    modify_task_project_path(script_directory, cluster_project_path, task)

    # Submit task to bioclust
    submit_task_to_bioclust(cluster_path, task)

    print(f"Task {task} submitted to bioclust.")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = Path(__file__).resolve().parent
    main(script_directory)

