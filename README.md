# github3apps.py

This project is an extension to the [github3.py](https://github.com/sigmavirus24/github3.py) project, with the purpose of enabling [GitHub Application](https://developer.github.com/apps/) development.

Using this library developers can access all of the special App endpoints as well as pull out a `github3.py` client authenticated by a specific installation.


## Usage

### Connect to Github as Application

To connect you need to pass the app id and the location of your app's private key.

```python
from github3apps import GithubApp

gha = GithubApp(app_id, path_to_private_key)
gha.set_user_agent('MyApp')
gha.get_app()
```


### List Available Installations

This returns the list of installations IDs available to your application.

```python
from github3apps import GithubApp

gha = GithubApp(app_id, path_to_private_key)
installation_ids = gha.get_installations()
```


### Get Repositories Available to Installation

This returns the list of repositories available to your specific installation.

```python
from github3apps import GithubApp

gha = GithubApp(app_id, path_to_private_key)

installation = gha.get_installation(installation_id)
installation.get_repositories()
```


### Comminicate with Github API as Installation

This returns a [github3.py](https://github.com/sigmavirus24/github3.py) client already authenticated against a specific installation.

```python
from github3apps import GithubApp

gha = GithubApp(app_id, path_to_private_key)
installation = gha.get_installation(installation_id)
gh = installation.get_github3_client()
```
