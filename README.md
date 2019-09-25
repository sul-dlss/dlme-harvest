[![CircleCI](https://circleci.com/gh/sul-dlss/dlme-harvest.svg?style=svg)](https://circleci.com/gh/sul-dlss/dlme-harvest)

# dlme-harvest
DLME Scripts for harvesting data from providers

# Harvest Scripts

Both python 2 and python 3 are installed on the server.  Use `python` to run python 2 scripts and use
`python3` to run python 3 scripts.  Note that any packages installed via `pip` will be installed under python 3 only.

## oai-harvest.py

OAI-PMH collections can be harvested with `oai-harvest.py` by calling the script followed by the base url of the sources you wish to harvest, the metadata prefix, and the name of the institution.
```
python3 oai-harvest.py http://cdm21044.contentdm.oclc.org/oai/oai.php -m oai_dc
```
Files will be written to `output/data`,

### Optional flags
* `-s` If `-s ` is called, the script will grab available sets first and files will be written to `output/set_name/data`.
* `-i` If the `-i institution_name` is called, the script will look in the `do_not_harvest` dictionary in `helper.py` for the name of the institution and pass along sets to ignore if any are found.

# Harvest Server

## Deployment

To deploy the latest harvest scripts to the VM from your machine.  Note, all changes
need to be committed to Github before deploying.  The default branch to deploy is
master, but you can specify a specific branch name to deploy when issuing the cap command (or just press
return when asked to accept the master branch.)

`bundle exec cap prod deploy`

## Ensure necessary python libraries are installed

The scripts require certain libraries to be installed on your laptop or server.
You need `pip` (python package installed) to install these python libraries
(pip is already setup on the server, along with python).  You should not need to
do this on the server (only first time setup)

```
pip install lxml --user
pip install sickle --user
```

## Running Scipts on Remove Server

Ensure you have a kerberos ticket:
```
kinit
```

```
ssh harvester@dlme-harvest ## to get to the machine
cd current ## to go the currently deployed code
```

You can then run your scripts, which will place the data in an "output" subfolder.

Note that you will probably want to run long running scripts in `screen` mode, so that
you can log out of the server and have them continue to run.
Full screen keyboard shortcuts: http://aperiodic.net/screen/quick_reference,
but basically:

```
## will show any currently running background processes (could be none):
screen -ls

## start a new screen called "bnf", helpful to give a useful name for later (note capital -S)
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


## Committing data directly to dlme-metadata repo

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

## Getting data off the machine

This will fetch the entire `output` directory on the remote machine.  You can also specify
a subdirectory of the `output` directory to get only.

```
scp -r harvester@dlme-harvest:/opt/app/harvester/output /PATH/TO/LOCAL/DIRECTORY
```


* [Details on How To Add Data to DLME from a New Provider to DLME](docs/add_data_source.md)
