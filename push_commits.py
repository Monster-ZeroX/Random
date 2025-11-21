import subprocess
import sys

def get_commits_to_push():
    # Get all commits from the initial commit (1f0576c) to HEAD
    # We assume 1f0576c is the shared base or we just want to push everything after it
    # If we want to push EVERYTHING including 1f0576c, we can, but it's likely already there.
    # However, since we want to overwrite the remote history which has garbage, 
    # we should identify the first commit of our NEW history.
    # Our new history starts after 1f0576c.
    
    base_commit = "1f0576c37090b08f956ea59927422dda10071bc4"
    
    try:
        result = subprocess.run(["git", "log", "--reverse", "--pretty=format:%H", f"{base_commit}..HEAD"], capture_output=True, text=True, check=True)
        commits = result.stdout.strip().splitlines()
        return commits
    except subprocess.CalledProcessError:
        # Fallback if base not found
        result = subprocess.run(["git", "log", "--reverse", "--pretty=format:%H"], capture_output=True, text=True, check=True)
        commits = result.stdout.strip().splitlines()
        return commits

def push_one_by_one(commits):
    total = len(commits)
    print(f"Found {total} commits to push.")
    for i, commit in enumerate(commits, 1):
        print(f"Pushing commit {i}/{total}: {commit}")
        try:
            # Force push the first commit to overwrite divergence, then normal push
            if i == 1:
                 subprocess.run(["git", "push", "-f", "origin", f"{commit}:refs/heads/main"], check=True)
            else:
                 subprocess.run(["git", "push", "origin", f"{commit}:refs/heads/main"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to push commit {commit}: {e}")
            break

if __name__ == "__main__":
    commits = get_commits_to_push()
    if not commits:
        print("No commits to push.")
    else:
        push_one_by_one(commits)
