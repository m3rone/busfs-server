# busfs-server

Basically Useless Simple File Storage is a very minimalist server side code with a web ui that lets you upload files, view uploaded files, and lets you download and delete those files. It is protected by basic HTTP authentication with an easy to set config. It is written in Python using Flask.

***Warning:*** This app currently does not have a secure way to open to WAN as it does not have a WSGI server configuration yet. Use this only in your local network for the time being.

### Features
- Collision protection: busfs appends a 10 character string to the end of your file to avoid collisions if the files have same names. Additionally, it just checks whether the uuid exists and assigns a new one.

- Descriptions: You can add and update descriptions of the files that you are uploading for more information.

- Security: busfs forces basic HTTP authentication for the entire app. Soon, there will be token based authentication and maybe even multi user support for shared and private directories later on.

- Clients: After busfs is in working order, clients for different platforms (Linux, Windows, maybe even Android) will be developed with both CLI and GUI alternatives. It is also very easy to integrate your own apps as all the API's are easily accessible.

- Simple with no maintenance: To run, you only have to install the dependencies and run a single file.

### Limitations
- Currently, busfs stores the user password in plaintext in the app.py file. Which means your username and password will reset if you just copy and paste the new version of this app in place of the old one. Regarding plaintext, it should not be an issue as someone who gets access to your server already has access to your files. Please encrypt your files if this is a concern.

- It supports only one user account. 

- UI could be better. I am working on it.

---
### Installation
After you install, the username and password will be `admin`. You may change it if you wish in the `app.py` file. Additionally, it will run on `0.0.0.0:6798`. That also can be changed in the `app.py` file.

From Codeberg
1. Install `git`, and `python3`.
2. Run `git clone https://codeberg.org/m3r/busfs-server.git` in your terminal
3. Run `cd busfs-server`
4. Run `python3 -m venv venv`
5. Run `source venv/bin/activate`
6. Run `python3 -m pip install -r requirements.txt`
7. Run `python3 app.py` to start the app.
   
From script
1. Run `curl https://codeberg.org/m3r/busfs-server/raw/branch/master/install.sh | sh` (works with `apt`, `dnf`, `pacman`, and `brew`)
2. Run `python3 app.py` to start the app.

Using Docker
1. (soon)

Using an executable
1. (soon)

### TODO / Roadmap
- [ ] Manage configuration through a config.ini file
- [ ] Provide docker images
- [ ] Provide executables with PyInstaller
- [x] Add file downloads
- [x] Add file deletion
- [x] Fix button spacing/Improve UX within the webapp
- [ ] Create clients 
- [x] Switch to 10 digit UUID's instead of 4
- [ ] Switch to Flask-Security
- [ ] Add versions and releases to the app


### "Maybe" features
- [ ] Multi user support with 
- [ ] Public links for files 
- [ ] Switch to SQLite