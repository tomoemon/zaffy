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
        pagesize: <<last.result.content|length>>

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

