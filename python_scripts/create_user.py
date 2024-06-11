import pandas as pd
import gitlab
from dotenv import load_dotenv
import os

# The spreadsheet's url
URL = 'https://docs.google.com/spreadsheets/d/1wU1346u_6U1VV9pxPRyRtv7OBucfnErKDUiUqWTwzSQ/export?format=csv&gid=0'
GITLAB_URL = 'http://16.171.227.77:80'
GROUP_NAME = 'test_group_with_a_name_that_hasnt_been_taken'


# Add user
def add_user(gl: object, employee_email: str, employee_password: str, employee_username: str, employee_name: str) -> object:
    try:
        prev_users = gl.users.list()
        user = gl.users.create({'email': employee_email,
                                'password': employee_password,
                                'username': employee_username,
                                'name': employee_name})
        users = gl.users.list()
        print(set(users) - set(prev_users))
    except Exception:
        print("User already exists.")
        user = gl.users.list(username=employee_username)[0]
    finally:
        return user

# Create Group
def create_group(gl: object, user: object) -> object:
    try:
        prev_groups = gl.groups.list()
        group = gl.groups.create({'name': GROUP_NAME, 'path': GROUP_NAME})
        groups = gl.groups.list()
        print(set(groups) - set(prev_groups))

        # Add user to the group
        member = group.members.create({'user_id': user.id,
                                    'access_level': gitlab.const.AccessLevel.REPORTER})
        print(group.members.list())
    except Exception:
        print("Group already exists.")
        group = gl.groups.get(gl.groups.list(search=GROUP_NAME)[0].id)
    finally:
        return group

# Create a project
def create_project(gl: object, group: object, user: object) -> object:
    try:
        project = gl.projects.create({'name': user.name, 'namespace_id': group.id})
        print(group.projects.list())
    except Exception:
        print("Project already exists.")
        project = gl.projects.get(GROUP_NAME+"/"+user.name)
    finally:
        return project

if __name__ == '__main__':
    # Parsing
    employees = pd.read_csv(URL)
    employees_dict = employees.to_dict(orient='records')

    employee = employees_dict[0]
    employee_name = employee["Name"]
    employee_email = employee["Email"]
    employee_username = employee["Username"]
    employee_password = employee["Password"]

    # Defining gitlab connection
    load_dotenv()
    access_token = os.environ['GITLAB_ACCESS_TOKEN']
    gl = gitlab.Gitlab(url=GITLAB_URL, private_token=access_token)

    user = add_user(gl, employee_email, employee_password, employee_username, employee_name)
    group = create_group(gl, user)
    project = create_project(gl, group, user)

