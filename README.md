# 恋のあとがき。／あと1ページの恋。

公式作品サイトの静的公開リポジトリです。完成済み作品とサイト一式を、ハッシュ検証後に `dist/` へ復元します。

## Cloudflare Pages 自動デプロイ

このリポジトリには GitHub Actions から Wrangler で Pages に公開する設定があります。今のDirect Uploadプロジェクトを保ったまま、GitHubへの変更を同じPagesプロジェクトへ反映できます。

最初の一度だけ、次を設定してください。

1. Cloudflareで、Account権限のカスタムAPIトークンを作り、権限を `Cloudflare Pages: Edit` に限定する。
2. GitHubリポジトリの Settings → Secrets and variables → Actions に、`CLOUDFLARE_API_TOKEN` と `CLOUDFLARE_ACCOUNT_ID` を登録する。トークンをチャットに貼らない。
3. 同じ画面の Variables に `CF_PAGES_DEPLOY_ENABLED=true` を登録する。

以後、`main` へのコミットでGitHub Actionsがサイトを復元・検証し、`koinoatogaki` Pagesプロジェクトへデプロイします。Actions画面で実行結果を確認できます。

Cloudflare PagesのGit integrationをすでに設定している場合は、GitHub Actionsでの二重デプロイを避けるため、この方法を有効にする前にどちらか一方を選んでください。Direct Uploadの既存プロジェクトには後からGit integrationを追加できないため、Wrangler経由のこの方法は既存URLを保つための選択肢です。

## Local build

Python 3が必要です。

```sh
python3 restore_site.py
```

ビルドは全分割データと完成アーカイブのSHA-256を検証してから展開します。

## Site edits

変更ファイルは `site-overrides/` に、公開サイト内と同じ相対パスで置きます。たとえば `site-overrides/assets/css/site.css` は、検証済みスナップショットを展開した後に `dist/assets/css/site.css` へ重ねられます。変更後にGitHubへコミットすると、上記設定を有効にした場合Cloudflareへ自動反映されます。元の漫画アーカイブを編集のたびにアップロードする必要はありません。
