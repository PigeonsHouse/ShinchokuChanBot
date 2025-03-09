# 進捗ちゃんBot

## 進捗ちゃんBotとは？
https://qiita.com/PigeonsHouse/items/9d86e35dbb6550d8f853

## 環境構築
### .envの作成
`.env.sample` から `.env` を作る。

```sh
cp .env.sample .env
```

適宜変数を埋める。

#### 各変数の取得方法
- `POSTGRES_HOST`
  - dockerで動かす場合は`db`で良い。
- `POSTGRES_XXX`
  - dockerで動かす場合は何でも良い。
- `DATABASE_URL`
  - `POSTGRES_XXX` を利用する場合は空欄で良い。herokuなど `DATABASE_URL` の変数で接続情報を受け取る場合のためのもの。
- `TOKEN`
  - [DiscordのApplicationのページ](https://discord.com/developers/applications)からBotのTokenをコピーしてくる。本家のトークンが欲しい場合は[鳩屋敷](https://x.com/PigeonsHouse)に連絡してください。

### docker を動かす

```sh
docker compose up -d
```

## 動かす際の注意
Discordの開発ポータルページの `Bot` の下部、`Privileged Gateway Intents` の設定をONにしないと動かない場合がある。
