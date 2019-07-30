# Personal Workflow System
*By and for Robert Swanson*

## Local Management

### ns {scriptname} [catagory]
Creates new script locally and in .workflow

### edit {scriptname}
Opens `scriptname` in vim, then copies it to .workflow

### lss
Lists active scripts

### lsc
Lists catagories in .workflow

### rs
Removes script locally and in .workflow

### update
Copies from .workspace using the script found for this machine in `.workspace/hosts/thishost`. By standard should copy applicable scripts, and dot files.


## Transferring .workflow

### gpush
Stages, commits, and pushes .workflow to github

### gpull
Pulls .workflow from github, then runs update

### spush <desthost>
Sends .workflow to `desthost` using scp

### spull <srchost>
Fetches .workflow from `srchost` using scp 
