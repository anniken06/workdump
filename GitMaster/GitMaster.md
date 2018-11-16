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
			-  non-merge commits have exactly 1 parent commit
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
	- Remote - a named reference to remote repository (default name: origin)
	- Remote branch - a local copy of a branch in the remote (default name: origin/<BRANCH_NAME>)
	- Workspace - the local directory of the repository / the folder in your hard drive
	- Index / Staging area - contains all the changes to be tracked
	- Upstream - where to pull
	- Downstream - where to push

# Revisions
	- Revisions are ways of specifying commits
	- Revisions are specified using any of following:
		- Commit hash: `<COMMIT_HASH>`
		- Named reference (REF_NAME) with an optional suffix (REF_NAME_SUFFIX):
			- Reference name without suffix: `<REF_NAME>`
			- Reference name with suffix: `<REF_NAME><REF_NAME_SUFFIX>`
			- Reference name suffixes (REF_NAME_SUFFIX):
				- From time: `@{'<NUMBER> <seconds|minutes|hours|days|weeks|months> ago'}`
				- From upstream: `@{upstream}`
				- From downstream: `@{push}`
		- Revisions from other revisions (REV):
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
		- The 2nd parent of the 1st parent of my-tag: `my-tag^1^2`
		- The 3rd generation ancestor of c4470d0d5: `c4470d0d5~3` or `c4470d0d5^1^1^1`
		- The commits in HEAD that are not in master: `master..HEAD`

# [WIP] \(Preferably\) Git GUI commands
	- git add
	- git rm
	- git diff
	- etc etc

# [WIP] \(Preferably\) Git CLI commands


- Sourcetree
- git config: https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration
- git bisect: https://www.youtube.com/watch?v=REaowJ8JSfw
	+ Regression binary search
	- git rev-parse
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-add.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-apply.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-bisect.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-blame.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-branch.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-checkout.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-cherry-pick.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-cherry.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-citool.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-clean.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-clone.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-commit.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-config.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-diff-tree.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-diff.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-difftool.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-fetch.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-for-each-ref.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-gc.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-gui.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-help.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-init.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-log.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-ls-files.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-ls-tree.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-merge-base.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-merge.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-mergetool.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-notes.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-prune.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-pull.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-push.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-rebase.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-reflog.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-remote.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-reset.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-revert.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-rm.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-show-branch.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-show-ref.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-show.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-stash.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-status.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-tag.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-var.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-whatchanged.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/git-worktree.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/gitcli.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/gitglossary.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/gitignore.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/gitk.html
file:///C:/Program%20Files/Git/mingw64/share/doc/git-doc/gitrevisions.html

