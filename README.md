# Step 1: 
set up a conda environment using the yml file (conda env create -f environment.yml) minimum requirements are python packages: ckanapi, scipy, pandas, matplotlib
install docker and docker compose
rename/copy the file env.example to .env
# Step 2: 
go to the directory "docker" and run 
> docker compose up

wait for all containers to run. this may take a few seconds. You can check their status with 
> docker ps

or in the gui. The UI in the browser can only be accessed if the container "nginx" is running.
You can further modify the ckan settings in the ckan.ini. This is located in the "/srv/app" directory in the ckan container.
You can access the container using
> docker exec -u 0 -it container_id /bin/bash

replace container_id with the ID you get from "docker ps" for the image "docker-ckan". This command will open a bash shell on the container and you can edit the ckan.ini from there e.g. using vi.
# Step 3
access the UI in the browser at 
> https://localhost:5000

by default you can login as an admit with the credentials Username: ckan_admin PW: test1234
here you can create organisations and groups to organize data sets and access rights
# Step 4
create the organisation e-conversion with the shortcut in "eco" in the URL
create the group "stein_group"
# Step 5
create a user and assign it to the stein group. 
create an API toke for that user
# Step 6
run the jupyter notebook or python script
this should create a set of data packages assigned to the stein group with standard plots and raw csv files added as ressources

