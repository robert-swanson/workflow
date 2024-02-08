# Personal Workflow System
*By and for Robert Swanson*

## First Time Setup
1. `cd <desired root dir>`
2. `git clone git@github.com:robert-swanson/workflow.git`
3. `cd workflow`
4. `python setup.py`






## Local Management

### ns {scriptname} [category default:misc]
Creates new script locally and in workflow

### lss
Lists active scripts

### lsc
Lists catagories in workflow

### rs
Removes script locally and in workflow (any script in any category with name)

### rename {original} {new} {category}
Renames script locally and in workflow

### update
Copies from .workspace using the script found for this machine in `.workspace/hosts/thishost`. By standard should copy applicable scripts, and dot files.

### clearscripts
Removes all local scripts (not in workflow)ls


## Transferring 

### gpush
Stages, commits, and pushes workflow to github

### gpull
Pulls workflow from github, then runs update

### spush {desthost}
Sends workflow to `desthost` using scp

### spull {srchost}
Fetches workflow from `srchost` using scp


## Adding a new host
1. clone the repository into the home folder: `cd ~; git clone https://github.com/swanson7889/workflow.git`
2. cd into `workflow`
3. run `source update`, to get hostname
4. add a file to `pullhosts` and to `pushhosts` with the hostname as the filename, including the scripts to handle pulling from workflow to the machine, and updating the workflow respectivly
5. run `source gpull`
6. run `bash` to reset environment variables
