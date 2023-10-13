from google.google_auth_credential import GoogleAuthCredential
from googleapiclient.discovery import build
from typing import List

class GoogleDocumentFacade(GoogleAuthCredential):
    """

    GoogleDocumentFacade

    Google Documents を操作するためのメソッドを提供するクラス。

    を継承します：
        GoogleAuthCredential

    引数
        secret_file (str)： Google API 用の認証情報を含む秘密ファイルへのパス。
        scopes (リスト[str])： API アクセスを許可するスコープのリスト。


    メソッド
        __init__(self, secret_file: str, scopes: List[str])
        get_contents(self, drive_id: str) -> str

    属性
        サービス

    """
    def __init__(self, secret_file: str, scopes: List[str]):
        super().__init__(secret_file, scopes)
        # configure
        self.service = build('docs', 'v1', credentials=self.credentials)


    def get_contents(self, drive_id: str) -> str:
        """
        引数
            drive_id (str)： Google Drive ドキュメントの ID。

        戻り値
            str： ドキュメントの全文。

        """
        document = self.service.documents().get(
            documentId=drive_id
        ).execute()
        full_text = ""

        # ドキュメントの本文内をループして各要素を取得します
        for content in document['body']['content']:
            if 'paragraph' in content:
                for paragraph_element in content['paragraph']['elements']:
                    if 'textRun' in paragraph_element:
                        full_text += paragraph_element['textRun']['content']

        return full_text
