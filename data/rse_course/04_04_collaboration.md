# 4.4 Collaboration

*Estimated time to complete this notebook: 20 minutes*

## Form a team

Now we're going to get to the most important question of all with Git and GitHub: working with others.

Organise into pairs. You're going to be working on the website of one of the two of you, together, so decide who is going to be the leader, and who the collaborator.

## Giving permission

The leader needs to let the collaborator have the right to make changes to his code.

In GitHub, go to `Settings` on the right, then `Collaborators & teams` on the left.

Add the user name of your collaborator to the box. They now have the right to push to your repository.

## Obtaining a colleague's code

Next, the collaborator needs to get a copy of the leader's code. For this example notebook,
I'm going to be collaborating with myself, swapping between my two repositories.
Make yourself a space to put it your work. (I will have two)


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
working_dir = os.path.join(git_dir, "git_example")
os.chdir(git_dir)
```


```bash
%%bash
pwd
rm -rf github-example # cleanup after previous example
rm -rf partner_dir # cleanup after previous example
```

    /home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git


Next, the collaborator needs to find out the URL of the repository: they should go to the leader's repository's GitHub page, and note the URL on the top of the screen.

As before, we're using `SSH` to connect - to do this you'll need to make sure the `ssh` button is pushed, and check that the URL begins with `git@github.com`.

Copy the URL into your clipboard by clicking on the icon to the right of the URL, and then:


```bash
%%bash
pwd
git clone git@github.com:alan-turing-institute/github-example.git partner_dir
```

    /home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git


    Cloning into 'partner_dir'...



```python
partner_dir = os.path.join(git_dir, "partner_dir")
os.chdir(partner_dir)
```


```bash
%%bash
pwd
ls
```

    /home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git/partner_dir
    lakeland.md
    test.md


Note that your partner's files are now present on your disk:


```bash
%%bash
cat lakeland.md
```

    Lakeland
    ========

    Cumbria has some pretty hills, and lakes too

    Mountains:
    * Helvellyn


## Nonconflicting changes

Now, both of you should make some changes. To start with, make changes to *different* files. This will mean your work doesn't "conflict". Later, we'll see how to deal with changes to a shared file.

Both of you should commit, but not push, your changes to your respective files:

E.g., the leader:


```python
os.chdir(working_dir)
```


```python
%%writefile Wales.md
Mountains In Wales
==================

* Tryfan
* Yr Wyddfa
```

    Writing Wales.md



```bash
%%bash
ls
```

    Wales.md
    __pycache__
    lakeland.md
    test.md
    wsd.py



```bash
%%bash
git add Wales.md
git commit -m "Add wales"
```

    [main 0c976b0] Add wales
     1 file changed, 5 insertions(+)
     create mode 100644 Wales.md


And the partner:


```python
os.chdir(partner_dir)
```


```python
%%writefile Scotland.md
Mountains In Scotland
==================

* Ben Eighe
* Cairngorm
```

    Writing Scotland.md



```bash
%%bash
ls
```

    Scotland.md
    lakeland.md
    test.md



```bash
%%bash
git add Scotland.md
git commit -m "Add Scotland"
```

    [main 289afed] Add Scotland
     1 file changed, 5 insertions(+)
     create mode 100644 Scotland.md


One of you should now push with `git push`:


```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       82b4fa0..289afed  main -> main


## Rejected push

The other should then attempt to push, but should receive an error message:


```python
os.chdir(working_dir)
```


```bash
%%bash
git push || echo "Push failed"
```

    Push failed


    To github.com:alan-turing-institute/github-example.git
     ! [rejected]        main -> main (fetch first)
    error: failed to push some refs to 'github.com:alan-turing-institute/github-example.git'
    hint: Updates were rejected because the remote contains work that you do
    hint: not have locally. This is usually caused by another repository pushing
    hint: to the same ref. You may want to first integrate the remote changes
    hint: (e.g., 'git pull ...') before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.


Do as it suggests:


```bash
%%bash
git pull
```

    Merge made by the 'recursive' strategy.
     Scotland.md | 5 +++++
     1 file changed, 5 insertions(+)
     create mode 100644 Scotland.md


    From github.com:alan-turing-institute/github-example
       82b4fa0..289afed  main       -> origin/main
     * [new branch]      experiment -> origin/experiment


