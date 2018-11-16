[TOC]



# What is Git
	- Git = file system + versioning + branching & merging
	- Git is a persistent map where the keys are SHA1 hashes and they reference primitive objects

# Primitive objects in Git
	- Blob - raw data
	- Tree (folder) - contains:
		- references to file blobs and metadata like filename, permissions, etc.
		- references to subtrees (subfolders)
			- this is what emulates the folder/directory structure
	- Commit - contains:
		- reference to the root tree
			- a snapshot of the root directory at the time of commit
		- references to parent commits
			- a way to trace the history
				- non-merge commits have exactly 1 parent commit
				- merge commits have multiple parent commits
		- commit message, time of commit, author name & email

# How Git tracks changes
	- When the changes of some file is tracked:
		1. it's blob conents changes
		2. the blob's reference changes
		3. it's tree contents changes (to reference the new blob)
		4. the tree's reference changes
		5. the tree's supertrees has to update as well (to reference the new tree) until the root tree
	- A new commit has to be made to track the reference to the new root tree

# Other objects in Git
	- Named reference - a name associated with an actual reference (SHA1 hash)
	- HEAD - a named reference to the latest commit in the current branch
	- Branch - a named reference to some commit
		- New commits to a branch will automatically update its referenced commit
	- Tag - a named reference to some commit, but no auto updates
		- Useful for saving unfinished work or creating backups
	- Remote - a named remote reference to remote repository (default name: origin)
	- Remote-tracking branch - a local copy of a branch in the remote (default name: origin/<BRANCH_NAME>)
	- Remote branch - the branch that exists in the remote (default name: origin <BRANCH_NAME>)
	- Working tree - the local directory of the repository / the folder in your hard drive
	- Index / Staging area - contains all the changes to be tracked
	- Upstream - where to pull from
	- Downstream - where to push to
	- gitignore: Specifies intentionally untracked files to ignore
	- detached HEAD: Occurs whenever HEAD does not refer to a branch
	- patch: Stored file diffs

