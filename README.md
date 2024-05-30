# To run with automatic server restart (equivalent of nodemon on node.js)

### First install
pip install watchdog
### Finally run flask with watchdog
watchmedo auto-restart --patterns="*.py;*.html;*.css;*.js" --recursive -- flask run 