## Merge commits

A window may pop up with a suggested default commit message. This commit is special: it is a *merge* commit. It is a commit which combines your collaborator's work with your own.

Now, push again with `git push`. This time it works. If you look on GitHub, you'll now see that it contains both sets of changes.


```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       289afed..34f8bbb  main -> main


The partner now needs to pull down that commit:


```python
os.chdir(partner_dir)
```


```bash
%%bash
git pull
```

    Updating 289afed..34f8bbb
    Fast-forward
     Wales.md | 5 +++++
     1 file changed, 5 insertions(+)
     create mode 100644 Wales.md


    From github.com:alan-turing-institute/github-example
       289afed..34f8bbb  main       -> origin/main



```bash
%%bash
ls
```

    Scotland.md
    Wales.md
    lakeland.md
    test.md


## Nonconflicted commits to the same file

Go through the whole process again, but this time, both of you should make changes to a single file, but make sure that you don't touch the same *line*. Again, the merge should work as before:


```python
%%writefile Wales.md
Mountains In Wales
==================

* Tryfan
* Snowdon
```

    Overwriting Wales.md



```bash
%%bash
git diff
```

    diff --git a/Wales.md b/Wales.md
    index f3e88b4..90f23ec 100644
    --- a/Wales.md
    +++ b/Wales.md
    @@ -2,4 +2,4 @@ Mountains In Wales
     ==================

     * Tryfan
    -* Yr Wyddfa
    +* Snowdon



```bash
%%bash
git commit -am "Translating from the Welsh"
```

    [main b8fb6c5] Translating from the Welsh
     1 file changed, 1 insertion(+), 1 deletion(-)



```bash
%%bash
git log --oneline
```

    b8fb6c5 Translating from the Welsh
    34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    289afed Add Scotland
    0c976b0 Add wales
    82b4fa0 Add Helvellyn
    6ff088f Include lakes in the scope
    d063119 Add lakeland
    c489aab Revert "Add a lie about a mountain"
    f79cacc Change title
    6e8a302 Add a lie about a mountain
    238eaff First commit of discourse on UK topography



```python
os.chdir(working_dir)
```


```python
%%writefile Wales.md
Mountains In Wales
==================

* Pen y Fan
* Tryfan
* Yr Wyddfa
```

    Overwriting Wales.md



```bash
%%bash
git commit -am "Add a beacon"
```

    [main 8cd684e] Add a beacon
     1 file changed, 1 insertion(+)



```bash
%%bash
git log --oneline
```

    8cd684e Add a beacon
    34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    289afed Add Scotland
    0c976b0 Add wales
    82b4fa0 Add Helvellyn
    6ff088f Include lakes in the scope
    d063119 Add lakeland
    c489aab Revert "Add a lie about a mountain"
    f79cacc Change title
    6e8a302 Add a lie about a mountain
    238eaff First commit of discourse on UK topography



```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       34f8bbb..8cd684e  main -> main


Switching back to the other partner...


```python
os.chdir(partner_dir)
```


```bash
%%bash
git push || echo "Push failed"
```

    Push failed


    To github.com:alan-turing-institute/github-example.git
     ! [rejected]        main -> main (fetch first)
    error: failed to push some refs to 'github.com:alan-turing-institute/github-example.git'
    hint: Updates were rejected because the remote contains work that you do
    hint: not have locally. This is usually caused by another repository pushing
    hint: to the same ref. You may want to first integrate the remote changes
    hint: (e.g., 'git pull ...') before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.



```bash
%%bash
git pull
```

    Auto-merging Wales.md
    Merge made by the 'recursive' strategy.
     Wales.md | 1 +
     1 file changed, 1 insertion(+)


    From github.com:alan-turing-institute/github-example
       34f8bbb..8cd684e  main       -> origin/main



