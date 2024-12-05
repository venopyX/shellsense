# Use a dynamic plugin directory
PLUGIN_DIR=$(dirname ${(%):-%N})/..
alias shellsense="python3 $PLUGIN_DIR/pyplugin/main.py"
alias ai_chat="shellsense -c"
alias ai_cloudflare="shellsense -cf"
alias ai_query="shellsense -q"
