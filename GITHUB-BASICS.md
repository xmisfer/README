# GitHub basics: finding, reading, and safely installing projects

## 1. What GitHub is

GitHub is a website where people publish code and the files around it.
Each project lives in a "repository" (repo). A repo's address looks like
`github.com/OWNER/PROJECT`. You do not need an account to browse or download.

## 2. Finding repositories

1. Go to https://github.com and use the search box at the top.
2. Type what you want in plain words, e.g. `markdown editor` or `youtube downloader`.
3. On the results page, click **Repositories** in the left column.
4. Sort by **Most stars** (dropdown at top right). Stars are rough votes of trust.
5. Use the filters on the left to narrow by language if you care.
6. Other good discovery pages:
   - https://github.com/trending shows what is popular this week.
   - https://github.com/topics groups projects by subject.
   - Searching the web for `"<thing I want>" site:github.com` also works well.

## 3. Reading a repository page

The front page of a repo shows you:

- **README** (scroll down): what it does, screenshots, how to install, how to use.
  Look for an "Installation" or "Getting started" section first.
- **About box** (top right): a one-line description, website link, and topics.
- **Stars, forks, watchers** (top right): popularity signals.
- **Last commit date** (above the file list): shows whether it is still maintained.
  Years of silence is a warning sign.
- **Issues** tab: real user problems. Many open, unanswered bugs is a warning sign.
- **License** file: whether you are allowed to use it freely.
- **Releases** (right column): packaged, downloadable versions. See below.

## 4. The Releases page

1. Click **Releases** in the right column (or add `/releases` to the repo URL).
2. The newest release is at the top. Prefer the one marked **Latest**.
   Avoid **Pre-release** versions unless you want to test unfinished work.
3. Read the release notes. They say what changed and sometimes warn about breaking changes.
4. Expand **Assets**. Pick the file for your computer:
   - Windows: `.exe`, `.msi`, or a `win`/`windows` zip. Usually `x64`/`amd64`.
   - macOS: `.dmg`, `.pkg`, or a `mac`/`darwin` archive. `arm64`/`Apple Silicon` for M-series Macs, `x64`/`intel` for older ones.
   - Linux: `.deb` (Debian/Ubuntu), `.rpm` (Fedora), `.AppImage`, or a `linux` tarball.
5. Ignore "Source code (zip/tar.gz)". That is raw code, not an installer.
6. If there is a `checksums.txt` or `.sha256` file, you can verify your download
   was not corrupted or swapped (see section 6).

## 5. Three safe ways to install

**A. Download an installer from Releases** (simplest).
Download the asset, open it, follow the prompts. On macOS and Windows you may see
a warning because the app is not from the app store; that alone is not proof of
malware, but only continue if the project passed the checklist in section 7.

**B. Use a package manager** (best for command-line tools).
A package manager is an app store for your terminal. The README usually lists a
one-line command for it. Which one depends on your OS, which is why I need to
know it before giving specific commands:
- Windows: `winget` (built in) or Scoop/Chocolatey.
- macOS: Homebrew (`brew`).
- Linux: `apt`, `dnf`, `pacman`, etc. depending on your distribution.

**C. Clone the source and build it** (advanced).
Only needed when there is no release or package. Skip this until you are comfortable.

## 6. Verifying an install worked

- **Graphical app**: it appears in your Start menu / Applications folder and opens.
- **Command-line tool**: open a terminal and run `TOOLNAME --version`.
  Seeing a version number means it is installed and on your PATH.
- **Checksum**: on the Releases page, copy the SHA256 listed for your file, then run
  - Windows PowerShell: `Get-FileHash .\file.exe`
  - macOS/Linux: `shasum -a 256 file` or `sha256sum file`
  and compare. They must match exactly.

## 7. Undoing an install

- **Installer**: Windows Settings > Apps > Uninstall; macOS drag the app to Trash;
  Linux `.deb`/`.rpm` use `sudo apt remove NAME` / `sudo dnf remove NAME`.
- **Package manager**: `winget uninstall NAME`, `brew uninstall NAME`,
  `scoop uninstall NAME`, `sudo apt remove NAME`.
- **Portable zip / AppImage**: delete the folder or file. Nothing else was changed.
- **Cloned source**: delete the folder.

## 8. Security checklist before installing anything

1. **Is this the real project?** Check the owner name. Popular projects are often
   copied under lookalike names. Follow the link from the project's official website
   or Wikipedia page rather than trusting a search result.
2. **Signs of life**: recent commits, answered issues, several contributors, a license.
3. **Stars are not safety.** Stars can be bought. Use them together with the above.
4. **Read the README's install section.** If it tells you to paste a long command that
   starts with `curl ... | sh`, `irm ... | iex`, or `bash -c "$(wget ...)"`, that
   downloads a script and runs it immediately. Only do this for projects you already
   trust, and prefer a package manager when one is available.
5. **Never run commands you do not understand** that were posted in an Issue, a
   comment, a Discord, or a video. Ask first.
6. **Download only from the Releases page of the real repo**, never from a link
   in an issue comment or a third-party "download" site.
7. **Verify checksums** when they are provided (section 6).
8. **Scan it**: upload the downloaded file to https://www.virustotal.com before opening it.
9. **Be suspicious of** password-protected zips, files named `.scr`, `.bat`, `.vbs`,
   installers that ask to disable your antivirus, and "cracked" or "free premium" versions.
10. **Prefer package managers** for command-line tools. They verify what they install.
