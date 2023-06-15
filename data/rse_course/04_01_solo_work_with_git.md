# 4.1 Solo work with git

*Estimated time to complete this notebook: 15 minutes*

## 4.1.1 Getting started

So, we're in our git working directory:


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
working_dir = os.path.join(git_dir, "git_example")
os.chdir(working_dir)
working_dir
```




    '/home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git/git_example'



### A first example file

So let's create an example file, and see how to start to manage a history of changes to it.

    <my editor> test.md # Type some content into the file.


```python
%%writefile test.md
Mountains in the UK
===================
England is not very mountainous.
But has some tall hills, and maybe a mountain or two depending on your definition.

```

    Writing test.md



```python
cat test.md
```

    Mountains in the UK
    ===================
    England is not very mountainous.
    But has some tall hills, and maybe a mountain or two depending on your definition.


### Telling Git about the File

So, let's tell Git that `test.md` is a file which is important, and we would like to keep track of its history:


```bash
%%bash
git add test.md
```

Don't forget: Any files in repositories which you want to "track" need to be added with `git add` after you create them.

### Our first commit

Now, we need to tell Git to record the first version of this file in the history of changes:


```bash
%%bash
git commit -m "First commit of discourse on UK topography"
```

    [main (root-commit) 238eaff] First commit of discourse on UK topography
     1 file changed, 4 insertions(+)
     create mode 100644 test.md


And note the confirmation from Git.

There's a lot of output there you can ignore for now.

### Configuring Git with your editor

If you don't type in the log message directly with -m "Some message", then an editor will pop up, to allow you
to edit your message on the fly.

For this to work, you have to tell git where to find your editor.

```bash
git config --global core.editor vim
```

You can find out what you currently have with:
```bash
git config --get core.editor
```

To configure `Notepad++` on Windows you'll need something like the below, ask a demonstrator if you need help:

```bash
git config --global core.editor "'C:/Program Files (x86)/Notepad++/notepad++.exe' -multiInst -nosession -noPlugin"
```

I'm going to be using `vim` as my editor, but you can use whatever editor you prefer. (Windows users could use `Notepad++`, Mac users could use `textmate` or `Sublime Text`, Linux users could use `vim`, `nano` or `emacs`.)

## 4.1.2 Commit logs

### Git log

Git now has one change in its history:


```bash
%%bash
git log
```

    commit 238eaff15e2769e0ef1d989f1a2e8be1873fa0ab
    Author: Turing Developer <developer@example.com>
    Date:   Mon Nov 8 13:59:33 2021 +0000

        First commit of discourse on UK topography


You can see the commit message, author, and date...

### Hash Codes

The commit "hash code", e.g.

`238eaff15e2769e0ef1d989f1a2e8be1873fa0ab`

is a unique identifier of that particular revision.

This is a really long code, but whenever you need to use it, you can just use the first few characters.
You just need however many characters is long enough to make it unique, for example `238eaff1`.

### Nothing to see here

Note that git will now tell us that our "working directory" is up-to-date with the repository: there are no changes to the files that aren't recorded in the repository history:


```bash
%%bash
git status
```

    On branch main
    nothing to commit, working tree clean


## 4.1.3 Staging changes

Let's edit the file again:

    vim test.md


```python
%%writefile test.md
Mountains in the UK
===================
England is not very mountainous.
But has some tall hills, and maybe a mountain or two depending on your definition.

Mount Fictional, in Barsetshire, U.K. is the tallest mountain in the world.

```

    Overwriting test.md



```python
cat test.md
```

    Mountains in the UK
    ===================
    England is not very mountainous.
    But has some tall hills, and maybe a mountain or two depending on your definition.

    Mount Fictional, in Barsetshire, U.K. is the tallest mountain in the world.


### Unstaged changes


```bash
%%bash
git status
```

    On branch main
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git restore <file>..." to discard changes in working directory)
    	modified:   test.md

    no changes added to commit (use "git add" and/or "git commit -a")


We can now see that there is a change to "test.md" which is currently "not staged for commit".
What does this mean?

If we do a `git commit` now *nothing will happen*.

Git will only commit changes to files that you choose to include in each commit.

This is a difference from other version control systems, where committing will affect all changed files.

We can see the differences in the file with:


```bash
%%bash
git diff
```

    diff --git a/test.md b/test.md
    index a1f85df..3a2f7b0 100644
    --- a/test.md
    +++ b/test.md
    @@ -2,3 +2,5 @@ Mountains in the UK
     ===================
     England is not very mountainous.
     But has some tall hills, and maybe a mountain or two depending on your definition.
    +
    +Mount Fictional, in Barsetshire, U.K. is the tallest mountain in the world.


Deleted lines are prefixed with a minus, added lines prefixed with a plus.

### Staging a file to be included in the next commit

To include the file in the next commit, we have a few choices. This is one of the things to be careful of with git: there are lots of ways to do similar things, and it can be hard to keep track of them all.


```bash
%%bash
git add --update
```

This says "include in the next commit, all files which have ever been included before".

Note that `git add` is the command we use to introduce git to a new file, but also the command we use to "stage" a file to be included in the next commit.

### The staging area

The "staging area" or "index" is the git jargon for the place which contains the list of changes which will be included in the next commit.

You can include specific changes to specific files with `git add`, commit them, add some more files, and commit them. (You can even add specific changes within a file to be included in the index.)

## 4.1.4 Visualising changes

### Message Sequence Charts

In order to illustrate the behaviour of Git, it will be useful to be able to generate figures in Python
of a "message sequence chart" flavour.

There's a nice online tool to do this, called "Message Sequence Charts".

Have a look at https://www.websequencediagrams.com

Instead of just showing you these diagrams, I'm showing you in this notebook how I make them.
This is part of our "reproducible computing" approach; always generating all our figures from code.

Here's some quick code in the Notebook to download and display an MSC illustration, using the Web Sequence Diagrams API:


```python
%%writefile wsd.py
import requests
import re
import IPython


