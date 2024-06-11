# Prerequisites:
  - AWS acount.
  - DockerHub account.
  - AWS cli Access keys.
  - ssh pem key.
  - Self hosted Gitlab on EC2 instance.
  
# Create a self hosted Gitlab CE container on an EC2:
  - create EC2 instance (t3.large or xlarge):
  - Create a yaml file in it:
  - Copy & past to the .yml file:
        
        version: '3.8'

        services:
        web:
            image: 'gitlab/gitlab-ce:latest'
            restart: always
            hostname: 'localhost'
            environment:
            GITLAB_OMNIBUS_CONFIG: |
                external_url 'http://localhost'
            ports:
            - '80:80'
            volumes:
            - '/srv/gitlab/config:/etc/gitlab'
            - '/srv/gitlab/logs:/var/log/gitlab'
            - '/srv/gitlab/data:/var/opt/gitlab'
            networks:
            - gitlab

        networks:
        gitlab:
            name: gitlab-network
  - Run the following commands:
    * ```sudo mkdir gitlab && cd gitlab```
    * ```sudo yum update -y```
    * ```sudo yum install docker -y```
    * ```sudo systemctl start docker```
    * ```sudo usermod -aG docker $USER```
    * ```sudo systemctl enable docker```
    * ```sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```
    * ```sudo chmod +x /usr/local/bin/docker-compose```
    * ```sudo docker-compose up -d```
        > to get the password run the command:
            ```sudo docker exec -it ec2-user-web-1 grep 'Password:' /etc/gitlab/```


# Create a Jenkins Master, Either as an instance or a container:
## Create a Jenkins master EC2 instance:
  - Run the following commands:
    * ```sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo```
    * ```sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key```
    * ```sudo yum upgrade```
    * ```sudo dnf install java-17-amazon-corretto -y```
    * ```sudo yum install jenkins -y```
    * ```sudo systemctl enable jenkins && sudo systemctl start jenkins```
    * ```sudo systemctl status jenkins``` - Verification
    * Run the following command to get the initial password for the default admin user: ```sudo cat /var/lib/jenkins/secrets/initialAdminPassword```
  - Install Plugins:
    - Manage Jenkins > Plugins > Available plugins > GitLub, git, Amazon EC2, Slack Notification, configuration as code, Publish Over SSH

## Create a jenkins master instance in a container:
  - Create EC2 instance, connect to it via ssh and run the following commands:
    * ```sudo sudo yum update -y```
    * ```sudo yum install docker -y```
    * ```sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```
    * ```sudo chmod +x /usr/local/bin/docker-compose```
    * ```sudo systemctl enable docker & sudo systemctl start docker```
    * ```sudo usermod -aG docker ec2-user```
    * ```sudo reboot```
    * ```sudo docker run --name jenkins -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home --restart always --name jenkins jenkins/jenkins:lts-jdk17```
  - Enter jenkins
  - user_name: root, to get the password run the command: 
    * ```sudo docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword```
  - Install plugins:
    *   Manage Jenkins > Plugins > Available plugins > GitLub, git, Amazon EC2, Slack Notification, configuration as code, Publish Over SSH

# Set up an AWS user with permissions to start/stop/terminate instances and a bit more:
  - On AWS go to services->IAM, set up a policy: policies->create a policy->JSON:
  - Paste these policy rules from the jenkins documentation into it:
   ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Stmt1312295543082",
                "Action": [
                    "ec2:DescribeSpotInstanceRequests",
                    "ec2:CancelSpotInstanceRequests",
                    "ec2:GetConsoleOutput",
                    "ec2:RequestSpotInstances",
                    "ec2:RunInstances",
                    "ec2:StartInstances",
                    "ec2:StopInstances",
                    "ec2:TerminateInstances",
                    "ec2:CreateTags",
                    "ec2:DeleteTags",
                    "ec2:DescribeInstances",
                    "ec2:DescribeInstanceTypes",
                    "ec2:DescribeKeyPairs",
                    "ec2:DescribeRegions",
                    "ec2:DescribeImages",
                    "ec2:DescribeAvailabilityZones",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeSubnets",
                    "iam:ListInstanceProfilesForRole",
                    "iam:PassRole",
                    "ec2:GetPasswordData"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }
