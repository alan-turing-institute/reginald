This is a list of the steps I, James G, took when I got a new laptop from IT.

- [ ] Sign in to Apple Cloud on new machine. Activate all accounts (Office365, personal email, ...)

- [ ] `brew cask install emacs`, and anything else you need.

- [ ] In my case, I store config files on Apple Cloud, and symbolic link them to their required place, eg:
  * `~/.emacs.el`
  * `~/.bash_profile`

- [ ] Office (including OneDrive): I installed with the new "self service" app that IT now bundle with laptops (which apparently installs things via homebrew!)

- [ ] OneDrive setup. I have a personal shared space on OneDrive, but also multiple shared spaces for projects, set up as "Groups" in Office 365. The standard location that Office chooses for your local OneDrive image is annoyingly long and full of spaces. So I put all shared spaces in ~/OneDrive-Actuals and then symbolic link to ~/OneDrive (for my personal space) and ~/Share/X (for project X).

- [ ] SSH tokens for GitHub. I made new ones. I had thought about moving them, but it turned out to be straightforward to make new ones.

- [ ] Go through every repo with an authoritative remote, make sure I've pushed all local commits, and delete. (I keep all repos in `~/Projects/`, with remotes usually on GitHub.)

- [ ] Double-check other directories within `~/`

- [ ] Install Emacs additions as I learn that I need them ...
