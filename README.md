# QBP_FTP_Proxy
Proxy script to fix AscendRMS' incomeplete implementation of QBP cart API

## Why this repo exists
AscendRMS implement's QBP's FTP guidlines in an incomplete way. This results in QBP always throwing an error and just staging the QBP order, rather than fully submitting it. This script intercepts the FTP request, repackages it in accordance with the Aug 2020 QBP guidelines, then sends it on to QBP. If the order is only shipping from a single warehouse, it will flow all the way through and send a confirmation email to the specified user in AscendRMS client.

If the order ships from two warehouses, it will still stage the order and not submit, but you will get a success email, rather than just an error email.

## Setup
- Create an FTP folder and user in a linux box, vm, etc
- Create a hostname or DNS redirect for your AscendRMS client to send the fil to this FTP proxy server, rather than straight to QBP
- Set up a cron job to run this script every minute or whenever you want