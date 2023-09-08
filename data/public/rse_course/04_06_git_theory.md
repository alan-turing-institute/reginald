# 4.6 Git Theory

*Estimated time to complete this notebook: 5 minutes*


## The revision Graph

Revisions form a **GRAPH**


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
working_dir = os.path.join(git_dir, "git_example")
os.chdir(working_dir)
```


```bash
%%bash
git log --graph --oneline
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


## Git concepts

* Each revision has a parent that it is based on
* These revisions form a graph
* Each revision has a unique hash code
  * In Sue's copy, revision 43 is ab3578d6
  * Jim might think that is revision 38, but it's still ab3579d6
* Branches, tags, and HEAD are *labels* pointing at revisions
* Some operations (like fast forward merges) just move labels.

## The levels of Git

There are four **Separate** levels a change can reach in git:

* The Working Copy
* The **index** (aka **staging area**)
* The local repository
* The remote repository

Understanding all the things `git reset` can do requires a good
grasp of git theory.

* `git reset <commit> <filename>` : Reset index and working version of that file to the version in a given commit
* `git reset --soft <commit>`: Move local repository branch label to that commit, leave working dir and index unchanged
* `git reset <commit>`: Move local repository and index to commit ("--mixed")
* `git reset --hard <commit>`: Move local repostiory, index, and working directory copy to that state