```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       8cd684e..ecc3206  main -> main



```bash
%%bash
git log --oneline --graph
```

    *   ecc3206 Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 8cd684e Add a beacon
    * | b8fb6c5 Translating from the Welsh
    |/
    *   34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 289afed Add Scotland
    * | 0c976b0 Add wales
    |/
    * 82b4fa0 Add Helvellyn
    * 6ff088f Include lakes in the scope
    * d063119 Add lakeland
    * c489aab Revert "Add a lie about a mountain"
    * f79cacc Change title
    * 6e8a302 Add a lie about a mountain
    * 238eaff First commit of discourse on UK topography



```python
os.chdir(working_dir)
```


```bash
%%bash
git pull
```

    Updating 8cd684e..ecc3206
    Fast-forward
     Wales.md | 2 +-
     1 file changed, 1 insertion(+), 1 deletion(-)


    From github.com:alan-turing-institute/github-example
       8cd684e..ecc3206  main       -> origin/main



```bash
%%bash
git log --graph --oneline
```

    *   ecc3206 Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 8cd684e Add a beacon
    * | b8fb6c5 Translating from the Welsh
    |/
    *   34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 289afed Add Scotland
    * | 0c976b0 Add wales
    |/
    * 82b4fa0 Add Helvellyn
    * 6ff088f Include lakes in the scope
    * d063119 Add lakeland
    * c489aab Revert "Add a lie about a mountain"
    * f79cacc Change title
    * 6e8a302 Add a lie about a mountain
    * 238eaff First commit of discourse on UK topography



```python
message = """
participant Sue as S
participant "Sue's repo" as SR
participant "Shared remote" as M
participant "Jim's repo" as JR
participant Jim as J

note left of S: git clone
M->SR: fetch commits
SR->S: working directory as at latest commit

note left of S: edit Scotland.md
note right of J: edit Wales.md

note left of S: git commit -am "Add scotland"
S->SR: create commit with Scotland file

note right of J: git commit -am "Add wales"
J->JR: create commit with Wales file

note left of S: git push
SR->M: update remote with changes

note right of J: git push
JR-->M: !Rejected change

note right of J: git pull
M->JR: Pull in Sue's last commit, merge histories
JR->J: Add Scotland.md to working directory

note right of J: git push
JR->M: Transfer merged history to remote

"""
from wsd import wsd

%matplotlib inline
wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_04_collaboration_59_0.png)




## Conflicting commits

Finally, go through the process again, but this time, make changes which touch the same line.


```python
%%writefile Wales.md
Mountains In Wales
==================

* Pen y Fan
* Tryfan
* Snowdon
* Fan y Big
```

    Overwriting Wales.md



```bash
%%bash
git commit -am "Add another Beacon"
git push
```

    [main ed30178] Add another Beacon
     1 file changed, 1 insertion(+)


    To github.com:alan-turing-institute/github-example.git
       ecc3206..ed30178  main -> main



```python
os.chdir(partner_dir)
```


```python
%%writefile Wales.md
Mountains In Wales
==================

* Pen y Fan
* Tryfan
* Snowdon
* Glyder Fawr
```

    Overwriting Wales.md



```bash
%%bash
git commit -am "Add Glyder"
```

    [main bc04a83] Add Glyder
     1 file changed, 1 insertion(+)



```bash
%%bash
git push || echo "Push failed"
```

    Push failed


    To github.com:alan-turing-institute/github-example.git
     ! [rejected]        main -> main (fetch first)
    error: failed to push some refs to 'github.com:alan-turing-institute/github-example.git'
    hint: Updates were rejected because the remote contains work that you do
    hint: not have locally. This is usually caused by another repository pushing
    hint: to the same ref. You may want to first integrate the remote changes
    hint: (e.g., 'git pull ...') before pushing again.
    hint: See the 'Note about fast-forwards' in 'git push --help' for details.


When you pull, instead of offering an automatic merge commit message, it says:


```bash
%%bash
git pull || echo "Pull failed"
```

    Auto-merging Wales.md
    CONFLICT (content): Merge conflict in Wales.md
    Automatic merge failed; fix conflicts and then commit the result.
    Pull failed


    From github.com:alan-turing-institute/github-example
       ecc3206..ed30178  main       -> origin/main


## Resolving conflicts

Git couldn't work out how to merge the two different sets of changes.

You now need to manually resolve the conflict.

It has marked the conflicted area:


