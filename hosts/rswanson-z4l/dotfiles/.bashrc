# .bashrc

#set -o xtrace

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH


# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
	for rc in ~/.bashrc.d/*; do
		if [ -f "$rc" ]; then
			. "$rc"
		fi
	done
fi

unset rc


# Workflow Setup
export WORKFLOW_PATH="/home/rswanson/dev/workflow"
export PATH="$PATH:$WORKFLOW_PATH/local_scripts"
export PYTHONPATH="$PYTHONPATH:$WORKFLOW_PATH"
source ~/.aliases
set-pane-title

# Prompt
source ~/.git-prompt.sh
export PS1="\$(get-pane-title --prompt)\[\e[32m\]\h\[\e[m\]\[\e[32m\]:\[\e[31m\]\[\e[m\]\[\e[35m\]\W\[\e[m\]\$(set-pane-title) "
#PROMPT_COMMAND='__git_ps1 "\[\e[32m\]\h\[\e[m\]\[\e[32m\]:\[\e[31m\]"  " \[\e[m\]\[\e[35m\]\W\[\e[m\] "'
#PROMPT_COMMAND='__git_ps1 "\[\e[31m\]"  " \[\e[m\]\[\e[35m\]\W\[\e[m\] "'
PROMPT_COMMAND=

GIT_PS1_SHOWDIRTYSTATE=True
GIT_PS1_SHOWSTASHSTATE=
GIT_PS1_SHOWUNTRACKEDFILES=True
GIT_PS1_SHOWUPSTREAM=True
GIT_PS1_SHOWCONFLICTSTATE=True
GIT_PS1_SHOWCOLORHINTS=True


# FZF mappings and options
[ -f /usr/share/fzf/shell/key-bindings.bash ] && source /usr/share/fzf/shell/key-bindings.bash

# Fix tmux vim problems
export TERM=screen-256color

# Long Bash History
HISTSIZE=10000
HISTFILESIZE=200000
HISTCONTROL=ignoredups:erasedups
shopt -s histappend
#PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

# Hishtory Config:
#export PATH="$PATH:/home/rswanson/.hishtory"
#source /home/rswanson/.hishtory/config.sh
