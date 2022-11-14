
## Corporate Web Site Backend

### Description

Corporative web site included functionality:

* Multilanguage


### What containers include
* As application engine has been used FastAPI.
* As database has been used PostgreSQL.
* Application running into containers.


### Prepare environment variables
Rename `.env_example` to `.env`  file.

Generate openssh private and public keys with command `ssh-keygen`.

Past private key in double quotes instead of `<open_ssh_rsa_priv_key>`.

Past public key in double quotes instead of `<open_ssh_rsa_pub_key>`.

Replace rest of values for your values.


### How to manage project

##### Run project

`./runserver.sh`

##### Stop project

`./stopserver.sh`

##### Display project

`docker ps`
