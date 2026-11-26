#
# ~/.bashrc
#

alias ls='ls --color=auto'
alias grep='grep --color=auto'

# Functions
cdoc() {
	cd ~/Documents
}
cdwn() {
	cd ~/Downloads
}
cprj() {
	source ~/.Scripts/cprj.sh
}

# Window title and Prompt
if [[ $TERM == "alacritty" ]]; then
	PROMPT_COMMAND="source ~/.Scripts/alacritty_prompt.sh"
fi

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
