# Contest scoreboards on GitHub Pages

Drop scraped scoreboards into **`scoreboards/`**. A GitHub Action builds the website and publishes it,
no other step needed.

```
scoreboards/            <- you put the scraped scoreboards here (one folder per contest)
    my-contest/data.json     (+ flags/, logo.png, meta.json from the notebook)
tools/
    viewer.html         the scoreboard page (shared by all contests, edit it to restyle everything)
    home.html           the contest list on the front page
    build_site.py       turns scoreboards/ into the website (plain Python, nothing to install)
.github/workflows/pages.yml   runs the build and deploys to GitHub Pages on every push
```

## One-time setup
1. Create a GitHub repository and upload everything in this folder (keep the `.github` folder).
2. **Settings -> Pages -> Build and deployment -> Source: GitHub Actions.**
3. Open the **Actions** tab: the first run starts by itself (or press *Run workflow*).
   The site appears at `https://<user>.github.io/<repo>/`.

## Adding / updating a contest
1. Run the archiver notebook and unzip `<id>-contest-folder.zip`.
2. Upload the `<id>` folder into `scoreboards/` (GitHub: *Add file -> Upload files*, drag the folder in; or `git add` / `git push`).
3. Wait about a minute: the home page lists it and `contests/<id>/` is its scoreboard.
   Uploading the same `<id>` again replaces it (handy for a contest that is still running).

Because `index.html` is rebuilt from `tools/viewer.html` on every run, a change to the viewer applies to every contest
without re-scraping anything.

## Try it locally
```
python3 tools/build_site.py
python3 -m http.server -d _site      # then open http://localhost:8000/
```
