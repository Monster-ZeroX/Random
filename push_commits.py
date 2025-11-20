import subprocess
import sys

def get_commits_to_push():
    # Try to find commits ahead of origin/main
    try:
        # Check if origin/main exists
        subprocess.run(["git", "rev-parse", "--verify", "origin/main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Get commits ahead
        result = subprocess.run(["git", "log", "--reverse", "--pretty=format:%H", "origin/main..HEAD"], capture_output=True, text=True, check=True)
        commits = result.stdout.strip().splitlines()
        return commits
    except subprocess.CalledProcessError:
        # If origin/main doesn't exist, maybe we push all commits?
        # Let's assume we push all commits of the current branch
        print("origin/main not found, assuming all commits need to be pushed.")
        result = subprocess.run(["git", "log", "--reverse", "--pretty=format:%H"], capture_output=True, text=True, check=True)
        commits = result.stdout.strip().splitlines()
        return commits

def push_one_by_one(commits):
    total = len(commits)
    print(f"Found {total} commits to push.")
    for i, commit in enumerate(commits, 1):
        print(f"Pushing commit {i}/{total}: {commit}")
        try:
            # Push specific commit to main branch on origin
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
