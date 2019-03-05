# dlme-harvest
DLME Scripts for harvesting data from providers

# Deployment

To deploy the latest harvest scripts to the VM from your machine.  Note, all changes
need to be committed to Github and merged to master branch before deploying.

`cap prod deploy`

# Ensure necessary python libraries are installed

The scripts require certain libraries to be installed on your laptop or server.
You need `pip` (python package installed) to install these python libraries
(pip is already setup on the server, along with python).  You should not need to
do this on the server (only first time setup)

```
pip install lxml --user
pip install sickle --user
```

# Running Scipts on Remove Server

Ensure you have a kerberos ticket:
```
kinit
```

```
ssh harvester@dlme-harvest # to get to the machine
cd current # to go the currently deployed code
```

You can then run your scripts, which will place the data in an "output" subfolder.

Note that you will probably want to run long running scripts in `screen` mode, so that
you can log out of the server and have them continue to run.
Full screen keyboard shortcuts: http://aperiodic.net/screen/quick_reference,
but basically:

```
# will show any currently running background processes (could be none):
screen -ls

# start a new screen called "bnf", helpful to give a useful name for later (note capital -S)
screen -S bnf
```

You will have a new process terminal window into which you can start a long running python
script....once running, leave the process running and exit the screen by
pressing `ctrl-a`, followed by `d`

This will now show your long running process:

```
screen -ls
```

Log off the server if you want

```
exit
```

Go back to the server later and find your long running process:

```
ssh harvester@dlme-harvest.stanford.edu
screen -ls
```

"Re-attach" to the process by name (substitute the name you used above when creating it):

```
screen -r bnf
```

If it is still running, exit with `ctrl-a`, `d` (like above) to keep the process going.
Or else you can kill the screen process if everything is done with: `exit`.  You will then be back at the main level
of the server, you can exit the server with `exit`.


# Committing data directly to dlme-metadata repo

The dlme-metadata repo is cloned on the server, and you can move data from the output folder and
then commit directly.

For example, this will move the everything that is currently in the "output" folder
on the server into the dlme-metadata folder, where it can be ready to commit.
You should confirm first that the data harvested in the output folder is correct
before committing, and be sure to commit to a new branch in the dlme-metadata repo
(as the example below shows):

```
ssh harvester@dlme-harvest.stanford.edu
cd dlme-metadata
mv ../current/output/ ./

git checkout -b 'new-data-branch'
git status
git add .
git commit -m 'new data'
```

# Getting data off the machine

This will fetch the entire `output` directory on the remote machine.  You can also specify
a subdirectory of the `output` directory to get only.

```
scp -r harvester@dlme-harvest:/opt/app/harvester/output /PATH/TO/LOCAL/DIRECTORY
```


* [Details on How To Add Data to DLME from a New Provider to DLME](docs/add_data_source.md)
