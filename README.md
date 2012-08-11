Zaffy
=====

Zaffy は yaml ベースのシンプルなルールでテストシナリオを記述することができる機能テストツールです。HTTP や SQL、ファイルシステムなど「外部」システムに対する入力とその応答を簡単にテストすることができます。

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

