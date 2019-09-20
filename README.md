# Digital-Cafeteria
Automate mess billing using Raspberry Pi.

Django is used to design the website to accept payment.

Prototype Complete 12/09/2019

Installation procedure -

  [1] Clone or download the repository
  
  [2] Extract the archive file
  
  [3] Open terminal and execute ``pip3 install -r requirements.txt``
  
  [4] Open Kiosk/views.py in an editor and change path of all instances of db according to your path
  
  [5] Open terminal and execute ``python3 manage.py runserver``
  
  
To Do:
- Configure RFID and input any unique ID

- Edit sqlite db file in Kiosk/views.py before deploying to Pi


Steps to perform at set intervals:
  [1] Delete all items from DynamoDB Orders Table
  
  [2] Set current order to 0 in SQLite Orders table
  
  [3] Delete all items from local Orders table

