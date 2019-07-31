# Personal Workflow System
*By and for Robert Swanson*

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
