# BUSFS-server

Basically Useless Simple File Storage is a very minimalist server side code with a web ui that lets you upload files, view uploaded files, and lets you download and delete those files. It is protected by basic HTTP authentication with an easy to set config. It is written in Python using Flask.

For more documentation, please visit the wiki.

It still is in beta so the format and everything may change in updates without warning (though release notes will say it). Use it at your own risk

### Features
- Collision protection: BUSFS uses a random 10 character string to identify and operate on your files to avoid collisions if the files have same names. Additionally, it just checks whether the uuid exists and assigns a new one if it does.

- Descriptions: You can add and update descriptions of the files that you are uploading for more information.

- Security: BUSFS forces basic HTTP authentication for the entire app. Soon, there will be token based authentication and maybe even multi user support for shared and private directories later on.

- Clients: After BUSFS is in working order, clients for different platforms (Linux, Windows, maybe even Android) will be developed with both CLI and GUI alternatives. It is also very easy to integrate your own apps as all the API's are easily accessible.

- Simple with no maintenance: To run, you only have to install the dependencies and run a single command.

### Limitations
- Currently, BUSFS stores the user password in plaintext in the config.ini file. However, it should not be an issue as someone who gets access to your server already has access to your files. Please encrypt your files if this is a concern.

- It supports only one user account. 

- UI could be better. I am working on it.

---
### Installing BUSFS
The default username and password is `admin` and can be changed through the web interface or by modifying the `app/config.ini` file.

From Codeberg
1. Install `git`, and `python3`.
2. Run `git clone https://codeberg.org/m3r/busfs-server.git` in your terminal to clone the repo
3. Run `cd busfs-server`
4. Run `python3 -m venv venv` to create the virtual environment
5. Run `source venv/bin/activate` to activate the virtual environment (`deactivate` to deactivate it)
6. Run `python3 -m pip install -r requirements.txt` to install the dependencies
   
From script
1. Run `curl https://codeberg.org/m3r/busfs-server/raw/branch/master/install.sh | sh` (works with `apt`, `dnf`, `zypper`, `pacman`, `brew`, `apk`, and `yum`)

Using Docker
1. Run `docker pull codeberg.org/m3r/busfs-server:latest` to pull the image 

Using an executable
1. (soon)

### Starting BUSFS

If you've installed from Codeberg or the script, run `uwsgi --http-socket 127.0.0.1:6798 --wsgi-file start.py` (always be in the virtual environment when running. The script puts you in one).

If you are using docker, run `docker run -d -p 127.0.0.1:6798:6798 -v busfs-data:/app busfs-server:latest` to run the image. You can change the host and port by editing the `127.0.0.1:6798` part.

You can adjust the host and port by modifying the commands above

### Updating BUSFS

soon:tm:

#### To consider
- It should be noted that if you put BUSFS behind a reverse proxy, do not forget to increase the maximum body size (guides for [nginx](https://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size), [apache](https://ubiq.co/tech-blog/increase-file-upload-size-apache), [caddy](https://caddyserver.com/docs/modules/http.handlers.request_body), [lighttpd](https://redmine.lighttpd.net/projects/lighttpd/wiki/Server_max-request-sizeDetails)) otherwise you will get a 413 error.

- By default, update checking is disabled. You can enable it by typing `yes` instead of `no` in config.ini file.

- You may want to use [`screen`](https://wiki.archlinux.org/title/GNU_Screen) or daemonize uWSGI by adding `--daemonize logfile.log` to the start command to keep uWSGI running in the background **if** you have installed it via Codeberg or script. With docker, `-d` flag takes care of that.

- If you have set a limit on how big your /tmp can get, that will limit you to the maximum size you can upload.
### TODO / Roadmap
- [x] Manage configuration through a config.ini file
- [x] Provide docker images
- [ ] Provide executables with PyInstaller
- [x] Add file downloads
- [x] Add file deletion
- [x] Fix button spacing/Improve UX within the webapp
- [ ] Create clients 
- [x] Switch to 10 digit UUID's instead of 4
- [ ] Switch to Flask-Security
- [x] Add versions and releases to the app
- [ ] Write a wiki


### "Maybe" features
- [ ] Multi user support with 
- [ ] Public links for files 
- [ ] Switch to SQLite
