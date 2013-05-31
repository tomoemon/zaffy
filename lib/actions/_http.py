# -*- coding: utf-8 -*-
import requests
from baseaction import BaseAction


class Http(BaseAction):
  """ Http アクション

  http リクエストを行なう

  .. code-block:: yaml

    - サンプルシナリオ

    - action: http.get
      url: http://yahoo.co.jp/
      params:
        id: userX
        pass: userPass
      headers:
        Referer: http://google.com/
      no_content: false
      assert:
        - res.content|length is gt 1000
  """
  def _create_result(self, response, no_content, binary_content, save_file):
    result = {}
    result['status'] = response.status_code
    result['headers'] = response.headers
    result['encoding'] = response.encoding
    result['cookies'] = response.cookies
    result['content'] = self._create_content(response, no_content, binary_content, save_file)
    return result

  def _create_content(self, response, no_content, binary_content, save_file):
    if not no_content:
      if save_file:
        # ファイルに保存する場合は自動的にバイナリ保存
        fp = open(save_file, "wb")
        for line in response.iter_content():
          fp.write(line)
        fp.close()
      else:
        return response.content if binary_content else response.text
    return ''

  def _http_method(self, method, url, auth, user, password, headers, cookies, params, data,
      no_content, binary_content, save_file, ssl_verify, allow_redirects, timeout):

    if auth == 'basic':
      auth = requests.auth.HTTPBasicAuth(user, password)
    elif auth == 'digest':
      auth = requests.auth.HTTPDigestAuth(user, password)

    r = getattr(requests, method)(url,
          headers=headers,
          cookies=cookies,
          params=params,
          auth=auth,
          data=data,
          verify=ssl_verify,
          allow_redirects=allow_redirects,
          timeout=timeout)
    self.output = self._create_result(r, no_content, binary_content, save_file)

  def do_delete(self, url, auth="", user="", password="", headers={}, cookies={}, params={}, data={},
      no_content=False, binary_content=False, save_file=None, ssl_verify=True, allow_redirects=True, timeout=None):
    """
    http delete (その他のメソッドもパラメータ、レスポンスは同じ)

    :param string url: URL (http, https スキーマの指定が必要)
    :param string auth: HTTP認証方法 ("basic", "digest")
    :param string user: HTTP認証ユーザ
    :param string password: HTTP認証パスワード
    :param dict headers: 送信する header
    :param dict cookies: 送信する cookie
    :param dict|string params: query string として送信するパラメータ。辞書形式ではなく a=10&b=20 形式の文字列で渡すことも可能
    :param dict|string data: message body として送信するパラメータ
    :param bool no_content: True: header のみを取得、False: content も取得
    :param bool binary_content: True: content をバイナリとして取得、False: header で指定された文字コードに従って decode
    :param string save_file: content をメモリ上に持たずに指定されたファイルに出力する (binary_content=Trueとして扱う)
    :param bool ssl_verify: True: https 通信の際に自己証明書が使われた場合は Error、False: 自己証明書を通す
    :param bool allow_redirects: True: 30x レスポンスに対して自動でリダイレクトする、False: リダイレクトしない
    :param float timeout: タイムアウト時間を秒単位で指定 (content のダウンロードに要する時間は除く)
    :return: - **status** (*int*) - http response status
             - **headers** (*dict*) - http response headers
             - **cookies** (*dict*) - http response cookies
             - **encoding** (*string*) - http header の content-type charset で指定された encoding
             - **content** (*string*) - http response body (no_content=True の時は '')
    """
    method_params = locals()
    del method_params['self']
    self._http_method("delete", **method_params)

  def do_get(self, url, auth="", user="", password="", headers={}, cookies={}, params={}, data={},
      no_content=False, binary_content=False, save_file=None, ssl_verify=True, allow_redirects=True, timeout=None):
    """ http get """
    method_params = locals()
    del method_params['self']
    self._http_method("get", **method_params)

  def do_post(self, url, auth="", user="", password="", headers={}, cookies={}, params={}, data={},
      no_content=False, binary_content=False, save_file=None, ssl_verify=True, allow_redirects=True, timeout=None):
    """ http post """
    method_params = locals()
    del method_params['self']
    self._http_method("post", **method_params)

  def do_put(self, url, auth="", user="", password="", headers={}, cookies={}, params={}, data={},
      no_content=False, binary_content=False, save_file=None, ssl_verify=True, allow_redirects=True, timeout=None):
    """ http put """
    method_params = locals()
    del method_params['self']
    self._http_method("put", **method_params)

  def do_head(self, url, auth="", user="", password="", headers={}, cookies={}, params={}, data={},
      no_content=False, binary_content=False, save_file=None, ssl_verify=True, allow_redirects=True, timeout=None):
    """ http head """
    method_params = locals()
    del method_params['self']
    self._http_method("head", **method_params)

  def do_patch(self, url, auth="", user="", password="", headers={}, cookies={}, params={}, data={},
      no_content=False, binary_content=False, save_file=None, ssl_verify=True, allow_redirects=True, timeout=None):
    """ http patch """
    method_params = locals()
    del method_params['self']
    self._http_method("patch", **method_params)

