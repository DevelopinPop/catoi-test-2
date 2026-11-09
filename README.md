# Contest scoreboards

A static website (GitHub Pages) with one scoreboard per contest.

```
index.html            home page: lists every folder found in contests/
contests/<id>/        one contest (made by the ranking archiver notebook)
    index.html        the scoreboard
    data.json         its data
    meta.json         title / participants (used by the home page)
    logo.*, flags/    images
tools/make_index.py   writes contests/index.json (used by the optional workflow)
.github/workflows/    optional: keeps contests/index.json up to date
.nojekyll             tells GitHub Pages not to run Jekyll
```

## Publish

1. Create a GitHub repository and upload these files (the full-site zip from the notebook) to the `main` branch.
2. **Settings -> Pages -> Build and deployment -> Deploy from a branch -> `main` / `(root)`**.
3. The site is at `https://<user>.github.io/<repo>/`.

## Add another contest

Run the notebook for the new contest and upload the new `<id>` folder into `contests/` (drag it onto the GitHub page, or `git add contests/<id>`).
Nothing else needs to change: the home page picks it up by itself.

## Remove a contest

Delete its folder from `contests/`.
