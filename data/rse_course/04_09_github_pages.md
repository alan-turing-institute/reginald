# 4.9 Publishing from GitHub

*Estimated time to complete this notebook: 5 minutes*

# GitHub pages

## Yaml Frontmatter

GitHub will publish repositories containing markdown as web pages, automatically.

You'll need to add this content:

> ```
>    ---
>    ---
> ```

A pair of lines with three dashes, to the top of each markdown file. This is how GitHub knows which markdown files to make into web pages.
[Here's why](https://jekyllrb.com/docs/front-matter/) for the curious.


```python
%%writefile test.md
---
title: Github Pages Example
---
Mountains and Lakes in the UK
===================

Engerland is not very mountainous.
But has some tall hills, and maybe a mountain or two depending on your definition.
```

    Overwriting test.md



```bash
%%bash
git commit -am "Add github pages YAML frontmatter"
```

    [main 12ee6ad] Add github pages YAML frontmatter
     1 file changed, 7 insertions(+), 4 deletions(-)


## The gh-pages branch

GitHub creates github pages when you use a special named branch.
By default this is `gh-pages` although you can change it to something else if you prefer.
This is best used to create documentation for a program you write, but you can use it for anything.


```python
os.chdir(working_dir)
```


```bash
%%bash

git checkout -b gh-pages
git push -uf origin gh-pages
```

    Branch 'gh-pages' set up to track remote branch 'gh-pages' from 'origin'.


    Switched to a new branch 'gh-pages'
    remote:
    remote: Create a pull request for 'gh-pages' on GitHub by visiting:
    remote:      https://github.com/alan-turing-institute/github-example/pull/new/gh-pages
    remote:
    To github.com:alan-turing-institute/github-example.git
     * [new branch]      gh-pages -> gh-pages


The first time you do this, GitHub takes a few minutes to generate your pages.

The website will appear at `http://username.github.io/repositoryname`, for example:

http://alan-turing-institute.github.io/github-example/

## Layout for GitHub pages

You can use GitHub pages to make HTML layouts, here's an [example of how to do it](http://github.com/UCL/ucl-github-pages-example), and [how it looks](http://ucl.github.io/ucl-github-pages-example). We won't go into the detail of this now, but after the class, you might want to try this.


```bash
%%bash
# Cleanup by removing the gh-pages branch
git checkout main
git push
git branch -d gh-pages
git push --delete origin gh-pages
git branch --remote
```

    Your branch is ahead of 'origin/main' by 1 commit.
      (use "git push" to publish your local commits)
    Deleted branch gh-pages (was 12ee6ad).
      origin/main


    Switched to branch 'main'
    To github.com:alan-turing-institute/github-example.git
       c8ba483..12ee6ad  main -> main
    To github.com:alan-turing-institute/github-example.git
     - [deleted]         gh-pages
