# Delete Account pages for Softifybd Ltd apps

Covers **Delta Classic** and **BNS**, and scales to any other app you publish.

Inside `delete-account-pages.zip`:

```
index.html                 → one shared page covering ALL Softifybd apps
delta-classic/index.html   → page for Delta Classic only
bns/index.html             → page for BNS only
.nojekyll                  → leave it there, it stops GitHub post-processing the files
_tools/generate.py         → regenerates all of the above, and adds new apps
```

You do not have to use all of it. Pick one of the two approaches below.

---

## Which approach?

**Shared page — one URL for every app.** Paste the same URL into the Data safety form of
Delta Classic, BNS and anything you publish later. This is allowed: Google requires the page
to refer to *your app or developer name* as shown on the store listing, and the shared page
names Softifybd Ltd and lists each app. Least work, one page to maintain.

**Per-app pages — one URL per app.** Slightly safer with reviewers, because the page names
the exact app they are reviewing and describes only that app's data. Recommended if the apps
handle noticeably different data, or if you want to describe in-app deletion steps that
differ per app.

You can do both — upload everything, then use whichever URL you prefer for each app.

---

## Publish on GitHub Pages (recommended, no terminal needed)

GitHub Pages is free forever, HTTPS, and never sleeps. A deletion URL has to stay reachable
for as long as the apps are on Play, so avoid hosts that can expire.

### 1. Create the repository

1. Sign in at https://github.com.
2. **+** (top right) → **New repository**.
3. Name: `delete-account`
4. Visibility: **Public** — required. Pages does not serve private repos on the free plan.
5. **Create repository**.

### 2. Upload the files

1. Unzip `delete-account-pages.zip` on your computer.
2. On the empty repository page, click **uploading an existing file**
   (or **Add file** → **Upload files**).
3. Select **all** the unzipped contents — including the `delta-classic` and `bns` folders —
   and drag them into the upload box. Dragging folders preserves the folder structure, which
   is what creates the per-app URLs.
4. Click **Commit changes**.

Do not rename any file. Every page must stay named exactly `index.html`, because that is what
makes a folder resolve to a clean URL.

### 3. Turn on Pages

1. Repository → **Settings** → **Pages** (left sidebar).
2. *Source*: **Deploy from a branch**.
3. Branch **main**, folder **/ (root)** → **Save**.
4. Wait one to three minutes, then refresh. A green banner shows your live site.

### 4. Your URLs

```
Shared page   https://YOUR-USERNAME.github.io/delete-account/
Delta Classic https://YOUR-USERNAME.github.io/delete-account/delta-classic/
BNS           https://YOUR-USERNAME.github.io/delete-account/bns/
```

Replace `YOUR-USERNAME` with your GitHub username, and keep the trailing slash.

### 5. Test before submitting

Open each URL in a **private/incognito window**, and ideally on your phone over mobile data.
You must see the page with no sign-in prompt. A 404 usually means the repo is private, a file
was renamed, or Pages has not finished building — wait two minutes and retry.

---

## Better option if you have a website

Hosting on your own domain is the strongest choice, because the domain matches the developer
name on your listings:

```
https://softifybd.com/delete-account/            (shared)
https://softifybd.com/delete-account/bns/        (per app)
```

Upload the same folder structure through your hosting control panel or FTP. Nothing in the
files needs to change.

You can also keep GitHub Pages and put your domain in front of it: **Settings → Pages →
Custom domain**, enter e.g. `support.softifybd.com`, then add the matching CNAME record at
your DNS provider.

---

## Railway, if you insist

Railway needs a web service, so static HTML will not deploy alone. Add a `Dockerfile` beside
`index.html`:

```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html/
```

Then at https://railway.app: sign in with GitHub → **New Project** → **Deploy from GitHub
repo** → pick the repo → after the build, open the service → **Settings** → **Networking** →
**Generate Domain**.

Only do this on a paid plan. If trial credit runs out the service stops, the URL dies, and
every app that points at it goes back into violation.

---

## Now fix the Data safety form — for each app separately

The URL alone will **not** clear the rejection. The violation is a *mismatch*: you declared
that the app has no account creation, and Google detected that it does. Repeat this for Delta
Classic, BNS, and any other flagged app — the Data safety form is per app, so nothing carries
over automatically.

In **Play Console → (select the app) → Policy and programs → App content → Data safety**, on
the account creation question:

1. Leave **"My app does not allow users to create an account"** unchecked.
2. Check every method the app actually supports. *Username and other authentication* alone is
   often wrong — if the app also takes a password, add *Username and password*; if it offers
   Google or Facebook sign-in, add *OAuth*. The mismatch is what triggered enforcement, so
   this has to match real behaviour.
3. Paste the URL into **Delete account URL**.
4. **Next** through the remaining screens, then **Save**.

Then check **Policy and programs → Policy status** for that app. If the version stays flagged
after the form is saved and reviewed, use **Submit an appeal** on the issue page and state
that the Data safety form has been corrected and a deletion URL added.

---

## Adding more apps later

Edit `_tools/generate.py`, add the app name to the `APPS` list near the top, and run:

```bash
python3 _tools/generate.py
```

Or generate one without editing the file:

```bash
python3 _tools/generate.py "My Third App"
```

It rewrites the per-app folders and refreshes the shared page's app list. Then upload the new
folder to the repo the same way as before.

If you would rather not run Python: copy the `bns` folder, rename the copy to your new app's
slug, open its `index.html` on GitHub and use the pencil icon to replace every occurrence of
`BNS` with the new app name. Do not forget the `<title>` tag and the `mailto:` subject line.

---

## Two things to review in every page

- **In-app deletion block.** Each per-app page has a commented-out section describing deletion
  from inside the app. If that app has the feature, delete the `<!--` and `-->` markers and
  correct the menu names to match the app exactly. If it does not, leave it commented out —
  never describe a feature that isn't there.
- **Retention periods.** The pages state 30 days for account data, 90 days for backups and
  support mail. Make sure that matches what you actually do, and change the numbers if not.
