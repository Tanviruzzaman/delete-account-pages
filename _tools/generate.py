#!/usr/bin/env python3
"""
Generate a Google Play compliant "delete account" page for each Softifybd Ltd app.

Usage
-----
    python3 _tools/generate.py                  # rebuild every app listed in APPS below
    python3 _tools/generate.py "My New App"     # add one more app on the fly

Run it from anywhere; it works out the site root itself. Each app gets its own folder
containing index.html, so on GitHub Pages the URLs become
    https://USERNAME.github.io/delete-account/<slug>/
and the shared all-apps page is written to the site root as index.html.

To add an app permanently, add its name to the APPS list and re-run this script.
"""

import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

# ---------------------------------------------------------------- configuration
APPS = ["Delta Classic", "BNS"]
DEVELOPER = "Softifybd Ltd"
SUPPORT_EMAIL = "softifybd@gmail.com"
LAST_UPDATED = "10 August 2026"

# The site root is this script's folder, or its parent when the script lives in _tools/.
_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent if _HERE.name == "_tools" else _HERE

# Any existing per-app page works as the template. They carry this marker; the shared
# all-apps page does not, so it is never mistaken for a template.
TEMPLATE_MARKER = "OPTIONAL: IN-APP DELETION"


def find_template() -> Path:
    candidates = sorted(ROOT.glob("index.html")) + sorted(ROOT.glob("*/index.html"))
    for path in candidates:
        if TEMPLATE_MARKER in path.read_text(encoding="utf-8"):
            return path
    raise SystemExit(
        f"No per-app template found under {ROOT}. Expected a file such as "
        "delta-classic/index.html containing the in-app deletion marker."
    )


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "app"


def template_app_name(template: str) -> str:
    """Read the app name out of the template's <title>, so any app page can be the source."""
    m = re.search(r"<title>Delete Your (.+?) Account", template)
    if not m:
        raise SystemExit("Could not read the app name from the template's <title> tag.")
    return m.group(1)


def make_app_page(template: str, app: str) -> str:
    """Swap the template's app name for another app's name, including the mailto subject.

    The mailto subject is URL-encoded, so it is rebuilt first: decode it, swap the name,
    re-encode. Doing it this way avoids the trap where a single-word source name such as
    "BNS" encodes to itself, which would make a naive encoded-string replace corrupt every
    plain-text occurrence on the page as well.
    """
    source = template_app_name(template)

    def rebuild_subject(m: re.Match) -> str:
        decoded = unquote(m.group(2)).replace(source, app)
        return m.group(1) + quote(decoded)

    html = re.sub(r'(mailto:[^"\'\s]*?subject=)([^"\'&\s]*)', rebuild_subject, template)
    return html.replace(source, app)


def style_block(template: str) -> str:
    m = re.search(r"<style>.*?</style>", template, re.S)
    if not m:
        raise SystemExit("Could not find the <style> block in the template.")
    return m.group(0)


def make_all_apps_page(template: str, apps: list[str]) -> str:
    """One page that covers every app, so a single URL can be reused across listings."""
    app_items = "\n".join(f"      <li><strong>{a}</strong></li>" for a in apps)
    subject = quote("Delete my account")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Delete Your Account &amp; Data — {DEVELOPER} Apps</title>
<meta name="description" content="Request deletion of your account and associated data for any Android app published by {DEVELOPER}, including {', '.join(apps)}. Email {SUPPORT_EMAIL} to request deletion.">
<meta name="robots" content="index, follow">
{style_block(template)}
</head>
<body>
<div class="wrap">

  <header>
    <span class="eyebrow">Account &amp; Data Deletion</span>
    <h1>Request deletion of your account and data</h1>
    <p class="lead">This page explains how to ask {DEVELOPER} to delete your account for any of
      our Android apps, what data is erased when we do, and what we are required to keep.</p>
    <p class="meta">
      Developer: <strong>{DEVELOPER}</strong> &nbsp;·&nbsp;
      Last updated: <strong>{LAST_UPDATED}</strong>
    </p>
  </header>

  <h2>Apps covered by this page</h2>
  <div class="panel">
    <ul>
{app_items}
    </ul>
    <p>The process below applies to every app in this list. If you use more than one of our
      apps, tell us which accounts you want removed and we will handle them together.</p>
  </div>

  <h2>How to request account deletion</h2>
  <p>You do not need to be signed in, and you do not need to have the app installed, to make a
    request. Follow the steps below.</p>

  <div class="panel accent">
    <h3>Step by step</h3>
    <ol>
      <li>Open your email app and start a new message to our support address:
        <a class="mailbox" href="mailto:{SUPPORT_EMAIL}?subject={subject}">{SUPPORT_EMAIL}</a>
      </li>
      <li>Use <strong>“Delete my account”</strong> as the subject line.</li>
      <li>In the message, name <strong>which app</strong> the account belongs to — for example
        {apps[0]}{' or ' + apps[1] if len(apps) > 1 else ''}.</li>
      <li>Include the <strong>username, email address, or phone number</strong> that you used to
        create the account, so that we can locate it.</li>
      <li>Send the email. We will reply from <em>{SUPPORT_EMAIL}</em> to confirm we received
        your request.</li>
      <li>Reply to that confirmation email to verify that the account is yours. This step
        protects you — it stops someone else from deleting your account.</li>
      <li>Once verified, we delete the account and its associated data on the timeline described
        below, and email you when it is done.</li>
    </ol>
    <p>Deletion is permanent. Your account, and the data listed as deleted below, cannot be
      recovered afterwards.</p>
  </div>

  <h3>You can copy this message</h3>
  <p class="template">To: {SUPPORT_EMAIL}
