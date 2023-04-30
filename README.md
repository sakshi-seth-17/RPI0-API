# RPI0-API
This API is built using Python's flask package to store information coming in from RPI0 to firebase database. RPI0 does not support firebase package hence, this API

---

### Flow of the application:
<img src="https://github.com/sakshi-seth-17/RPI0-API/blob/main/RPI0-API-Flow.jpg" alt="Alt text" title="Optional title">


### Instructions
1. Clone this repository. \
`git clone https://github.com/sakshi-seth-17/RPI0-API.git`

2. Make neccessary changes required in the app.py wrt specific path. 

3. Travel to the parent project directory and install the required python packages. \
Create virtual environment – `python3 -m venv venv` \
`source venv/bin/activate` \
`pip3 install -r requirement.txt` \
`To check if application is working fine run – python3 app.py` 

### API listing on webserver
1. To access any API from outside the server, the API needs to be listed on the server.
2. Steps to register the API on the server with reverse proxy:
  - First, allow outgoing port - `sudo ufw allow 8072`
  - `sudo ufw enable`
  - `sudo ufw status`
  - `cd /etc/apache2/sites-available`
  - `sudo nano 000-default.conf` \
    o	Add below lines \
    
    
              #pi0
              ProxyPass /rpi0  http://128.192.158.63:8072/rpi0
              ProxyPassReverse /rpi0  http://128.192.158.63:8072/rpi0
              
              
  - Now restart apache2 \
    `sudo systemctl restart apache2` \
    `sudo systemctl status apache2` 
    

### Create service file to make the app run indefinitely
`sudo nano /lib/systemd/system/rpi0.service` \
Paste below lines inside the file by making necessary changes


              [Unit] 
              Description=rpi0 
              After=multi-user.target 

              [Service] 
              User=webserver 
              Type=idle 
              ExecStart=/var/www/aspendb/probesearch/rpi0/venv/bin/python3 /var/www/aspendb/probesearch/rpi0/app.py 
              Restart=on-failure 


              [Install] 
              WantedBy=multi-user.target 

`sudo chmod 644 /lib/systemd/system/SensorsData.service` \
`sudo systemctl enable rpi0.service` \
`sudo systemctl daemon-reload` \
`sudo systemctl start rpi0.service` \
`sudo systemctl status rpi0.service` 

---
### Location details of the components:
1.	Application code path (on webserver - webserver@128.192.158.63) path: /var/www/aspendb/probesearch/rpi0

---
### Technical details:
1. The application is built using Python.
2. The application runs on port 8072

---
### Folder Structure
- venv/
- app.py
- userdefined.py
- requirement.txt
- config.json (Not on github, need to ask for this file from lab members)
- db-key.json (Not on github, need to ask for this file from lab members)	
