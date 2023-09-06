# 4.3 Publishing

*Estimated time to complete this notebook: 15 minutes*

We're still in our working directory:


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
working_dir = os.path.join(git_dir, "git_example")
os.chdir(working_dir)
working_dir
```




    '/home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git/git_example'



## Sharing your work

So far, all our work has been on our own computer.
But a big part of the point of version control is keeping your work safe, on remote servers.
Another part is making it easy to share your work with the world.
In this example, we'll be using the `GitHub` cloud repository to store and publish our work.

If you have not done so already, you should create an account on `GitHub`: go to [https://github.com/](https://github.com/), fill in a username and password, and click on "sign up for free".

## Creating a repository

Ok, let's create a repository to store our work. Hit "new repository" on the right of the github home screen, or click [here](https://github.com/new).

- Fill in a short name, and a description.
- Choose a "public" repository.
- Don't choose to add a README.

## GitHub private repositories

For this course, you should use public repositories in your personal account for your example work: it's good to share! GitHub is free for open source, but in general, charges a fee if you want to keep your work private.

In the future, you might want to keep your work on GitHub private.

Students can get free private repositories on GitHub, by going to [GitHub Education](https://github.com/edu) and filling in a form (look for the Student Developer Pack).

## Adding a new remote to your repository

Instructions will appear, once you've created the repository, as to how to add this new "remote" server to your repository.
In this example we are using pre-authorised `Deploy Keys` to connect using the `SSH` method.
If you prefer to use username and password/token, these instructions will be slightly different:


```bash
%%bash
git remote add origin git@github.com:alan-turing-institute/github-example.git
```

Note that the `https` version of this instruction would be something like `git remote add origin https://${YOUR_USERNAME}:${GITHUB_TOKEN}@github.com/alan-turing-institute/github-example.git`


```bash
%%bash
git remote -v
```

    origin	git@github.com:alan-turing-institute/github-example.git (fetch)
    origin	git@github.com:alan-turing-institute/github-example.git (push)



```bash
%%bash
git push -uf origin main # Note we use the '-f' flag here to force an update
```

    Branch 'main' set up to track remote branch 'main' from 'origin'.


    To github.com:alan-turing-institute/github-example.git
     + d358baa...c489aab main -> main (forced update)


## Remotes

The first command sets up the server as a new `remote`, called `origin`.

Git, unlike some earlier version control systems is a "distributed" version control system, which means you can work with multiple remote servers.

Usually, commands that work with remotes allow you to specify the remote to use, but assume the `origin` remote if you don't.

Here, `git push` will push your whole history onto the server, and now you'll be able to see it on the internet! Refresh your web browser where the instructions were, and you'll see your repository!

Let's add these commands to our diagram:


```python
message = """
Working Directory -> Staging Area : git add
Staging Area -> Local Repository : git commit
Working Directory -> Local Repository : git commit -a
Local Repository -> Working Directory : git checkout
Local Repository -> Staging Area : git reset
Local Repository -> Working Directory: git reset --hard
Local Repository -> Remote Repository : git push
"""
from wsd import wsd

%matplotlib inline
wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_03_publishing_15_0.png)




## Playing with GitHub

Take a few moments to click around and work your way through the GitHub interface. Try clicking on 'test.md' to see the content of the file: notice how the markdown renders prettily.

Click on "commits" near the top of the screen, to see all the changes you've made. Click on the commit number next to the right of a change, to see what changes it includes: removals are shown in red, and additions in green.

# Working with multiple files

## Some new content

So far, we've only worked with one file. Let's add another:

``` bash
vim lakeland.md
```


```python
%%writefile lakeland.md
Lakeland
========

Cumbria has some pretty hills, and lakes too.
```

    Writing lakeland.md



```python
cat lakeland.md
```

    Lakeland
    ========

    Cumbria has some pretty hills, and lakes too.


## Git will not by default commit your new file


```bash
%%bash
git commit -am "Try to add Lakeland" || echo "Commit failed"
```

    On branch main
    Your branch is up to date with 'origin/main'.

    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    	__pycache__/
    	lakeland.md
    	wsd.py

    nothing added to commit but untracked files present (use "git add" to track)
    Commit failed


This failed, because we've not told git to track the new file yet.

## Tell git about the new file


```bash
%%bash
git add lakeland.md
git commit -am "Add lakeland"
```

    [main d063119] Add lakeland
     1 file changed, 4 insertions(+)
     create mode 100644 lakeland.md


Ok, now we have added the change about Cumbria to the file. Let's publish it to the origin repository.


```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       c489aab..d063119  main -> main


Visit GitHub, and notice this change is on your repository on the server. We could have said `git push origin` to specify the remote to use, but origin is the default.

# Changing two files at once

What if we change both files?


```python
%%writefile lakeland.md
Lakeland
========

Cumbria has some pretty hills, and lakes too

Mountains:
* Helvellyn
```

    Overwriting lakeland.md



```python
%%writefile test.md
Mountains and Lakes in the UK
===================
Engerland is not very mountainous.
But has some tall hills, and maybe a
mountain or two depending on your definition.
```

    Overwriting test.md



```bash
%%bash
git status
```

    On branch main
    Your branch is up to date with 'origin/main'.

    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git restore <file>..." to discard changes in working directory)
    	modified:   lakeland.md
    	modified:   test.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    	__pycache__/
    	wsd.py

    no changes added to commit (use "git add" and/or "git commit -a")


These changes should really be separate commits. We can do this with careful use of git add, to **stage** first one commit, then the other.


```bash
%%bash
git add test.md
git commit -m "Include lakes in the scope"
```

    [main 6ff088f] Include lakes in the scope
     1 file changed, 4 insertions(+), 3 deletions(-)


Because we "staged" only test.md, the changes to lakeland.md were not included in that commit.


```bash
%%bash
git commit -am "Add Helvellyn"
```

    [main 82b4fa0] Add Helvellyn
     1 file changed, 4 insertions(+), 1 deletion(-)



```bash
%%bash
git log --oneline
```

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
       d063119..82b4fa0  main -> main



```python
message = """
participant "Jim's remote" as M
participant "Jim's repo" as R
participant "Jim's index" as I
participant Jim as J

note right of J: vim test.md
note right of J: vim lakeland.md

note right of J: git add test.md
J->I: Add *only* the changes to test.md to the staging area

note right of J: git commit -m "Include lakes"
I->R: Make a commit from currently staged changes: test.md only

note right of J: git commit -am "Add Helvellyn"
J->I: Stage *all remaining* changes, (lakeland.md)
I->R: Make a commit from currently staged changes

note right of J: git push
R->M: Transfer commits to Github
"""
wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_03_publishing_41_0.png)
