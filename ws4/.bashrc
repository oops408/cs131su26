# WS4 .bashrc file
# Aliases
alias ll='ls -alFh'
alias croot='cd ~/cs131'
alias ws4='cd ~/cs131/ws4'
alias gs='git status'
alias gl='git log --oneline --graph --decorate -5'
# Create a directory and enter the directory at the same time
mkcd ()
{
if [ -z "$1" ]; then
echo "Usage: mkcd directory_name"
return 1
fi
mkdir -p "$1" && cd "$1"
}
# Search (inside the cs131 folder) for any word or pattern
cfind ()
{
if [ -z "$1" ]; then
echo "Usage: cfind search_term"
return 1
fi
grep -RIn --color=always "$1" ~/cs131 2>/dev/null
}
# Make a timestamped backup copy of a file
backup ()
{
if [ -z "$1" ]; then
echo "Usage: backup filename"
return 1
fi
if [ -f "$1" ]; then
cp "$1" "$1.bak.$(date +%Y%m%d-%H%M%S)"
echo "Backup created for $1"
else
echo "Error: $1 is not a valid file"
return 1
fi
}
# Prompt that shows user, host, folder, and command prompt
PS1='\u@\h:\w$ '
