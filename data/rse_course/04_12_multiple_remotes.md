# 4.12 Working with multiple remotes


*Estimated time to complete this notebook: 10 minutes*

## Distributed versus centralised

Older version control systems (cvs, svn) were "centralised"; the history was kept only on a server,
and all commits required an internet.

Centralised                    |  Distributed
-------------------------------|--------------------------
Server has history             |Every user has full history
Your computer has one snapshot |  Many local branches
To access history, need internet| History always available
You commit to remote server     | Users synchronise histories
cvs, subversion(svn)            | git, mercurial (hg), bazaar (bzr)

With modern distributed systems, we can add a second remote. This might be a personal *fork* on github:


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
working_dir = os.path.join(git_dir, "git_example")
os.chdir(working_dir)
```


```bash
%%bash
git checkout main
git remote add jack89roberts git@github.com:jack89roberts/github-example.git
git fetch jack89roberts
```

    Your branch is up to date with 'origin/main'.


    Already on 'main'
    From github.com:jack89roberts/github-example
     * [new branch]      main       -> jack89roberts/main
     * [new branch]      master     -> jack89roberts/master


Check your remote branches:


```bash
%%bash
git remote -v
```

    jack89roberts	git@github.com:jack89roberts/github-example.git (fetch)
    jack89roberts	git@github.com:jack89roberts/github-example.git (push)
    origin	git@github.com:alan-turing-institute/github-example.git (fetch)
    origin	git@github.com:alan-turing-institute/github-example.git (push)


and ensure that the newly-added remote is up-to-date


```bash
%%bash
git fetch jack89roberts
```


```python
%%writefile Pennines.md

Mountains In the Pennines
========================

* Cross Fell
* Whernside
```

    Writing Pennines.md



```bash
%%bash
git add Pennines.md
git commit -am "Add Whernside"
```

    [main 7444bd0] Add Whernside
     1 file changed, 6 insertions(+)
     create mode 100644 Pennines.md


We can specify which remote to push to by name:


```bash
%%bash
git push -uf jack89roberts main || echo "Push failed"
```

    Push failed


    ERROR: Permission to jack89roberts/github-example.git denied to deploy key.
    fatal: Could not read from remote repository.
    
    Please make sure you have the correct access rights
    and the repository exists.


... but note that you need to have the correct permissions to do so.


```bash
%%bash
git push -uf origin main
```

    Branch 'main' set up to track remote branch 'main' from 'origin'.


    To github.com:alan-turing-institute/github-example.git
     + 92a57e1...7444bd0 main -> main (forced update)


## Referencing remotes

You can always refer to commits on a remote like this:


```bash
%%bash
git fetch
git log --oneline --left-right jack89roberts/main...origin/main
```

    > 12ee6ad Add github pages YAML frontmatter
    > c8ba483 Add a makefile and ignore generated files
    > 537950c Commit Aonach onto main branch
    > 85b2797 Merge branch 'main' of github.com:alan-turing-institute/github-example
    > bc04a83 Add Glyder
    > ed30178 Add another Beacon
    > ecc3206 Merge branch 'main' of github.com:alan-turing-institute/github-example
    > 8cd684e Add a beacon
    > b8fb6c5 Translating from the Welsh
    > 34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    > 289afed Add Scotland
    > 0c976b0 Add wales
    > 82b4fa0 Add Helvellyn
    > 6ff088f Include lakes in the scope
    > d063119 Add lakeland
    > c489aab Revert "Add a lie about a mountain"
    > f79cacc Change title
    > 6e8a302 Add a lie about a mountain
    > 238eaff First commit of discourse on UK topography
    < 31ea056 Add Whernside
    < 009f998 Add github pages YAML frontmatter
    < 2f9bcc8 Add a makefile and ignore generated files
    < ae539cc Merge branch 'experiment' into main
    < 492fec5 Commit Aonach onto main branch
    < fe1c71d Add Cadair Idris
    < 338d4d6 Merge branch 'main' of https://github.com/alan-turing-institute/github-example into main
    < 07c4fea Add Glyder
    < c405c4d Add another Beacon
    < f8f20a6 Merge branch 'main' of https://github.com/alan-turing-institute/github-example into main
    < 1f69c3f Translating from the Welsh
    < b2b4fa3 Add a beacon
    < c1897d4 Merge branch 'main' of https://github.com/alan-turing-institute/github-example into main
    < 0e96c25 Add wales
    < 0de6b80 Add Scotland
    < 959e142 Add Helvellyn
    < 600ffe1 Include lakes in the scope
    < c7454a7 Add lakeland
    < 5342922 Revert "Add a lie about a mountain"
    < f65fd0b Change title
    < 8c467a3 Add a lie about a mountain
    < 1f92929 First commit of discourse on UK topography


To see the differences between remotes, for example.

To see what files you have changed that aren't updated on a particular remote, for example:


```bash
%%bash
git diff --name-only origin/main
```

    Pennines.md


When you reference remotes like this, you're working with a cached copy of the last time you interacted with the remote. You can do `git fetch` to update local data with the remotes without actually pulling. You can also get useful information about whether tracking branches are ahead or behind the remote branches they track:


```bash
%%bash
git branch -vv
```

    * main 7444bd0 [origin/main: ahead 1] Add Whernside


# Hosting Servers

## Hosting a local server

* Any repository can be a remote for pulls
* Can pull/push over shared folders or ssh
* Pushing to someone's working copy is dangerous
* Use `git init --bare` to make a copy for pushing
* You don't need to create a "server" as such, any 'bare' git repo will do.


```python
bare_dir = os.path.join(git_dir, "bare_repo")
os.chdir(git_dir)
```


```bash
%%bash
mkdir -p bare_repo
rm -rf bare_repo/*
cd bare_repo
git init --bare --initial-branch=main
```

    Initialized empty Git repository in /home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git/bare_repo/



```python
os.chdir(working_dir)
```


```bash
%%bash
git remote add local_bare ../bare_repo
git push -u local_bare main
```

    Branch 'main' set up to track remote branch 'main' from 'local_bare'.


    To ../bare_repo
     * [new branch]      main -> main


Check your remote branches:


```bash
%%bash
git remote -v
```

    jack89roberts	git@github.com:jack89roberts/github-example.git (fetch)
    jack89roberts	git@github.com:jack89roberts/github-example.git (push)
    local_bare	../bare_repo (fetch)
    local_bare	../bare_repo (push)
    origin	git@github.com:alan-turing-institute/github-example.git (fetch)
    origin	git@github.com:alan-turing-institute/github-example.git (push)


You can now work with this local repository, just as with any other git server.
If you have a colleague on a shared file system, you can use this approach to collaborate through that file system.

## Home-made SSH servers

Classroom exercise: Try creating a server for yourself using a machine you can SSH to:

``` bash
ssh <mymachine>
mkdir mygitserver
cd mygitserver
git init --bare
exit
git remote add <somename> ssh://user@host/mygitserver
git push -u <somename> master
```

# SSH keys and GitHub

Classroom exercise: If you haven't already, you should set things up so that you don't have to keep typing in your
password whenever you interact with GitHub via the command line.

You can do this with an "ssh keypair". You may have created a keypair in the
Software Carpentry shell training. Go to the [ssh settings
page](https://github.com/settings/ssh) on GitHub and upload your public key by
copying the content from your computer. (Probably at .ssh/id_rsa.pub)

If you have difficulties, the instructions for this are [on the GitHub
website](https://help.github.com/articles/generating-ssh-keys). 
