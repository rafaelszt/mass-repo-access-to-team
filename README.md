# mass-repo-access-to-team
Grants access to all repositories of an organization to a given team

Python3 required

usage:
python3 grant_access.py <organization name> <team name> [Optional: Access Token]

If you don't pass the Access Token as a parameter, it will be asked later

The Access Key needs at least the following permission:
repo
  repo:Status
  repo_deployment
  public_repo
  repo:invite
  
admin:org
  write:org
  read:org

3rd party libraries:
  http://docs.python-requests.org/en/master/
  
