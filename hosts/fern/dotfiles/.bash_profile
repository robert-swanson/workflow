export PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:${PATH}"

#Add Workflow to path
export PATH=/Users/robertswanson/dev/workflow/local_scripts:$PATH
export PATH=/Users/robertswanson/dev/workflow/workflow_scripts:$PATH
export WORKFLOW_PATH=/Users/robertswanson/dev/workflow

# Add Homebrew to path
eval "$(/opt/homebrew/bin/brew shellenv)"

#Fix tmux vim problems
export TERM=screen-256color

#Silence zsh warning
export BASH_SILENCE_DEPRECATION_WARNING=1


#Set prompt
export PS1="\[\e[32m\]\h\[\e[m\]\[\e[32m\]:\[\e[m\]\[\e[35m\]\W\[\e[m\] "

