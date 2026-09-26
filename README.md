# 恋のあとがき。／あと1ページの恋。

公式作品サイトの静的公開リポジトリです。完成済み作品とサイト一式を、ハッシュ検証後に `dist/` へ復元します。

## Cloudflare Pages

- Git repository: this repository
- Production branch: `main`
- Framework preset: `None`
- Build command: `python3 restore_site.py`
- Build output directory: `dist`
- Root directory: repository root

初回接続後、ビルドが成功するとCloudflareの `*.pages.dev` URLで公開されます。Pagesのプロジェクト名を `koinoatogaki` に設定すると `https://koinoatogaki.pages.dev` になります。

## Local build

Python 3が必要です。

```sh
python3 restore_site.py
```

ビルドは全分割データと完成アーカイブのSHA-256を検証してから展開します。元の画像やHTMLが欠けている場合は失敗します。
\n## Site edits\n\nPlace only the files you change in `site-overrides/` using their paths relative to the published site. For example, `site-overrides/assets/css/site.css` replaces `dist/assets/css/site.css` after the verified archive is restored. Commit the change to GitHub; a Git-connected Cloudflare Pages project will rebuild and publish it automatically. The original manga archive does not need to be re-uploaded for these edits.\n