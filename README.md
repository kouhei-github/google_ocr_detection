# OCRを使用してPDFや画像を文字起こしする

## 1. 使い方

### 1.1. dockerイメージの作成
```shell
docker compose build
```

### 1.2. コンテナの起動
```shell
docker compose up -d
```

### 1.3 dockerコンテナの停止
```shell
docker compose down
```

---

## 2 AWS Lambdaへ デプロイ方法
```shell
sh image-refresh.sh
```

---

##  3. google-docs-account.jsonファイルの作成
```shell
touch src/config/google-docs-account.json
```

GCPで作成したservice-account.jsonファイルn内容を下記にコピーする。<br>
その際以下の権限を付与しておく。
1. **Google Docs API**
2. **Google Drive API**

---
