# insta-influencer-api

## 開発サーバーの起動
### コンテナのビルド
```sh
docker compose build
```

### コンテナの起動
```sh
docker compose up -d
```

### コンテナの停止と削除
```sh
docker compose down
```

### テストの実行
```sh
docker compose exec web python -m pytest -v
```