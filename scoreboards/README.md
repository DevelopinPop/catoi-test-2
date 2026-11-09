# Put your scraped scoreboards here

One entry per contest. Any of these works:

| What you drop in                         | What happens                                                              |
|------------------------------------------|---------------------------------------------------------------------------|
| `my-contest/` (folder with `data.json`)  | the usual output of the archiver notebook (flags, logo and meta.json come along) |
| `my-contest.json`                        | just the data                                                             |
| `my-contest.html`                        | a saved scoreboard page, its data is extracted and rebuilt                |
| `my-contest/` (folder with only `index.html`) | copied as it is                                                      |

The folder / file name becomes the address: `https://<user>.github.io/<repo>/contests/my-contest/`.
Re-uploading the same name replaces that contest. Files and folders starting with `.` or `_` are ignored,
and so are `raw/` folders. Delete `sample-open-2026/` once you have your own contests.
