import os
import gitlab
from dotenv import load_dotenv
import subprocess


GITLAB_URL = 'http://16.171.227.77:80'

def create_dir(dirpath: str) -> None:
    if not os.path.exists(dirpath):
        print("Creating Directory.\n")
        os.makedirs(dirpath)
    else:
        print("Directory already exists.\n")


def create_project(gl: object, project_name: str) -> object:
    try:
        project = gl.projects.create({'name': project_name})

        print(gl.projects.list())
    except Exception:
        print("Project already exists.")
        project = None
    finally:
        return project


def upload_file(gl: object, project: object, file_path: str, file_name: str) -> None:
    print("Uploading file " + file_name + " .")
    project.upload(file_name, filepath=file_path)


def open_vscode(target_path: str) -> None:
    subprocess.Popen(['code', target_path])


if __name__ == '__main__':
    # Creating a dir
    dirpath = input("Enter a containing directory (full path) for the project: \n")
    project_name = input("Enter a project name: \n")
    full_path = dirpath + "/" + project_name
    create_dir(full_path)

    # Defining gitlab connection
    load_dotenv()
    access_token = os.environ['GITLAB_ACCESS_TOKEN']
    gl = gitlab.Gitlab(url=GITLAB_URL, private_token=access_token)

    project = create_project(gl, project_name)

    file_name = input("Enter a file name to upload: ")
    upload_file(gl, project, full_path + "/" + file_name, file_name)
    open_vscode(full_path)
