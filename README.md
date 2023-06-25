# Red Team Village 2023 CTF - Setup and Walkthrough

## Setup Instructions

Build and run the Docker image:

```bash
sudo docker build -t rtv-2023 .
sudo docker run -p 80:80 rtv-2023
```

4. Access the application in your web browser by navigating to http://localhost.

## Walkthrough
1. Once the server is running, open your web browser and navigate to http://localhost.
2. You will be presented with the landing page of the Missle Terminal
3. The menus give error messages that are hints to the login password and loging page.
4. Using the hints, you can figure out the correct login password is `pipboy4life`.
5. Once logged in, you can access the Secure Terminal, which allows bash commands in the data folder.
6. Type `ls -a securit`y to see that there is a hidden launch key file.
7. Use `cat security/.launch_key` to get the password.
8. Return to the Missile Control page and type 4 to find the hidden control menu.
9. Select enter launch key and type in `Death is a preferable alternative to communism`.
10. The flag will be displayed on the screen: flag{584d0218c9c70bfebb5416967f5a35a1}.