def wsd(code):
    response = requests.post(
        "http://www.websequencediagrams.com/index.php",
        data={
            "message": code,
            "apiVersion": 1,
        },
    )
    expr = re.compile("(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
    m = expr.search(response.text)
    if m == None:
        print("Invalid response from server.")
        return False

    image = requests.get("http://www.websequencediagrams.com/" + m.group(0))
    return IPython.core.display.Image(image.content)
```

    Writing wsd.py



```python
%matplotlib inline
from wsd import wsd

wsd("Sender->Recipient: Hello\n Recipient->Sender: Message received OK")
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_01_solo_work_with_git_50_0.png)




### The Levels of Git

Let's make ourselves a sequence chart to show the different aspects of Git we've seen so far:


```python
message = """
Working Directory -> Staging Area : git add
Staging Area -> Local Repository : git commit
Working Directory -> Local Repository : git commit -a
"""
wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_01_solo_work_with_git_53_0.png)




## 4.1.6 Correcting mistakes

### Review of status


```bash
%%bash
git status
```

    On branch main
    Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
    	modified:   test.md

    Untracked files:
      (use "git add <file>..." to include in what will be committed)
    	__pycache__/
    	wsd.py




```bash
%%bash
git commit -m "Add a lie about a mountain"
```

    [main 6e8a302] Add a lie about a mountain
     1 file changed, 2 insertions(+)



```bash
%%bash
git log
```

    commit 6e8a302387007780675dbd5cb1823901d1a7b59b
    Author: Turing Developer <developer@example.com>
    Date:   Mon Nov 8 13:59:37 2021 +0000

        Add a lie about a mountain

    commit 238eaff15e2769e0ef1d989f1a2e8be1873fa0ab
    Author: Turing Developer <developer@example.com>
    Date:   Mon Nov 8 13:59:33 2021 +0000

        First commit of discourse on UK topography


Great, we now have a file which contains a mistake.

### Carry on regardless

In a while, we'll use Git to roll back to the last correct version: this is one of the main reasons we wanted to use version control, after all! But for now, let's do just as we would if we were writing code, not notice our mistake and keep working...

```bash
vim test.md
```


```python
%%writefile test.md
Mountains and Hills in the UK
===================
England is not very mountainous.
But has some tall hills, and maybe a mountain or two depending on your definition.

Mount Fictional, in Barsetshire, U.K. is the tallest mountain in the world.

```

    Overwriting test.md



```python
cat test.md
```

    Mountains and Hills in the UK
    ===================
    England is not very mountainous.
    But has some tall hills, and maybe a mountain or two depending on your definition.

    Mount Fictional, in Barsetshire, U.K. is the tallest mountain in the world.


### Commit with a built-in-add


```bash
%%bash
git commit -am "Change title"
```

    [main f79cacc] Change title
     1 file changed, 1 insertion(+), 1 deletion(-)


This last command, `git commit -a` automatically adds changes to all tracked files to the staging area, as part of the commit command. So, if you never want to just add changes to some tracked files but not others, you can just use this and forget about the staging area!

### Review of changes


```bash
%%bash
git log | head
```

    commit f79cacc17500651a228f9b5a1922c3b50ea723c3
    Author: Turing Developer <developer@example.com>
    Date:   Mon Nov 8 13:59:38 2021 +0000

        Change title

    commit 6e8a302387007780675dbd5cb1823901d1a7b59b
    Author: Turing Developer <developer@example.com>
    Date:   Mon Nov 8 13:59:37 2021 +0000



We now have three changes in the history:


```bash
%%bash
git log --oneline
```

    f79cacc Change title
    6e8a302 Add a lie about a mountain
    238eaff First commit of discourse on UK topography


## Git Solo Workflow

We can make a diagram that summarises the above story:


```python
message = """
participant "Jim's repo" as R
participant "Jim's index" as I
participant Jim as J

note right of J: vim test.md

note right of J: git init
J->R: create

note right of J: git add test.md

J->I: Add content of test.md

note right of J: git commit
I->R: Commit content of test.md

note right of J:  vim test.md

note right of J: git add --update
J->I: Add content of test.md
note right of J: git commit -m "Add a lie"
I->R: Commit change to test.md

note right of J:  vim test.md
note right of J: git commit -am "Change title"
J->R: Add and commit change to test.md (and all tracked files)
"""
wsd(message)
```





![png](/Users/lbokeria/Documents/hack_week_2023/reginald/data_processing/rse_course_modules/module04_version_control_with_git/04_01_solo_work_with_git_73_0.png)
