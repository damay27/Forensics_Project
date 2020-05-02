import docker
import os
import time
import subprocess
import sys

if len( sys.argv ) < 2:
    print("No container ID given")
else:
    container_id = sys.argv[1]

low_level_client = docker.APIClient("unix:///var/run/docker.sock")
client = docker.from_env()

#Get the path to where the container filesystem is stored on disk
target_data = low_level_client.inspect_container(container_id)
path = target_data["GraphDriver"]["Data"]["MergedDir"]

#Clear the previous data if it exists and setup the git repo
os.system("rm -rf ./merged")
os.system("mkdir ./merged")
os.system("git init ./merged")
os.chdir("./merged")

#This is the time from which all of the commits will be measured
start_time = time.time()

os.system("git add *")
os.system( "git commit -m%d" % (time.time() - start_time) )

#Keep looping as long as the container is still running
while( container_id[:10] in str(client.containers.list()) ):
    os.system("rm -rf merged")
    subprocess.check_output(["cp", "-r", path+"/", "./"])

    commit_message = time.time() - start_time

    output = str( subprocess.check_output( ["git", "status"] ) )
    print(output)

    if "nothing to commit" not in output:
        os.system("git add *")
        os.system( 'git commit -m %s' % (commit_message) )
        print("Found new data")
    else:
        print("No change detected")

    time.sleep(30)