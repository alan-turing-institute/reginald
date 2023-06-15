# 4.11 Debugging With git bisect


*Estimated time to complete this notebook: 5 minutes*

You can use

``` bash
git bisect
```

to find out which commit caused a bug.

## An example repository

In a nice open source example, I found an arbitrary exemplar on github


```python
import os

top_dir = os.getcwd()
git_dir = os.path.join(top_dir, "learning_git")
os.chdir(git_dir)
```


```bash
%%bash
rm -rf bisectdemo
git clone https://github.com/shawnsi/bisectdemo.git
```

    Cloning into 'bisectdemo'...



```python
bisect_dir = os.path.join(git_dir, "bisectdemo")
os.chdir(bisect_dir)
```


```bash
%%bash
python squares.py 2 # 4
```

    4


This has been set up to break itself at a random commit, and leave you to use
bisect to work out where it has broken:


```bash
%%bash
./breakme.sh > break_output
```

    error: branch 'buggy' not found.
    Switched to a new branch 'buggy'


Which will make a bunch of commits, of which one is broken, and leave you in the broken final state


```python
python squares.py 2 # Error message
```


      File "<ipython-input-6-8e2377cd54bf>", line 1
        python squares.py 2 # Error message
                     ^
    SyntaxError: invalid syntax



## Bisecting manually


```bash
%%bash
git bisect start
git bisect bad # We know the current state is broken
git checkout master
git bisect good # We know the master branch state is OK
```

    Your branch is up to date with 'origin/master'.
    Bisecting: 500 revisions left to test after this (roughly 9 steps)
    [ac8555136ae6e4fe0e0eefab16219132d0ff84e3] Comment 499


    Switched to branch 'master'


Bisect needs one known good and one known bad commit to get started

## Solving Manually

``` bash
python squares.py 2 # 4
git bisect good
python squares.py 2 # 4
git bisect good
python squares.py 2 # 4
git bisect good
python squares.py 2 # Crash
git bisect bad
python squares.py 2 # Crash
git bisect bad
python squares.py 2 # Crash
git bisect bad
python squares.py 2 #Crash
git bisect bad
python squares.py 2 # 4
git bisect good
python squares.py 2 # 4
git bisect good
python squares.py 2 # 4
git bisect good
```


And eventually:

``` bash
git bisect good
    Bisecting: 0 revisions left to test after this (roughly 0 steps)

python squares.py 2
    4

git bisect good
2777975a2334c2396ccb9faf98ab149824ec465b is the first bad commit
commit 2777975a2334c2396ccb9faf98ab149824ec465b
Author: Shawn Siefkas <shawn.siefkas@meredith.com>
Date:   Thu Nov 14 09:23:55 2013 -0600

    Breaking argument type

```

``` bash
git bisect end
```

## Solving automatically

If we have an appropriate unit test, we can do all this automatically:


```bash
%%bash
git bisect start
git bisect bad HEAD # We know the current state is broken
git bisect good master # We know master is good
git bisect run python squares.py 2
```

    Bisecting: 500 revisions left to test after this (roughly 9 steps)
    [ac8555136ae6e4fe0e0eefab16219132d0ff84e3] Comment 499
    running python squares.py 2
    Bisecting: 249 revisions left to test after this (roughly 8 steps)
    [dc6f0dbecc899deaf0eff1fe3a73a9264e16433f] Comment 250
    running python squares.py 2
    4
    Bisecting: 124 revisions left to test after this (roughly 7 steps)
    [5878604f23677c8e5cf84a84562a9f51ff044499] Comment 375
    running python squares.py 2
    4
    Bisecting: 62 revisions left to test after this (roughly 6 steps)
    [718d9858a1b9b476bb12a1b6e058fa6cdd6f7f1a] Comment 437
    running python squares.py 2
    4
    Bisecting: 31 revisions left to test after this (roughly 5 steps)
    [041edbbbd3093bf9ec51f31cd59ab935da74ad76] Comment 468
    running python squares.py 2
    4
    Bisecting: 15 revisions left to test after this (roughly 4 steps)
    [a4cc3ab1db2c7a27f38486a430925c77cb23236f] Comment 484
    running python squares.py 2
    4
    Bisecting: 7 revisions left to test after this (roughly 3 steps)
    [e907c01ab2defc6b777ef4411bc2b79af2c15335] Comment 492
    running python squares.py 2
    4
    Bisecting: 3 revisions left to test after this (roughly 2 steps)
    [539c282551e2306cff9a5067e01b5983230a00ef] Comment 495
    running python squares.py 2
    Bisecting: 1 revision left to test after this (roughly 1 step)
    [5b19f6ff5e0ad5cd90b997a40e7534fbf9963e68] Breaking argument type
    running python squares.py 2
    Bisecting: 0 revisions left to test after this (roughly 0 steps)
    [6c02f2ac5a56ab88966be1edd1d0bb8194c01f5a] Comment 493
    running python squares.py 2
    4
    5b19f6ff5e0ad5cd90b997a40e7534fbf9963e68 is the first bad commit
    commit 5b19f6ff5e0ad5cd90b997a40e7534fbf9963e68
    Author: Shawn Siefkas <shawn.siefkas@meredith.com>
    Date:   Thu Nov 14 09:23:55 2013 -0600

        Breaking argument type

     squares.py | 2 +-
     1 file changed, 1 insertion(+), 1 deletion(-)
    bisect run success


    Previous HEAD position was 6c02f2a Comment 493
    Switched to branch 'buggy'
    Traceback (most recent call last):
      File "squares.py", line 9, in <module>
        print(integer**2)
    TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'
    Traceback (most recent call last):
      File "squares.py", line 9, in <module>
        print(integer**2)
    TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'
    Traceback (most recent call last):
      File "squares.py", line 9, in <module>
        print(integer**2)
    TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'


Boom!