Subject: Delete my account

Hello {DEVELOPER},

Please delete my account and all associated personal data.

App name: ______________________

My account identifier (username / email / phone): ______________________

I confirm that I am the owner of this account.

Thank you.</p>

  <h2>What happens to your data</h2>
  <p>The table below lists the categories of data connected to an account, whether each one is
    deleted when your request is processed, and how long anything we must keep is retained.</p>

  <table>
    <caption>Data deleted and data retained</caption>
    <thead>
      <tr>
        <th scope="col">Data</th>
        <th scope="col">Outcome</th>
        <th scope="col">Retention period</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Account credentials and profile — username, email address, phone number, password or
          authentication tokens, profile photo</td>
        <td><span class="tag del">Deleted</span></td>
        <td>Erased within 30 days of a verified request</td>
      </tr>
      <tr>
        <td>Content you created or uploaded in the app, and your in-app settings and preferences</td>
        <td><span class="tag del">Deleted</span></td>
        <td>Erased within 30 days of a verified request</td>
      </tr>
      <tr>
        <td>Usage and diagnostic data linked to your account, and device identifiers linked to
          your account</td>
        <td><span class="tag del">Deleted</span></td>
        <td>Erased within 30 days of a verified request</td>
      </tr>
      <tr>
        <td>Support emails and messages you exchanged with us</td>
        <td><span class="tag del">Deleted</span></td>
        <td>Erased within 90 days of a verified request</td>
      </tr>
      <tr>
        <td>Encrypted backup copies of the above</td>
        <td><span class="tag del">Deleted</span></td>
        <td>Purged as backups rotate, no later than 90 days</td>
      </tr>
      <tr>
        <td>Purchase, billing and tax records, where you made a purchase</td>
        <td><span class="tag keep">Kept</span></td>
        <td>Retained as long as accounting and tax law requires, then deleted. Google Play holds
          its own copy of Play purchases.</td>
      </tr>
      <tr>
        <td>Minimal records needed to prevent fraud, abuse or repeat policy violations, and to
          comply with a legal obligation or court order</td>
        <td><span class="tag keep">Kept</span></td>
        <td>Retained only for as long as the purpose requires, then deleted</td>
      </tr>
      <tr>
        <td>Aggregated or anonymised statistics that can no longer identify you or your device</td>
        <td><span class="tag keep">Kept</span></td>
        <td>Retained indefinitely, because it is no longer personal data</td>
      </tr>
    </tbody>
  </table>

  <h2>How long it takes</h2>
  <ul>
    <li>We acknowledge your request within <strong>7 days</strong>.</li>
    <li>Once you have verified the account is yours, we delete it and its associated data within
      <strong>30 days</strong>.</li>
    <li>Encrypted backups and support correspondence are fully purged within <strong>90
      days</strong>.</li>
    <li>We email you to confirm once deletion is complete.</li>
  </ul>

  <h2>Deleting data without deleting your account</h2>
  <p>If you would rather keep your account but remove specific data — for example content you
    uploaded, or your profile photo — say so in your email and tell us what you want removed. We
    will action that request on the same timeline instead of deleting the whole account.</p>

  <h2>Contact</h2>
  <p>
    {DEVELOPER} — app support<br>
    Email: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a>
  </p>
  <p>If you do not hear from us within 7 days, please email again and mention that it is a
    follow-up, in case the first message was filtered.</p>

  <footer>
    <p>This page is published by {DEVELOPER}, developer of the Android apps listed above, to let
      users request deletion of their account and associated data. Last updated {LAST_UPDATED}.</p>
  </footer>

</div>
</body>
</html>
"""


def main() -> None:
    template_path = find_template()
    template = template_path.read_text(encoding="utf-8")
    print(f"template: {template_path.relative_to(ROOT)}")

    apps = list(APPS) + [a for a in sys.argv[1:] if a not in APPS]

    for app in apps:
        folder = ROOT / slugify(app)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(make_app_page(template, app), encoding="utf-8")
        print(f"wrote {slugify(app)}/index.html   ({app})")

    (ROOT / "index.html").write_text(make_all_apps_page(template, apps), encoding="utf-8")
    print("wrote index.html   (shared page for all apps)")


if __name__ == "__main__":
    main()
