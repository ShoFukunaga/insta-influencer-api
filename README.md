# insta-influencer-api

## 開発サーバーの起動
### コンテナのビルド
```sh
$ docker compose build
```

### コンテナの起動
```sh
# [localhost:8004/docs](http://localhost:8004/docs)でAPIドキュメント表示
$ docker compose up -d
```

![](/images/image.png) 

### CSVデータをRDBへ格納するコマンド
```sh
$ docker compose exec web python app/commands/create_posts_from_csv.py data/t_influencer_posts.csv
```

### テストの実行
```sh
$ docker compose exec web python -m pytest -v
```