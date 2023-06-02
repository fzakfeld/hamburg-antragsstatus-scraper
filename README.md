When you request a new ID or passport in the city of Hamburg, you'll typically get a piece of paper with a serial number, pointing to https://serviceportal.hamburg.de/HamburgGateway/Service/Entry/PASSDA, where you can find out if the ID is ready for pickup. This script checks that status, saves it in a file called state.txt and notifies you via Telegram if it changed.

## Usage

Copy config.ini.example to config.ini and fill in your values. The script needs to be periodically called, e.g. via a cronjob. The script will save a file to the local file system, so it can't work in completely stateless environments.