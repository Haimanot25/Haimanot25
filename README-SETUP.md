# Haimanot25 GitHub Profile Automation Kit

A ready-to-customize GitHub profile README with a cyan-on-dark custom SVG banner, animated typing text, skill icons, dynamic stats cards, contribution snake automation, and a daily workflow that refreshes a recent-public-repositories table.

## Included

- `README.md` — profile page content.
- `assets/hero.svg` — custom, self-contained banner artwork.
- `scripts/generate_readme.py` — safely updates the generated repository table using public GitHub API data.
- `.github/workflows/update-profile.yml` — refreshes the repository table daily and on manual dispatch.
- `.github/workflows/snake.yml` — generates contribution snake SVGs and publishes them to the `output` branch.
- `setup.ps1` — copies the project into a chosen local folder after confirmation.

## Requirements

- A GitHub account with username `Haimanot25`.
- A public repository named exactly `Haimanot25` (GitHub renders its README on your profile).
- Git installed on Windows.
- PowerShell 5.1 or newer.
- Python 3.9+ is optional for local testing of the README updater; GitHub Actions installs Python automatically.

## Install on Windows

1. Download and extract this ZIP.
2. Open PowerShell in the extracted folder.
3. Run:

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\setup.ps1
   ```

   The execution policy change applies only to the current PowerShell process. If your organization's policy disallows it, follow your organization's instructions instead.

4. Create a **public** GitHub repository named `Haimanot25` if it does not exist. Do not create a second repository if you already use it for your profile.
5. In the destination folder created by the script, review `README.md` and then publish:

   ```powershell
   git init
   git branch -M main
   git add .
   git commit -m "Add automated GitHub profile"
   git remote add origin https://github.com/Haimanot25/Haimanot25.git
   git push -u origin main
   ```

   If the repository already has commits, clone it first or merge the existing history instead of running `git init` over an unrelated repository.

## Enable the automation

1. Open `https://github.com/Haimanot25/Haimanot25/settings/actions`.
2. Under **Actions → General → Workflow permissions**, allow workflows to read and write repository contents.
3. Open **Actions**, select `Generate contribution snake`, and click **Run workflow** once.
4. Run `Update profile repository list` once as well.

The workflows use GitHub's automatically provided `GITHUB_TOKEN`; you do not need to paste a personal access token into a file. The `output` branch is created by the snake workflow when it runs successfully.

## Customize

- Change the visual design in `assets/hero.svg`.
- Edit the intro, skills, and featured project copy in `README.md`.
- The DBoard link is set to `https://github.com/Haimanot25/dboard`.
- The HTML-to-PDF project URL is intentionally not invented. Replace the placeholder only after confirming the repository URL.
- To change the username, update `Haimanot25` in the README, script, and workflow files.

## How the automation works

- The repository-table script calls the public GitHub REST API and displays up to six non-forked, non-archived public repositories, ordered by last update.
- GitHub Actions runs that script daily at 06:23 UTC and commits only if the README changes.
- The contribution snake workflow runs daily at 03:41 UTC and publishes generated SVGs to the `output` branch.
- Stats, streak, skill-icon, and typing images are provided by third-party services. They may occasionally be unavailable or rate-limited; the profile remains readable without them.

## Notes

- The repository table only includes public repositories. It does not invent star counts or language statistics.
- GitHub Actions schedules can be delayed during high load.
- The snake graphic requires contribution activity to visualize; it does not create contributions.
- Review third-party image-service privacy, availability, and terms before relying on them for a professional profile.