# Revisions
	- [Revisions](https://git-scm.com/docs/gitrevisions) are ways of specifying commits
	- Revisions are specified using any of following:
		- Commit hash: `<COMMIT_HASH>`
		- Named reference (REF_NAME) with an optional suffix (REF_NAME_SUFFIX):
			- Reference name without suffix: `<REF_NAME>`
			- Reference name with suffix: `<REF_NAME><REF_NAME_SUFFIX>`
			- Reference name suffixes (REF_NAME_SUFFIX):
				- From time: `@{'<NUMBER> <seconds|minutes|hours|days|weeks|months> ago'}`
				- From upstream: `@{upstream}`
				- From downstream: `@{push}`
		- Revisions from other revisions (REV) with an optional suffix (REV_SUFFIX):
			- Revision without suffix: `<REV>`
			- Revision with suffix: `<REV><REV_SUFFIX>`
			- Revision suffixes (REV_SUFFIX):
				- From N-th parent: `^{N}`
				- From N-th generation ancestor (takes the first parents only): `~{N}` 
		- Revision ranges from other revisions:
			- All commits from REV_2 that are not in REV_1: `<REV_1>..<REV_2>`
	- Examples:
		- The current head: `HEAD`
		- The commit on my-branch 10 minutes ago: `my-branch@{'10 minutes ago'}`
		- The commit on the master branch in the remote: `master@{upstream}`
		- The 2nd parent of the 1st parent of my-tag: `my-tag^1^2`
		- The 3rd generation ancestor of c4470d0d5: `c4470d0d5~3` or `c4470d0d5^1^1^1`
		- The commits in HEAD that are not in master: `master..HEAD`

# ..., Pathspec, Resolution strategy, Reflog
	- `...` denotes a repeatable argument (space separated)  
	- Pathspecs are ways of specifiying paths that to be passed to certain Git commands
		- Pathspecs are usually preceded by two dashes: `<GIT_COMMAND> -- <PATHSPEC>`
		- Pathspecs are specified using any of following:
			- Individual file path/s: `<FILE_i>...`
			- File paths in the glob pattern: `lib/*.js`
		- Examples:
			- `git add -- file1.txt file2.txt file3.txt`
			- `git rm -- file*.txt`
	- Resolution strategy is a rule that automatically resolves conflicts
		- `ours`: Forces conflicting hunks to be auto-resolved cleanly by favoring our version
		- `theirs`: Opposite of ours
	- Reference logs (reflogs) record when references were updated in the local repository
		- This includes the previous states of HEAD - good for reverting bad resets, checkouts, merges

# [WIP] Git commands
A non-exhaustive list of Git commands and command options
- Preferably GUI commands:
	- [add](https://git-scm.com/docs/git-add.html): Add file contents to the index
		- `git add <FILE>`
		- `git add -- <PATHSPEC>`
	- [blame](https://git-scm.com/docs/git-blame.html): Show what revision and author last modified each line of a file
		- `git blame <FILE>`
		- `git blame -- <PATHSPEC>`
	- [cat-file](https://git-scm.com/docs/git-cat-file): Provide content or type and size information for repository objects
		- Try `git cat-file -p HEAD` to see the contents of HEAD commit file
	- [diff](https://git-scm.com/docs/git-diff.html): Show changes between commits, commit and working tree, etc
	- [cherry](https://git-scm.com/docs/git-cherry.html): Find commits yet to be applied to upstream
	- [diff-tree](https://git-scm.com/docs/git-diff-tree.html): Compares the content and mode of blobs found via two tree objects
	- [gui](https://git-scm.com/docs/git-gui.html): A portable graphical interface to Git
	- [ls-files](https://git-scm.com/docs/git-ls-files.html): Show information about files in the index and the working tree
	- [ls-tree](https://git-scm.com/docs/git-ls-tree.html): List the contents of a tree object
	- [rm](https://git-scm.com/docs/git-rm.html): Remove files from the working tree and from the index
		- `git rm <OPTIONS> <FILE>`
		- `git rm <OPTIONS> -- <PATHSPEC>`
		- `git rm <OPTIONS> <FOLDER>`
		- Options:
			- `-r`: Allows recursive removal when passing a folder
			- `--cached`: Remove file from the index but keep it in the working tree
	- [show-branch](https://git-scm.com/docs/git-show-branch.html): Show branches and their commits
	- [show-ref](https://git-scm.com/docs/git-show-ref.html): List references in a local repository
	- [show](https://git-scm.com/docs/git-show.html): Show various types of objects
- Preferably CLI commands:
	- [apply](https://git-scm.com/docs/git-apply.html): Apply a patch to files and/or to the index
	- [bisect](https://git-scm.com/docs/git-bisect.html): Use binary search to find the commit that introduced a bug
	- [checkout](https://git-scm.com/docs/git-checkout.html): Switch branches or restore working tree files
		- `git checkout <OPTIONS> <BRANCH_NAME>`: Switch branches
		- `git checkout <REV> -- <PATHSPEC>`: Resets the files in the pathspec to the version from the specified revision 
		- Options:
			- `-f`: Proceed even if the index or the working tree differs from HEAD and throw away local changes
			- `-b`: Create a new branch then switch
	- [cherry-pick](https://git-scm.com/docs/git-cherry-pick.html): Apply the changes introduced by some existing commits and create a new commit
		- `git cherry-pick <OPTIONS> <REV_i>...`: Apply diffs from the specified revisions
		- `git cherry-pick --<continue|quit|abort>`
		- Options:
			- `--no-commit`: Apply the changes but keep them in the index
	- [clean](https://git-scm.com/docs/git-clean.html): Remove untracked files from the working tree
	- [clone](https://git-scm.com/docs/git-clone.html): Clone a repository into a new directory
	- [commit](https://git-scm.com/docs/git-commit.html): Record changes to the repository
		- `git commit`: Create a new commit via text editor
		- `git commit <OPTIONS>`
		- Options:
			- `-m <MESSAGE>`: Specifies the commit message
			- `--fixup=<REV>`: Creates a commit that is fixup-able to the specified revision
				- By default, you can only create fixup commits applicable to the HEAD
	- [config](https://git-scm.com/docs/git-config.html): Get and set repository or global options
		- `git config <OPTIONS>`
		- Options:
			- `--list`: List all variables set in config file along with their values
			- `--global <KEY> <VALUE>`: Write to global config file rather than the repository config file
				- `--global user.name 'John Paul Guzman'`
				- `--global user.email 'JohnPaul.Guzman@infor.com'`
				- `--global core.editor 'notepad'`: Sets the text editor used by Git from vim to notepad
	- [fetch](https://git-scm.com/docs/git-fetch.html): Download objects and refs from another repository then update the remote-tracking branch
		- `git fetch`: Fetch current branch
		- `git fetch <OPTIONS>`
		- Options:
			- `--all`: Fetch all remotes
	- [gc](https://git-scm.com/docs/git-gc.html): Cleanup unnecessary files and optimize the local repository
	- [help](https://git-scm.com/docs/git-help.html): Display help information about Git
	- [init](https://git-scm.com/docs/git-init.html): Create an empty Git repository or reinitialize an existing one
	- [log](https://git-scm.com/docs/git-log.html): Show commit logs
		- `git log`
		- `git log <OPTIONS>`
		- Options:
			- `--oneline`: Shows abbreviated single line version of commit logs
	- [merge-base](https://git-scm.com/docs/git-merge-base.html): Find as good common ancestors as possible for a merge
	- [merge](https://git-scm.com/docs/git-merge.html): Join two or more development histories together
		- `git merge <OPTIONS> <REV_i>...`
		- `git merge --<abort|continue>`
		- Options:
			- `--strategy=<RESOLUTION_STRATEGY>`
	- [prune](https://git-scm.com/docs/git-prune.html): Prune all unreachable objects from the object database
	- [pull](https://git-scm.com/docs/git-pull.html): Fetch from and integrate with another repository or a local branch
		- `git pull`: An abbreviation for `git fetch` then `git merge origin/<CURRENT_BRANCH>`
		- `git pull <OPTIONS> <REMOTE> <BRANCH_NAME>`
		- Options:
			- `-f`: Forcefully pull when existing commits are overridden by rebased remote commits
			- `--rebase`: An abbreviation for `git fetch` then `git rebase` rather than `git merge`
			- `--strategy=<RESOLUTION_STRATEGY>`
	- [push](https://git-scm.com/docs/git-push.html): Update remote refs along with associated objects
		- `git push <OPTIONS> <REMOTE> <BRANCH_NAME>`
		- Options:
			- `-f`: Forcefully push when existing commits in the remote are overridden by rebased local commits 
	- [rebase](https://git-scm.com/docs/git-rebase.html): Reapply commits on top of another base tip
		- `git rebase <OPTIONS> <REV_i>...`
		- Options:
			- `--strategy=<RESOLUTION_STRATEGY>`
			- `<-i|--interactive>`: Make a list of the commits which are about to be rebased and lets the user edit the history using the following commands
				- `<p|pick>`: use commit
				- `<r|reword>`: use commit, but edit the commit message
				- `<e|edit>`: use commit, but stop for amending
				- `<s|squash>`: use commit, but meld into previous commit
				- `<f|fixup>`: like "squash", but discard this commit's log message
				- `<d|drop>`: remove commit
	- [reflog](https://git-scm.com/docs/git-reflog.html): Manage reflog information
		- `git reflog`
		- `git reflog <OPTIONS>`
		- Options:
			- `--all`: Process the reflogs of all references including the individual steps within rebase/merge
	- [remote](https://git-scm.com/docs/git-remote.html): Manage set of tracked repositories
	- [reset](https://git-scm.com/docs/git-reset.html): Reset current HEAD to the specified state
		- `git reset <MODE> <REV>`
		- Modes:
			- `--hard`: Reset the index and working tree
			- `--soft`: Keep the index and working tree
			- `--mixed`: Reset the index and keep the working tree (default)
	- [revert](https://git-scm.com/docs/git-revert.html): Revert some existing commits
	- [stash](https://git-scm.com/docs/git-stash.html): Stash the changes in a dirty working directory away
		- `git stash`
		- `git stash pop`: Applies the lastest stashed changes on the current working tree
	- [status](https://git-scm.com/docs/git-status.html): Show the working tree status
	- [tag](https://git-scm.com/docs/git-tag.html): Create, list, delete or verify a tag object signed with GPG
		- `git tag <TAG_NAME>`: Creates a new tag
		- `git tag <OPTIONS> <TAG_NAME>`
		- Options:
			- `-d`: Delete a tag
			- `-l`: List all tags

# [WIP] Git + Unix commands
Git works well with Unix commands
- Creating a patch from  a diff
	- Example: `git diff HEAD~1 > last_change.patch`: Redirect the output of diff to a file
- Display the (commit hash, file name, author, timestamp, line contents) of all the changes in origin/master made in Nov. 2018:
	- Example: `git ls-tree -r origin/master --name-only | xargs -I{} git blame {} | grep '2018-11-'`
		- `git ls-tree -r origin/master --name-only`: Display all the filenames in the tree of origin/master, then pipe out
		- `xargs -I{} git blame {}`: Take the piped filenames and passes it to git blame, then pipe out
		- `grep '2018-11-'`: Take the piped blame and keep only the rows that contain "2018-11-"
- etcetc.
