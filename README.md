# How I Create A Backdoor 😎

![Linux-ok](https://img.shields.io/badge/Linux-ok-green) ![MacOS-ok](https://img.shields.io/badge/MacOS-ok-green) ![Window-ok](https://img.shields.io/badge/Window-todo-lightgrey)

## ⚠️ Disclaimer
> Any actions and or activities related to the material contained within this repository is solely your responsibility. The misuse of the information in this website can result in criminal charges brought against the persons in question. The author will not be held responsible in the event any criminal charges be brought against any individuals misusing the information in this repository to break the law.



## 👌🏻 Basic Backdoor
### Description
Basic backdoor is the easiest backdoor that you could make.
The victim is just a server that redirects incoming messages into a shell and then sends back the shell output.
The victim IP can be found easly with `nmap`.

**⚠️ You usually need to be on the same subnet of the victim**

### Pre-requirements
- [netcat](http://netcat.sourceforge.net/) *Usually already installed*

### Usage
```bash
# On the victim
./basic-backdoor/backdoor.sh
```

```bash
# On the attacker
nc $VICTIM-IP 8080
```

## 💪🏻 Advanced Backdoor
### Description
This advanced backdoor allow to bypass the firewall and to communicate outside subnetwork.
Now the victim is just a client, the attacker is the server. When the victim is connected to the attacker's server, he'll execute command provided by the attacker and then send it back its output.
You can configure `PORT` and `DNS` inside the files [backdoor-client.py](./advanced-backdoor/backdoor-client.py) and [backdoor-server.py](./advanced-backdoor/backdoor-server.py).

> You can use [freenom](https://my.freenom.com) to get a free DNS.
> You can use [aws](https://aws.amazon.com/fr/ec2/) to get free server.

### Pre-requirements
- [python3](https://www.python.org/download/releases/3.0/) *Usually already installed*
- [pip](https://pip.pypa.io/en/stable/installing/) **Only for attacker**

### Usage
```bash
# On the victim for non-permanent backdoor
./advanced-backdoor/backdoor-client.py

# ⚠️ On the victim for "PERMANENT" backdoor
./advanced-backdoor/setup.sh
```

```bash
# On the attacker (where the DNS is pointing to)
pip3 install -r ./advanced-backdoor/requirements.txt
./advanced-backdoor/backdoor-server.py
```

*Take time to understand how it's working, PR are welcomed*
