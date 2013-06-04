Zaffy
=====

Zaffy は yaml フォーマットでテストシナリオを記述できる機能テストツールです。Web や Database、ファイルシステムなどの外部システムに対する入力とその応答検証を共通の形式で記述することができます。種々の機能を組み合わせた自動化ツールとして使うことも可能です。

詳しくはこちら
http://tomoemon.github.com/zaffy/

Setup
-------------

### Requirements

* python 2.6 or later
* setuptools (package management tool for python)

        # on python 2.x
        wget http://peak.telecommunity.com/dist/ez_setup.py
        sudo python ez_setup.py
        sudo easy_install pip

* required packages

        sudo pip install -r required_packages.txt

* optional packages
 * if you'd like to parse XML/HTML (used by `asxml`, `ashtml`, `xpath` filter)

            #   on linux
            #     (ubuntu) sudo apt-get install python-dev libxslt-dev
            #     (centos) sudo yum install python-devel libxslt-devel
            #   on windows http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
            sudo pip instal lxml

 * if you'd like to query SQL (used by `sql` action)

            sudo pip install PyMySQL

 * if you'd like to connect with SSH (used by `ssh` action)

            #   on windows http://www.voidspace.org.uk/python/modules.shtml#pycrypto
            sudo pip install ssh


Usage
--------------
    $ python lib/zaffy.py sample_scenario/httpTest.yml
      # using config file: zaffy.yml
    1..1
    ok 1 - HTTP テスト

    1 test succeeded (1.00 sec elapsed)

標準でTAP(Test Anything Protocol)形式による出力を行います


Example
--------------
# http test
    - HTTP テスト
    - action: http.get
      url: http://yahoo.co.jp/
      params:
        hoge: 10
        fuga: piyo
      assert:
        - out.status == 200
        - out.content|length > 1000

    - action: http.post
      url: http://localhost:8000/
      params:
        pagesize: <<last.res.content|length>>

# sql test
    - SQL テスト
    - action: sql.select
      driver: mysql
      host: localhost
      db: user_db
      user: root
      password: hogehoge
      sql: select * from user where user_id=1;
      assert:
       - >
        out.rows[0] ==
          [1, "nanoha", "2012-04-10 15:57:26"|todate, "2012-04-10 15:57:26"|todate]

    # preset 機能を使うことで接続情報などを省略したシンプルな記述が可能
    - action: sql.update
      sql: insert into user (user_id, name) values (10, "hoge")

# shell test
    - SHELL テスト
    - action: shell
      cmd: wc -l output.txt
      assert:
        - out.returncode == 0
        - out.stdout.strip() == "50 output.txt"

