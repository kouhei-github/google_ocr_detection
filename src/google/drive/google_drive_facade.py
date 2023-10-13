import uuid
import requests
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.google_auth_credential import GoogleAuthCredential
from typing import List

class GoogleDriveFacade(GoogleAuthCredential):
    """

    GoogleDriveFacade クラスは GoogleAuthCredential のサブクラスで、 Google ドライブからファイルをアップロードしたり削除したりするためのメソッドを提供します。

    使用法
        GoogleDriveFacade クラスのオブジェクトを secret_file および scopes 引数とともにインスタンス化します。これらの引数はスーパークラスのコンストラクタ GoogleAuthCredential に渡されます。

        例
            facade = GoogleDriveFacade(secret_file='path/to/secret_file.json', scopes=['scope1', 'scope2'])

        次にupload_to_google_driveメソッドでGoogle Driveにファイルをアップロードします。このメソッドには2つの引数が渡されます：
            - file_name: アップロードするファイルの名前。
            - drive_id: アップロードするファイルの名前： ファイルをアップロードするドライブのID。

        例
            uploaded_file_id = facade.upload_to_google_drive(file_name='file.txt', drive_id='drive_id')

        このメソッドは、アップロードされたファイルのIDを返します。

        Google Driveからオブジェクトを削除するにはdelete_objectメソッドを使用します。このメソッドには引数が1つ渡されます：
            - drive_id： 削除するオブジェクトの ID。

        例
            facade.delete_object(drive_id='drive_id')

        delete_objectメソッドは値を返さないことに注意してください。

    属性
        - service： Google Drive API とのやりとりに使用するサービスオブジェクト。

    メソッド：
        - upload_to_google_drive(file_name: str, drive_id: str) -> str：
            Google Drive にファイルをアップロードする。

        - delete_object(drive_id: str)：
            Google Drive からオブジェクトを削除する。

    """
    def __init__(self, secret_file: str, scopes: List[str]):
        super().__init__(secret_file, scopes)
        # configure
        self.service = build('drive', 'v3', credentials=self.credentials)


    def upload_to_google_drive(self, url: str, drive_id: str) -> str:
        """
        Google Drive にファイルをアップロードする。

        引数
            url (str)： アップロードするPDFファイルのURL。
            drive_id (str)： ファイルをアップロードするドライブのID。

        戻り値
            str： アップロードされたファイルのID。

        """
        response = requests.get(url)
        file_data = io.BytesIO(response.content)
        file_meta_data = {
            'name': str(uuid.uuid4()),
            'parents': [drive_id],
            'mimeType': 'application/vnd.google-apps.document'
        }
        media = MediaIoBaseUpload(file_data,  mimetype='application/pdf', resumable=True)
        file = self.service.files().create(
            body=file_meta_data,
            media_body=media,
            fields="id").execute()

        return file.get("id")


    def delete_object(self, drive_id: str):
        """
        Google Drive からオブジェクトを削除します。

        引数
            drive_id (str)： 削除するオブジェクトの ID。

        """
        self.service.files().delete(fileId=drive_id).execute()
