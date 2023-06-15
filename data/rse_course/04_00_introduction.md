# 4.0 Introduction to version control

*Estimated time to complete this notebook: 10 minutes*

## What's version control?

Version control is a tool for __managing changes__ to a set of files.

There are many different __version control systems__:

- Git
- Mercurial (`hg`)
- CVS
- Subversion (`svn`)
- ...

## Why use version control?

- Better kind of __backup__.
- Review __history__ ("When did I introduce this bug?").
- Restore older __code versions__.
- Ability to __undo mistakes__.
- Maintain __several versions__ of the code at a time.

Git is also a __collaborative__ tool:

- "How can I share my code?"
- "How can I submit a change to someone else's code?"
- "How can I merge my work with Sue's?"

## Git != GitHub

- __Git__: version control system tool to manage source code history.
- __GitHub__: hosting service for Git repositories.

## How do we use version control?

Do some programming, then commit our work:

`my_vcs commit`

Program some more.

Spot a mistake:

`my_vcs rollback`

Mistake is undone.

## What is version control? (Team version)

Sue                | James
------------------ |------
`my_vcs commit`    | ...
...                | Join the team
...                | `my_vcs checkout`
...                | Do some programming
...                | `my_vcs commit`
`my_vcs update`    | ...
Do some programming|Do some programming
`my_vcs commit`    | ...
`my_vcs update`    | ...
`my_vcs merge`     | ...
`my_vcs commit`    | ...

## Scope

This course will use the `git` version control system, but much of what you learn will be valid with other version control tools you may encounter, including subversion (`svn`) and mercurial (`hg`).

# 4.0.1 Practising with Git

## Example Exercise

In this course, we will use, as an example, the development of a few text files containing a description of a topic of your choice.

This could be your research, a hobby, or something else. In the end, we will show you how to display the content of these files as a very simple website.

## Programming and documents

The purpose of this exercise is to learn how to use Git to manage program code you write, not simple text website content, but we'll just use these text files instead of code for now, so as not to confuse matters with trying to learn version control while thinking about programming too.

In later parts of the course, you will use the version control tools you learn today with actual Python code.

## Markdown

The text files we create will use a simple "wiki" markup style called [markdown](http://daringfireball.net/projects/markdown/basics) to show formatting.
This is the convention used in this file, too.

You can view the content of this file in the way Markdown renders it by looking on the [web](https://alan-turing-institute.github.io/rse-course/html/module04_version_control_with_git/04_00_introduction.html), and compare the [raw text](https://raw.githubusercontent.com/alan-turing-institute/rse-course/main/module04_version_control_with_git/04_00_introduction.ipynb).

## Displaying Text in this Tutorial

This tutorial is based on use of the Git command line. So you'll be typing commands in the shell.

To make it easy for me to edit, I've built it using Jupyter notebook.

Commands you can type will look like this, using the %%bash "magic" for the notebook.

If you are running the notebook on windows you'll have to use %%cmd.


```bash
%%bash
echo some output
```

    some output


with the results you should see below.

In this document, we will show the new content of an edited document like this:


```python
%%writefile somefile.md
Some content here
```

    Overwriting somefile.md


But if you are following along, you should edit the file using a [text editor](https://alan-turing-institute.github.io/rse-course/html/course_prerequisites/03_editor.html).

## Setting up somewhere to work


```bash
%%bash
rm -rf learning_git/git_example # Just in case it's left over from a previous class; you won't need this
mkdir -p learning_git/git_example
cd learning_git/git_example
```

I just need to move this Jupyter notebook's current directory as well:


```python
import os

top_dir = os.getcwd()
top_dir
```




    '/home/turingdev/research-software/rse-course/module04_version_control_with_git'




```python
git_dir = os.path.join(top_dir, "learning_git")
git_dir
```




    '/home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git'




```python
working_dir = os.path.join(git_dir, "git_example")
```


```python
os.chdir(working_dir)
```

# 4.0.2 Solo work

## Configuring Git with your name and email

First, we should configure Git to know our name and email address:

```bash
git config --global user.name "YOUR NAME HERE"
git config --global user.email "yourname@example.com"
```

Note that by using the `--global` flag, we are setting these options for all projects. To set them just for this project, use `--local` instead.

Now check that this worked


```bash
%%bash
git config --get user.name
```

    Turing Developer



```bash
%%bash
git config --get user.email
```

    developer@example.com


## Initialising the repository

Now, we will tell Git to track the content of this folder as a git "repository".


```bash
%%bash
pwd # Note where we are standing-- MAKE SURE YOU INITIALISE THE RIGHT FOLDER
git init --initial-branch=main
```

    /home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git/git_example
    Initialized empty Git repository in /home/turingdev/research-software/rse-course/module04_version_control_with_git/learning_git/git_example/.git/


As yet, this repository contains no files:


```bash
%%bash
ls
```


```bash
%%bash
git status
```

    On branch main

    No commits yet

    nothing to commit (create/copy files and use "git add" to track)