```

# Create the (slave) EC2:
  - Create an AMI for the slaves.
  - Create a new amazon linux 2023 instance, with the security group and key pair we've created earlier.
  - Connect to the instance via ssh and run the following commands:
    * ```sudo yum update -y```
    * ```sudo yum install docker -y```
    * ```sudo systemctl enable docker && sudo systemctl start docker```
    * ```sudo systemctl status docker``` - Verification
    * ```sudo yum install git -y```
    * ```sudo usermod -aG docker ec2-user```
    * ```sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose```
    * ```sudo chown ec2-user:ec2-user /usr/local/bin/docker-compose```
    * ```sudo chmod +x /usr/local/bin/docker-compose```
    * ```sudo dnf install java-17-amazon-corretto -y```
  - Once everything is installed, go to EC2 instances, select the slave instance you've just created > actions > image and templates > create image.
  - Save the AMI ID
  
# Conect Jenkins Master to amazon ec2:
  - Go to the jenkins app webpage.
  - Manage jenkins > Cloud > add a new cloud > Amazon EC2 > "configure"
  - In Amazon EC2 Credentials click the '+Add' button > Jenkins > Kind: AWS Credentials > give it an ID and Description, 
  - In access key ID and Secret Access Key copy the user's access key and secret access key that you created earlier and click Add.
  - Select the newly created credentials.
  - Select the AWS region you're going to be using.
  - In EC2 Key Pair's Private Key press click the '+Add' button > Jenkins > Kind: SSH Username with private key.
  - Give it an ID and Description, as Username insert the AWS EC2 user with the instance management policies that we've create earlier,
  - As for Private Key click the Enter Directly > Add > copy the contents on the .pem file that you created earlier, including the header and tail text.
  - Click the Add button and select the newly created credentials > click test connection, if everything was entered right it should say "Success".
  - Click save. 
  - Click "configure" agent
  - You'll see the setting we've changed and at the bottom of the page: "AMIs List of AMIs to be launched as agents"
  - Click "add", and paste into the AMI ID the AMI ID that we've just created.
  - Click "check AMI", if it works correctly it should show your "account_id_num/ami_name".
  - In instance type select either "t2Micro" or "t3Micro", depending on what is included in the free-tier in the region you've selected.
  - In security group names insert the security group name we've created earlier.
  - In Remote FS Root enter: '/home/ec2-user'.
  - In Remote User enter: 'ec2-user'.
  - In AMI Type select: Unix.
  - Click Save.
  - Go to Manage jenkins > Nodes > Built-in Node > Configure > set Number of executors to 0.
  - Run a test build that executes echo "1" to see if the configurations worked and if it starts up an EC2 instace to perform the build.
  
  
  
  
# integrate gitlab with jenkins: 
  - [Guide On Youtube](https://www.youtube.com/watch?v=_8YjWDmLvAE)
  ### Go to the GitLab app webpage:
  - Login as admin/project maintainer
  - Go to: user > edit profile > Access Tokens > Add new token
  - give the key name
  - Copy and save the Gitlab API token for later
  
  ### go to the Jenkins app webpage:
  - Go to: Manage Jenkins > System > Jenkins Locations -> Jenkins URL: http://private_ip_of_jenkins_master_instance:8080/
  - Scroll down, once you reach GitLab click the "enable authentication for '/project' end-point
  - Give the connection a name: gitlab
  - In GitLab host URL insert: http://private_ip_of_gitlab_instance/ 
  - In Credentials click Add > Jenkins > Kind: Gitlab API token
  - Copy the access token into the jenkins credentials we were editing
  - Go to: Manage Jenkins > System > scroll down til "gitlab" > Connection name: gitlab > GitLab host URL: <gitlab ec2 Private IPv4 addresses> > Credentials > +Add > Kind: Gitlab API token > API token: 
        enter  the token > Add > Test conection > Save 
  - Create new project:
    - project > Configure > GitLab Connection: gitlab > Build when a change is pushed to GitLab: v > Push Events: v > Opened Merge Request Events: v > save


# Trigger via webhook:
  - Go to the Jenkins app webpage:
    - project > Configure > GitLab Connection:< >> Build when a change is pushed to GitLab: v > Push Events: v > Opened Merge Request Events: v > advenced > Secret token > Generate > Cpoy the token >
    save
  - Login with admin account > go to admin area > settings > Network > Outbound Requests > Expand > here add jenkins_master's_private_ip:8080 click Save Changes.
  - Go to the GitLab app webpage:
    - project > Settings > Webhook > Add new webhook > URL: <jenkins ec2 Private IPv4 addresses>/project/<your_project_name> > Paste the Token > 
    
# Example Test Pipeline
    pipeline {
        agent any
        stages {
            stage('fetch from gitlab') {
                steps {
                    echo 'fetching from GitLab'      
                }
            }
            stage('build app') {
                steps {
                    echo 'building...'            
                }
            }
            stage('test image') {
                steps {
                echo 'testing...'              
                }
            }
            stage('show images') {
                steps {
                    echo 'images'              
                }
            }
            stage('Login to Docker Hub') {      	
                steps{   
                    echo 'login'                    	       	     
                }           
            }
            stage('Push Image to Docker Hub') {         
                steps{                             
                    echo 'commit ok'                     
                }            
            } 
        }
        post {
        success {
            echo "success"
        }
        failure {
            echo "failure"
        }
        always {
            echo "always"
        }
        }
    }

# DockerHub
- Create a repository and an access key in order for the images to be uploaded from the pipeline.
- save the username and the acces key as secrets in the Jenkins.

# Slack:
  - [Guide](https://www.youtube.com/watch?v=EDVZli8GdUM)
  - Manage Jenkins > Credentials > Global > Add Credentials > Kind: Secret text > ID: slack_ bot > Description: slack_bot
  - Enter your workspace.
  - Go to plugins.jenkins.io/slack and save your bot token.