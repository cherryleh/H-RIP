
http://hrip.manoa.hawaii.edu/

# Running locally:
sudo launchctl load -w /System/Library/LaunchDaemons/org.apache.httpd.plist
http://localhost:80

Had to edit 'sudo vi /etc/apache2/httpd.conf' to point to /Users/jgeis/Work/H-RIP
I've since put it back to the original and added a link to the one in my work directory.

------------------
# Jetstream

Site URL: ~~http://149.165.159.19/H-RIP/~~  
http://149.165.159.160/H-RIP/

GitHub: https://github.com/cherryleh/H-RIP  

## Logging in to Jetstream:
- https://jetstream2.exosphere.app/exosphere/projects (jgeis username)
- Use "ACCESS CI (XSEDE)" for identity provider, not "University of Hawaii"
- Click on existing allocation   
~~(RAPID: Tuning and Assessing Lahaina Wildfire Models with AI Enhanced Data)~~    
ASC190026 (Hawaii EPSCoR Project, Jetstream2 IU)

## Accessing the code
- Follow the "Logging in to Jetstream" instructions above
- Click on Instances
- Click on H-RIP-EPSCoR
- Click on Web Desktop
- Click on the terminal icon in the desktop that opened in a new browser tab
```
cd /var/www/html/
```

## Creating a new vm and apache server for H-RIP from scratch
- Follow the "Logging in to Jetstream" instructions above
- Click the "Create" button
- Select "Instance" from the resulting drop down menu
  - Select the latest Ubuntu version 
  - Name it "H-RIP-EPSCoR"
  - Select "m3.quad" for the flavor
  - Set a custom disk size of 100G.
  - Enable Web Desktop
  - Click the "Create" button at the bottom 

~~https://jetstream2.exosphere.app/exosphere/projects/ae2152821a6a4d5d866e10698d616466/regions/IU/servers/bbda40a9-0435-45f6-9fc3-7464afd56a53~~  
~~Public IP: 149.165.159.19~~  
~~Internal IP: 10.1.222.22~~  
~~hostname: h-rip.ees230061.projects.jetstream-cloud.org~~  
~~Open web desktop~~  
~~exouser@h-rip~~  
~~exouser@149.165.159.19~~  

https://jetstream2.exosphere.app/exosphere/projects/e547d834b2fe4beda5061b60dfc9df1b/regions/IU/servers/67f00085-ba27-4787-8650-b505fc7abbd0
Public IP: 149.165.159.160
Internal IP: 10.0.59.226  
hostname: h-rip-epscor.asc190026.projects.jetstream-cloud.org

ssh exouser@149.165.159.19  

### Install and start apache
``` 
sudo apt install apache2
sudo systemctl status apache2
```

### Install PHP
#### Windows:
```
sudo apt install php libapache2-mod-php
sudo systemctl restart apache2.service  
```
#### Mac/Linux
```
sudo apt install php
sudo apachectl restart
```

### Download the H-RIP code
```
cd /var/www/html
sudo git clone https://github.com/cherryleh/H-RIP.git
```

#### View the site via the internal remote web browser (the one in the web desktop):
To get internal IPs
```
hostname -I   
```
The command gave a list of IPs, one of which was 172.17.0.1.  

Bring up 172.17.0.1/H-RIP on the browser in the web desktop.

#### To view on your local machine via localhost port forwarding: 

- Get your local machine's IP address.  
- Run the following command on your local machine with the bracketed parts filled in:
```
ssh -v -L 3000:<your local machine's IP adress>:3000 exouser@<remote machine's IP address>
```
Example: 

~~ssh -v -L 3000:192.168.1.13:3000 exouser@149.165.159.19~~  
```
ssh -v -L 3000:192.168.1.66:3000 exouser@149.165.159.160  
```
- Then go to http://<remote-machine's IP address>/H-RIP/ in your local browser.

Example:  
~~http://149.165.159.19/H-RIP/~~  
http://149.165.159.160/H-RIP/

