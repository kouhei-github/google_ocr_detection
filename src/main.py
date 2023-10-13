import json
import os
from typing import Dict
from google.drive.google_drive_facade import GoogleDriveFacade
from google.document.google_document_facade import GoogleDocumentFacade
from ocr.nagamatsu_deeplearning_v2 import NagamatsuDeepLearning

def lambda_handler(event, context) -> Dict[str, str]:
    # pdf_file: str, google_drive_id: str, service_account_file: str
    service_account_file = event["service_account_file"]
    pdf_file = event["pdf_file"]
    google_drive_id = event["google_drive_id"]

    # アクセス許可のスコープを指定します。(ここではGoogle Driveへのフルアクセス権限)
    drive_scopes = ['https://www.googleapis.com/auth/drive']
    # Google認証情報が含まれている.json形式のファイルへのパスを指定します。
    secret_file = os.path.join(service_account_file)
    # GoogleDriveFacadeクラスのインスタンスを作成します。それによりGoogle Driveへの操作を行うことが可能となります。
    drive_facade = GoogleDriveFacade(secret_file, drive_scopes)
    # Google Driveにファイルをアップロードします。返値はアップロードしたファイルのIDです。
    # 第1引数はアップロードするファイルへのパス、第2引数はアップロードしたファイルを保存するフォルダのID。
    file_id = drive_facade.upload_to_google_drive(pdf_file, google_drive_id)
    # Google Documentへのアクセス許可のスコープを指定します。
    document_scope = ['https://www.googleapis.com/auth/documents']
    # GoogleDocumentFacadeクラスのインスタンスを作成します。それによりGoogle Documentへの操作を行うことが可能となります。
    document_facade = GoogleDocumentFacade(secret_file, document_scope)
    # Google Documentの内容を取得します。ここでは先ほどアップロードしたファイルのIDを使用します。
    document_text = document_facade.get_contents(file_id)

    # NagamatsuDeepLearningインスタンスを作成
    # 引数にはドキュメントのテキストが含まれています
    deep_docs = NagamatsuDeepLearning(document_text)

    # Google Driveから特定のドキュメントを削除します
    drive_facade.delete_object(file_id)

    # NagamatsuDeepLearningインスタンスから情報を抽出し、
    # それを辞書形式で返します。
    return {
        "kana": deep_docs.get_kana_from_pdf(),  # ドキュメントからローマ字の名前を抽出します
        "gender": deep_docs.get_gender_from_pdf(),  # ドキュメントから性別を抽出します
        "birthday": deep_docs.get_birth_day_from_pdf(),  # ドキュメントから生年月日を抽出します
        "age": deep_docs.age,  # NagamatsuDeepLearningインスタンスから年齢を抽出します
        "email": deep_docs.get_email_from_pdf(),  # ドキュメントから電子メールのアドレスを抽出します
        "phone": deep_docs.get_phone_number_from_pdf(),  # ドキュメントから電話番号を抽出します
    }


if __name__ == "__main__":
    payload = {
        "service_account_file": "./config/google-docs-account.json",
        "pdf_file": "https://www.kansaigaidai.ac.jp/asp/img/pdf/82/7a79c35f7ce0704dec63be82440c8182.pdf",
        "google_drive_id": "XXXXXXXXXXXXXXXXXXXXXX"
    }
    data = lambda_handler(
        payload,
        {},
    )
    print(data)
