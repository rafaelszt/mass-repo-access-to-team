#!/usr/bin/env python3
import requests
import sys
from getpass import getpass

LIST_REPOS_URL="https://api.github.com/orgs/%s/repos?page=%d&per_page=200"
ADD_REPO_TO_TEAM_URL="https://api.github.com/teams/%s/repos/%s/%s"
LIST_TEAMS_URL="https://api.github.com/orgs/%s/teams"

ACCESS_DENIED=-1
NOT_FOUND=-2


def get_team_id(org, team_name, token):
    # Get a list of teams
    teams = requests.get(LIST_TEAMS_URL %(org),
                        auth=("", token))

    if teams.status_code == 200:
        teams = teams.json()
        # Return the id of the one we want
        for team in teams:
            if team["name"] == team_name:
                return team["id"]

    else:
        # No permission to access teams
        return ACCESS_DENIED

    # Team not found
    return NOT_FOUND


def get_repo_list(org, token):
    repos = []
    # Change page if we have more than 200 repos
    for i in range(1, 10):
        # Request repos
        req = requests.get(LIST_REPOS_URL %(org, i),
                        auth=("", token))

        # Organization not found
        if req.status_code == 404:
            return NOT_FOUND

        req = req.json()
        # We only need the name of the repo
        for repo in req:
            repos.append(repo["name"])

        # If we got none, we can stop looping
        if len(req) is 0:
            break

    return repos


def grant_permission_to_repos(org, team_id, token, repos):
    # Grant permission on each repo
    for repo in repos:
        req = requests.put(ADD_REPO_TO_TEAM_URL %(team_id, org, repo), 
                    auth=("", token))

        # Can't grant access to repo
        if req.status_code == 401:
            return ACCESS_DENIED

    return 0


def main(org, team_name, token):
    print("Listing all the repos you have access to...", end=" ")
    sys.stdout.flush()

    repos = get_repo_list(org, token)
    if repos == NOT_FOUND:
        print("\nOrganization name not found.")
        return NOT_FOUND

    print("Done")

    team_id = get_team_id(org, team_name, token)
    if team_id == ACCESS_DENIED:
        print("Access denied when getting the team id, check your Access Token.")
        return ACCESS_DENIED
        
    elif team_id == NOT_FOUND:
        print("Team name not found.")
        return NOT_FOUND

    print("Granting access to {} repos...".format(len(repos)), end=" ")
    sys.stdout.flush()

    ret = grant_permission_to_repos(repos, team_id, token)
    if ret is not 0:
        if ret == ACCESS_DENIED:
            print("\nCould not grant permission, Access Denied")
            return ACCESS_DENIED
    
    print("Done")

if __name__ == '__main__':
    argc = len(sys.argv)
    
    if argc < 3:
        print("{} organization team_name [OPTIONAL: Github_Token]")
        
    elif argc >= 3:
        org = sys.argv[1]
        team_name = sys.argv[2]
        
        if argc == 3:
            token = getpass("Github Access Token: ")
        else:
            token = sys.argv[3]

        main(org, team_name, token)
