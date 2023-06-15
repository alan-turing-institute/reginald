# 4.7 Branches

*Estimated time to complete this notebook: 10 minutes*

Branches are incredibly important to why `git` is cool and powerful.

They are an easy and cheap way of making a second version of your software, which you work on in parallel,
and pull in your changes when you are ready.


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
working_dir = os.path.join(git_dir, "git_example")
os.chdir(working_dir)
```


```bash
%%bash
git branch # Tell me what branches exist
```

    * main



```bash
%%bash
git checkout -b experiment # Make a new branch
```

    Switched to a new branch 'experiment'



```bash
%%bash
git branch
```

    * experiment
      main



```python
%%writefile Wales.md
Mountains In Wales
==================

* Pen y Fan
* Tryfan
* Snowdon
* Glyder Fawr
* Fan y Big
* Cadair Idris
```

    Overwriting Wales.md



```bash
%%bash
git commit -am "Add Cadair Idris"
```

    [experiment a4378e5] Add Cadair Idris
     1 file changed, 2 insertions(+), 1 deletion(-)



```bash
%%bash
git checkout main # Switch to an existing branch
```

    Your branch is up to date with 'origin/main'.


    Switched to branch 'main'



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
git checkout experiment
```

    Switched to branch 'experiment'



```python
cat Wales.md
```

    Mountains In Wales
    ==================

    * Pen y Fan
    * Tryfan
    * Snowdon
    * Glyder Fawr
    * Fan y Big
    * Cadair Idris


## Publishing branches

To let the server know there's a new branch use:


```bash
%%bash
git push -u origin experiment
```

    Branch 'experiment' set up to track remote branch 'experiment' from 'origin'.


    remote:
    remote: Create a pull request for 'experiment' on GitHub by visiting:
    remote:      https://github.com/alan-turing-institute/github-example/pull/new/experiment
    remote:
    To github.com:alan-turing-institute/github-example.git
     * [new branch]      experiment -> experiment


We use `--set-upstream origin` (Abbreviation `-u`) to tell git that this branch should be pushed to and pulled from origin per default.

If you are following along, you should be able to see your branch in the list of branches in GitHub.

Once you've used `git push -u` once, you can push new changes to the branch with just a git push.

If others checkout your repository, they will be able to do `git checkout experiment` to see your branch content,
and collaborate with you **in the branch**.


```bash
%%bash
git branch -r
```

      origin/experiment
      origin/main


Local branches can be, but do not have to be, connected to remote branches
They are said to "track" remote branches. `push -u` sets up the tracking relationship.
You can see the remote branch for each of your local branches if you ask for "verbose" output from `git branch`:


```bash
%%bash
git branch -vv
```

    * experiment a4378e5 [origin/experiment] Add Cadair Idris
      main       85b2797 [origin/main] Merge branch 'main' of github.com:alan-turing-institute/github-example


### Find out what is on a branch

In addition to using `git diff` to compare to the state of a branch,
you can use `git log` to look at lists of commits which are in a branch
and haven't been merged yet.


```bash
%%bash
git log main..experiment
```

    commit a4378e56a723f2ba662262f94108a74be5f896f0
    Author: Turing Developer <developer@example.com>
    Date:   Mon Nov 8 14:06:02 2021 +0000

        Add Cadair Idris


Git uses various symbols to refer to sets of commits.
The double dot `A..B` means "ancestor of B and not ancestor of A"

So in a purely linear sequence, it does what you'd expect.


```bash
%%bash
git log --graph --oneline HEAD~9..HEAD~5
```

    *   34f8bbb Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 289afed Add Scotland
    * | 0c976b0 Add wales
    |/
    * 82b4fa0 Add Helvellyn
    * 6ff088f Include lakes in the scope


But in cases where a history has branches,
the definition in terms of ancestors is important.


