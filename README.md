Zaffy
=====

Zaffy は yaml ベースのシンプルなフォーマットでテストシナリオを記述できる機能テストツールです。Web や Database、ファイルシステムなどの「外部システム」に対する入力とその応答チェックを共通の形式で記述することができます。種々の機能を組み合わせた自動化ツールとして使うことも可能です。

シナリオ記述例
--------------
#http test
    - action: http.get
      url: http://yahoo.co.jp/
      params:
        hoge: 10
        fuga: piyo
      assert:
        - res.status == 200
        - res.content|length > 1000

    - action: http.post
      url: http://localhost:8000/
      params:
        pagesize: <<last.res.content|length>>

#sql test
    - action: sql.select
      driver: mysql
      host: localhost
      db: user_db
      user: root
      password: hogehoge
      sql: select * from user where user_id=1;
      assert:
       - >
        res.rows[0] ==
          [1, "nanoha", "2012-04-10 15:57:26"|todatetime, "2012-04-10 15:57:26"|todatetime]

    # preset 機能を使うことで接続情報などを省略したシンプルな記述が可能
    - action: sql.update
      sql: insert into user (user_id, name) values (10, "hoge")

# shell test
    - action: shell
      cmd: wc -l output.txt
      assert:
        - res.returncode == 0
        - res.stdout.strip() == "50 output.txt"

アクション一覧
--------------
* http
    * get
    * post
    * put
    * delete
    * head
    * patch

* sql
    * select…selectした結果の1行1行をリスト形式で取得する
    * selectdict…selectした結果の1行1行をカラム名と対応した辞書形式で取得する
    * update…insert文やupdate文などの更新系SQLを実行する

* shell
    * run(*)…デフォルトシェル経由でコマンドを実行する

* file
    * copy…ファイルをコピーする
    * remove…ファイルを削除する
    * rename…ファイル名を変更する
    * write…ファイルに書き込みを行なう
    * @exists…ファイルの存在をチェックする
    * @writable…ファイルの書き込み権限をチェックする
    * @readable…ファイルの読み込み権限をチェックする
    * @executable…ファイルの実行権限をチェックする
    * @size…ファイルサイズを取得する
    * @access_time…ファイルの最終アクセス時刻を取得する
    * @update_time…ファイルの最終更新時刻を取得する
    * @create_time…ファイルの作成時刻を取得する
    * @read…ファイルの内容を取得する

* sleep
    * sleep(*)…指定した時間（ミリ秒単位）処理を停止する

* env
    * @NAME…指定した環境変数を取得する

* const
    * set…他のアクションで使用できる定数を定義する
    * push
    * pop

* debug
    * print(*)…他のアクションの実行結果などを標準出力に出力する

* preset
    * アクション名…指定したアクションのパラメータテンプレートを作成する

* require
    * require(*)…他のテストシナリオの内容を実行する

