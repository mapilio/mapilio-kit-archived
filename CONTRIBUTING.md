# Contribute Rules

You are welcome to contribute to project mapilio-uploader. 

We sincerely appreciate your contribution.  This document explains our workflow and work style.

<!--ts-->

* [Workflow](#workflow)
* [Code Review](#code-review)
* [Coding Standard](#coding-standard)
   - [Code Style](#code-style)
   - [Docstring Format](#docstring-format)
* [Keeping Your Fork Update](#keeping-your-fork-update)
* [Issues](#issues)
<!--te-->

## Workflow

PaddlePaddle uses this [Git branching model](http://nvie.com/posts/a-successful-git-branching-model/).  The following steps guide usual contributions.

1. Fork

   Our development community has been growing fastly; it doesn't make sense for everyone to write into the official repo.  So, please file Pull Requests from your fork. On GitHub.com, navigate to the .[/mapilio/mapilio-uploader repository](https://github.com/mapilio/mapilio-uploader).  In the top-right corner of the page, click Fork.

1. Clone

   To make a copy of your fork to your local computers, please run

   ```bash
   git clone https://github.com/mapilio/mapilio-uploader.git
   cd mapilio-uploader
   ```

1. Create the local feature branch

   For daily works like adding a new feature or fixing a bug, please open your feature branch before coding:

   ```bash
   git checkout -b mybranch
   ```

1. Work on your new code. Write and run the tests.

1. Commit your Changes

```bash
git add -A
```

```bash
git commit -m "commit message here"
```

6. Push your changes to your GitHub repository.

  You can "push" your local work into your forked repo:

```bash
git push origin mybranch
```

   To create a pull request, please follow [these steps](https://help.github.com/articles/creating-a-pull-request/).

   If your change is for fixing an issue, please write ["Fixes <issue-URL>"](https://help.github.com/articles/closing-issues-using-keywords/) in the description section of your pull request.  Github would close the issue when the owners merge your pull request.

   Please remember to specify some reviewers for your pull request.  If you don't know who are the right ones, please follow Github's recommendation.


## Code Review

-  Please feel free to ping your reviewers by sending them the URL of your pull request via IM or email.  Please do this after your pull request passes the CI.

- Please answer reviewers' every comment.  If you are to follow the comment, please write "Done"; please give a reason otherwise.

- If you don't want your reviewers to get overwhelmed by email notifications, you might reply their comments by [in a batch](https://help.github.com/articles/reviewing-proposed-changes-in-a-pull-request/).

- Reduce the unnecessary commits.  Some developers commit often.  It is recommended to append a sequence of small changes into one commit by running `git commit --amend` instead of `git commit`.


## Coding Standard

### Code Style

Our Python code follows the [Google style guide](https://google.github.io/styleguide/pyguide.html) and [PEP 8 -Style Guide](https://www.python.org/dev/peps/pep-0008/)


### Docstring Format

For functions:

```python

def contributors_function(
        id: int,
        name: str, 
        score: float, 
        isvalid: bool, 
        queue: list, 
        image: np.ndarray = None
) -> dict:
    """
    
    Args:
        id: 
        name: 
        score: 
        queue: 
        image: 

    Returns:

    """
    pass
   ```

For classes:

```python
class Sampleclass:
    """
    description of Class
    """
    def __init__(self,  *args, **kwargs):
        """
        description of function
	"""
```
## Keeping Your Fork Update

Unlike systems like Subversion, Git can have multiple remotes. A remote is the name for a URL of a Git repository. By default your fork will have a remote named "origin" which points to your fork, but you can add another remote named "mapilio-uploader" which points to https://github.com/mapilio/mapilio-uploader.git. This is a read-only remote but you can pull from this develop branch to update your own.
If you are using command-line you can do the following:

   ```bash
git remote add mapilio-uploader https://github.com/mapilio/mapilio-uploader.git
   ```
   ```bash
git pull mapilio-uploader mybranch
   ```
   ```bash
git push origin mybranch
   ```

Now your fork is up to date. This should be done regularly, or before you send a pull request at least.

## Issues
### Create a new issue
If you spot a problem with the [docs](https://github.com/mapilio/mapilio-uploader/issues). Search if an issue already exists. Search Filter:
```bash
is:issue is:open repo:mapilio/mapilio-uploader 
```
If a related issue doesn't exist, you can open a new issue using a relevant issue form.   [form](https://github.com/mapilio/mapilio-uploader/issues/new).                    
### Solve an  issue
Scan through our existing issues to find one that interests you. You can narrow down the search using labels as filters. See Labels for more information. As a general rule, we don’t assign issues to anyone. If you find an issue to work on, you are welcome to open a PR with a fix.