For details on the above procedure:  
https://stackoverflow.com/questions/18705453/ssh-l-connection-successful-but-localhost-port-forwarding-not-working-channel  

~~### mesonet example~~  
~~#ssh -L 3000:192.168.1.13:3000 exouser@149.165.152.187~~  
~~#http://149.165.152.187:8080/~~  
~~#Then go to http://localhost:3000/tapis-ui in local browser.~~  



### Install php:

To enable PHP in Apache add the following to httpd.conf and restart Apache:
```
sudo vi /etc/apache2/httpd.conf

    LoadModule php_module /usr/local/opt/php/lib/httpd/modules/libphp.so

    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>
```
Finally, check DirectoryIndex includes index.php:
```
    DirectoryIndex index.php index.html
```

The php.ini and php-fpm.ini file can be found by:
```
    whereis php
```
For the setup we have:  
~~/usr/local/etc/php/8.3/~~
```
less /etc/php/8.3/cli/php.ini
less /etc/php/8.3/apache2/php.ini
```

To start php now and restart at login:
```
  brew services start php
```
Or, if you don't want/need a background service you can just run:
```
  /usr/local/opt/php/sbin/php-fpm --nodaemonize
```


```
sudo tail -f /var/log/apache2/error.log
```

TODO: set up a certificate for php:  https://www.simplified.guide/macos/apache-php-homebrew-codesign


TODO:
- look at rainfall.py line 38, "dir_path = '../RID'"  That doesn't look right.
- Need to get rid of header menus "Select Ranch, About, Links, Contact" or make them work.
- Need to get rid of the "Learn More" button in the header or make it actually go somewhere.
- Fix the absolute urls in the header and on index.html (http://149.165.159.19/H-RIP/)


[Sat Jan 20 00:06:51.292530 2024] [php:error] [pid 1598339] [client 209.143.6.229:41978] PHP Fatal error:  Uncaught TypeError: fgetcsv(): Argument #1 ($stream) must be of type resource, bool given in /var/www/html/H-RIP/RID.php:69\nStack trace:\n#0 /var/www/html/H-RIP/RID.php(69): fgetcsv()\n#1 {main}\n  thrown in /var/www/html/H-RIP/RID.php on line 69, referer: https://www.google.com/
[Sat Jan 20 00:25:03.466402 2024] [php:error] [pid 1598339] [client 140.114.79.210:34880] script '/var/www/html/index.php' not found or unable to stat
[Sat Jan 20 01:08:00.481048 2024] [php:error] [pid 1598380] [client 76.83.173.151:50628] PHP Fatal error:  Uncaught TypeError: round(): Argument #1 ($num) must be of type int|float, string given in /var/www/html/H-RIP/RID.php:111\nStack trace:\n#0 /var/www/html/H-RIP/RID.php(111): round()\n#1 {main}\n  thrown in /var/www/html/H-RIP/RID.php on line 111
[Sat Jan 20 01:08:31.682351 2024] [php:error] [pid 1598391] [client 76.83.173.151:50629] PHP Fatal error:  Uncaught TypeError: round(): Argument #1 ($num) must be of type int|float, string given in /var/www/html/H-RIP/RID.php:111\nStack trace:\n#0 /var/www/html/H-RIP/RID.php(111): round()\n#1 {main}\n  thrown in /var/www/html/H-RIP/RID.php on line 111, referer: http://149.165.159.19/H-RIP/
[Sat Jan 20 01:09:43.237608 2024] [php:error] [pid 1598340] [client 76.83.173.151:50635] PHP Fatal error:  Uncaught TypeError: round(): Argument #1 ($num) must be of type int|float, string given in /var/www/html/H-RIP/RID.php:111\nStack trace:\n#0 /var/www/html/H-RIP/RID.php(111): round()\n#1 {main}\n  thrown in /var/www/html/H-RIP/RID.php on line 111”