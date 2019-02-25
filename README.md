# dlme-harvest
DLME Scripts for harvesting data from providers

# Deployment

To deploy the latest harvest scripts to the VM from your machine.  Note, all changes
need to be committed to Github and merged to master branch before deploying.

`cap prod deploy`

# Running Scipts on Remove Server

```
ssh harvester@dlme-harvest # to get to the machine
cd current # to go the currently deployed code

# run your scripts, updated to place data in the /opt/app/harvester/output directory
```

# Getting data off the machine

This will fetch the entire `output` directory on the remote machine.  You can also specify
a subdirectory of the `output` directory to get only.

```
scp -r harvester@dlme-harvest:/opt/app/harvester/output /PATH/TO/LOCAL/DIRECTORY
```
