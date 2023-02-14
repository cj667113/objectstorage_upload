###Developed by Christopher Johnston 2/14/2023###
import argparse
import subprocess
import os
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--provider", help = "Object Storage Provider")
parser.add_argument("-cf", "--config", help = "Config File")
parser.add_argument("-c", "--container", help = "Object Storage Container")
parser.add_argument("-f", "--filename", help = "Object Storage Filename")
args = parser.parse_args()
if args.provider and args.config and args.container and args.filename:
    provider=args.provider
    config=args.config
    container=args.container
    filename=args.filename
print(provider,container,config,filename)
def OpenstackProvider():
    import openstack
    def create_connection(auth_url, region, project_name, username, password,user_domain, project_domain):
        return openstack.connect(
            auth_url=auth_url,
            project_name=project_name,
            username=username,
            password=password,
            region_name=region,
            user_domain_name=user_domain,
            project_domain_name=project_domain,
        )
    cmd='source %s;printenv' %(config)
    env = subprocess.check_output([cmd], shell=True)
    auth_url=os.environ['OS_AUTH_URL']
    username=os.environ['OS_USERNAME']
    password=os.environ['OS_PASSWORD']
    try:
        region=os.environ['OS_REGION']
    except:
        region="RegionOne"
    project_name=os.environ['OS_PROJECT_NAME']
    project_domain=os.environ['OS_PROJECT_DOMAIN_NAME']
    user_domain=os.environ['OS_USER_DOMAIN_NAME']
    conn=create_connection(auth_url,region,project_name,username,password,user_domain,project_domain)
    with open(filename, 'r') as f:
        upload_data = f.read()
    upload = conn.object_store.upload_object(container=container, name=filename, data=upload_data)
    return upload
if provider=='openstack':
    upload=OpenstackProvider()
    print(upload)