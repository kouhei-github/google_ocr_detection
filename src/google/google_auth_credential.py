import os
from google.oauth2 import service_account
from typing import List

class GoogleAuthCredential:
    """

    このクラスは Google API に対するリクエストの認証や認可に使用する Google 認証クレデンシャルを表します。

    引数
        secret_file (str)： サービスアカウントの認証情報を含む秘密ファイル JSON へのパス。
        scopes (リスト[str])： クレデンシャルのアクセスレベルを定義するスコープ文字列のリスト。

    属性：
        credentials (google.auth.credentials.クレデンシャル)： 認証されたクレデンシャルオブジェクト。
    """
    def __init__(self, secret_file: str, scopes: List[str]):
        secret_file = os.path.join(secret_file)
        self.credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