```bash
%%bash
git log --graph --oneline HEAD~5..HEAD
```

    * a4378e5 Add Cadair Idris
    *   85b2797 Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * ed30178 Add another Beacon
    * | bc04a83 Add Glyder
    |/
    *   ecc3206 Merge branch 'main' of github.com:alan-turing-institute/github-example
    |\
    | * 8cd684e Add a beacon
    * b8fb6c5 Translating from the Welsh


If there are changes on both sides, like this:


```bash
%%bash
git checkout main
```

    Your branch is up to date with 'origin/main'.


    Switched to branch 'main'



```python
%%writefile Scotland.md
Mountains In Scotland
==================

* Ben Eighe
* Cairngorm
* Aonach Eagach

```

    Overwriting Scotland.md



```bash
%%bash
git diff Scotland.md
```

    diff --git a/Scotland.md b/Scotland.md
    index 9613dda..bf5c643 100644
    --- a/Scotland.md
    +++ b/Scotland.md
    @@ -3,3 +3,4 @@ Mountains In Scotland

     * Ben Eighe
     * Cairngorm
    +* Aonach Eagach



```bash
%%bash
git commit -am "Commit Aonach onto main branch"
```

    [main 537950c] Commit Aonach onto main branch
     1 file changed, 1 insertion(+)


Then this notation is useful to show the content of what's on what branch:


```bash
%%bash
git log --left-right --oneline main...experiment
```

    < 537950c Commit Aonach onto main branch
    > a4378e5 Add Cadair Idris


Three dots means "everything which is not a common ancestor" of the two commits, i.e. the differences between them.

## Merging branches

We can merge branches, and just as we would pull in remote changes, there may or may not be conflicts.


```bash
%%bash
git branch
git merge experiment
```

      experiment
    * main
    Merge made by the 'recursive' strategy.
     Wales.md | 3 ++-
     1 file changed, 2 insertions(+), 1 deletion(-)



```bash
%%bash
git log --graph --oneline HEAD~3..HEAD
```

    *   2365c66 Merge branch 'experiment'
    |\
    | * a4378e5 Add Cadair Idris
    * | 537950c Commit Aonach onto main branch
    |/
    * 85b2797 Merge branch 'main' of github.com:alan-turing-institute/github-example
    * ed30178 Add another Beacon


## Cleaning up after a branch


```bash
%%bash
git branch  # list branches
```

      experiment
    * main



```bash
%%bash
git branch -d experiment  # delete a branch
```

    Deleted branch experiment (was a4378e5).



```bash
%%bash
git branch # current branch
```

    * main



```bash
%%bash
git branch --remote  # list remote branches
```

      origin/experiment
      origin/main



```bash
%%bash
git push --delete origin experiment
# Remove remote branch. Note that you can also use the GitHub interface to do this.
```

    To github.com:alan-turing-institute/github-example.git
     - [deleted]         experiment



```bash
%%bash
git branch --remote  # list remote branches
```

      origin/main



```bash
%%bash
git push
```

    To github.com:alan-turing-institute/github-example.git
       85b2797..2365c66  main -> main


```bash
%%bash
git branch  # current branch
```

    * main 2365c66 [origin/main] Merge branch 'experiment'


## A good branch strategy

* A `production` or `main` branch: the current working version of your code
* A `develop` branch: where new code can be tested
* `feature` branches: for specific new ideas
* `release` branches: when you share code with others
  * Useful for applying bug fixes to older versions of your code

## Grab changes from a branch

Make some changes on one branch, switch back to another, and use:

```bash
git checkout <branch> <path>
```

to quickly grab a file from one branch into another. This will create a copy of the file as it exists in `<branch>` into your current branch, overwriting it if it already existed.
For example, if you have been experimenting in a new branch but want to undo all your changes to a particular file (that is, restore the file to its version in the `main` branch), you can do that with:

```
git checkout main test_file
```

Using `git checkout` with a path takes the content of files.
To grab the content of a specific *commit* from another branch,
and apply it as a patch to your branch, use:

``` bash
git cherry-pick <commit>
```
