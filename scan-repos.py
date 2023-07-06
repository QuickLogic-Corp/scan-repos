#!/usr/bin/python3

import os
import tempfile
import json
import argparse

parser = argparse.ArgumentParser(description="List repos associated with a git user")
parser.add_argument('user_name', nargs='+')
args = parser.parse_args()

def main():
    # Set up temp file
    temp_file_name = tempfile.mkstemp(suffix=".scan_git", text=True)[1]
    
    # print header
    print(f"user name, private, repo name")
    for user_name in args.user_name:
        for page in range(1,100):
            status = os.system(f"curl https://api.github.com/users/{user_name}/repos?page={page} > {temp_file_name} 2> /dev/null")
            if status != 0:
                print(f"Error: curl reported error status={status} on user={user_name}. Skipping user")
                break
            with open(temp_file_name, 'r') as json_file:
                repo_dict = json.load(json_file)
                if repo_dict == []:
                    break
                if 'message' in repo_dict:
                    print(f"Error: looking for user={user_name} and git reported \'{repo_dict['message']}\'. Skipping user.")
                    break
                # print(f"{repo_dict=}")
                for repo in repo_dict:
                    # print(f"\n\n***\n{repo}")
                    print(f"{repo['owner']['login']}, {repo['private']}, {repo['name']}")
    
    # Cleanup temp file
    os.system(f"rm {temp_file_name}")

if __name__ == "__main__":
    main()