```bash
%%bash
cat Wales.md
```

    Mountains In Wales
    ==================

    * Pen y Fan
    * Tryfan
    * Snowdon
    <<<<<<< HEAD
    * Glyder Fawr
    =======
    * Fan y Big
    >>>>>>> ed301786b17defffe617ed8c7ded6591a7fb94f0


Manually edit the file, to combine the changes as seems sensible and get rid of the symbols:


```python
%%writefile Wales.md
Mountains In Wales
==================

* Pen y Fan
* Tryfan
* Snowdon
* Fan y Big
* Glyder Fawr
```

    Overwriting Wales.md


## Commit the resolved file

Now commit the merged result:


```bash
%%bash
git commit -a --no-edit # I added a No-edit for this non-interactive session. You can edit the commit if you like.
```

    [main 85b2797] Merge branch 'main' of github.com:alan-turing-institute/github-example



```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       ed30178..85b2797  main -> main



```python
os.chdir(working_dir)
```


```bash
%%bash
git pull
```

    Updating ed30178..85b2797
    Fast-forward
     Wales.md | 1 +
     1 file changed, 1 insertion(+)


    From github.com:alan-turing-institute/github-example
       ed30178..85b2797  main       -> origin/main



```bash
%%bash
cat Wales.md
```

    Mountains In Wales
    ==================

    * Pen y Fan
    * Tryfan
    * Snowdon
    * Fan y Big
    * Glyder Fawr



```bash
%%bash
git log --oneline --graph
```

    *   85b2797 Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * ed30178 Add another Beacon
    * | bc04a83 Add Glyder
    |/
    *   ecc3206 Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 8cd684e Add a beacon
    * | b8fb6c5 Translating from the Welsh
    |/
    *   34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 289afed Add Scotland
    * | 0c976b0 Add wales
    |/
    * 82b4fa0 Add Helvellyn
    * 6ff088f Include lakes in the scope
    * d063119 Add lakeland
    * c489aab Revert "Add a lie about a mountain"
    * f79cacc Change title
    * 6e8a302 Add a lie about a mountain
    * 238eaff First commit of discourse on UK topography


## Distributed VCS in teams with conflicts


```python
message = """
participant Sue as S
participant "Sue's repo" as SR
participant "Shared remote" as M
participant "Jim's repo" as JR
participant Jim as J

note left of S: edit the same line in wales.md
note right of J: edit the same line in wales.md

note left of S: git commit -am "update wales.md"
S->SR: add commit to local repo

note right of J: git commit -am "update wales.md"
J->JR: add commit to local repo

note left of S: git push
SR->M: transfer commit to remote

note right of J: git push
JR->M: !Rejected

note right of J: git pull
M->J: Make conflicted file with conflict markers

note right of J: edit file to resolve conflicts
note right of J: git add wales.md
note right of J: git commit
J->JR: Mark conflict as resolved

note right of J: git push
JR->M: Transfer merged history to remote

note left of S: git pull
M->SR: Download Jim's resolution of conflict.

"""

wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_04_collaboration_81_0.png)




# The Levels of Git


```python
message = """
Working Directory -> Staging Area : git add
Staging Area -> Local Repository : git commit
Local Repository -> Local Repository : git commit -a
Local Repository -> Working Directory : git checkout
Local Repository -> Staging Area : git reset
Local Repository -> Working Directory: git reset --hard
Local Repository -> Remote Repository : git push
Remote Repository -> Local Repository : git fetch
Local Repository -> Working Directory : git merge
Remote Repository -> Working Directory: git pull
"""

wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_04_collaboration_83_0.png)




## Editing directly on GitHub

Note that you can also make changes in the GitHub website itself. Visit one of your files, and hit "edit".

Make a change in the edit window, and add an appropriate commit message.

That change now appears on the website, but not in your local copy. (Verify this).

Now pull, and check the change is now present on your local version.

## GitHub as a social network

In addition to being a repository for code, and a way to publish code, GitHub is a social network.

You can follow the public work of other coders: go to the profile of your collaborator in your browser, and hit the "follow" button.

[Here's mine](https://github.com/jamespjh) : if you want to you can follow me.

Using GitHub to build up a good public profile of software projects you've worked on is great for your CV!
