# Use a dynamic plugin directory
PLUGIN_DIR=$(dirname ${(%):-%N})/..
alias shellsense="python3 $PLUGIN_DIR/main.py"
alias sschat="shellsense -c"
alias sscfchat="shellsense -cf"
alias ssai="shellsense -q"
