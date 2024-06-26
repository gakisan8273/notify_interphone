# notify_interphone

## このリポジトリ何？

GPIO に入力があったら LINE API で push メッセージを送ります。
`.env` に環境変数を設定し、任意のユーザ ID や送信メッセージを設定してください。

**インターホンが鳴ったら LINE に通知する仕組み** としての使用方法を Qiita に書きました。

https://qiita.com/gakisan8273/items/47fc00da4a3b5588f25e

## 使い方

まず .env を生成してください。

```
$ cp .env.example .env
```

次に環境変数の設定をしてください。

### 環境変数設定

#### USER_IDS

LINE ユーザ ID を設定します。
複数設定する場合は`,`で区切ってください。
ここで指定した ID に push メッセージが送信されます。

#### ACCESS_TOKEN

アクセストークンを設定します。
長期でも短期でもどちらでもいいです。

#### MESSAGE

push メッセージの本文を設定します。

#### SLEEP_TIME_SEC

push メッセージを送信した後、何秒待機するかを設定します。
