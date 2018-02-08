# kilroy

## Set up the development environment
#### Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
#### Install [Vagrant](https://www.vagrantup.com/)
#### Pull the Repository
1. Install a [git](https://git-scm.com/download) client.
2. Using the git command line (The "Git CMD" program in Windows), navigate to where you want to download the project.
3. Download the project by executing `git clone https://github.com/PseudoDesign/kilroy.git`

#### Start up the VM
1. Navigate your command prompt to the "vagrant" directory
2. Execute `vagrant up`
3. Execute `vagrant ssh`

#### Install necessary tools
sudo apt-get update
sudo apt-get install python3.5
sudo python3.5 -m pip install squalchemy aioconsole pyyaml
sudo python3.5 -m pip install -U discord.py


#### Create a bot and invite it to your server
See [here](https://stackoverflow.com/questions/37689289/joining-a-server-with-the-discord-python-api)

#### Create a config.yaml file
```yaml
connections:
  - client: discord
    client_oauth_token: YOUR_CLIENT_OAUTH_TOKEN
plugins:
  - name: hello_kilroy
  - name: wallet
```

#### Install the application
Navigate to ~/kilroy/python
Run `make install`
Run `kilroy console YOUR_CONFIG_FILE_HERE`