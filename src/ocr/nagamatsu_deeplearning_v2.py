from datetime import datetime
import re

class NagamatsuDeepLearning:
    """
    NagamatsuDeepLearningクラスは、PDF文書から情報を抽出するためのディープラーニングモデルを表します。

    メソッド
        - __init__(self, document: str)： ドキュメント文字列でNagamatsuDeepLearningインスタンスを初期化する。
        - get_kana_from_pdf(self) -> str： PDF文書からかなを取り出す。
        - get_gender_from_pdf(self) -> str： PDF 文書から性別情報を抽出します。
        - get_birth_day_from_pdf(self) -> str： PDF ドキュメントから誕生日を抽出します。
        - get_email_from_pdf(self) -> str： PDF ドキュメントからメールアドレスを抽出します。
        - get_phone_number_from_pdf(self) -> str： PDF ドキュメントから電話番号を抽出します。
    Examples:
        deep_docs = NagamatsuDeepLearning("Sample Document")
        kana = deep_docs.get_kana_from_pdf()
        gender = deep_docs.get_gender_from_pdf()
        birth_day = deep_docs.get_birth_day_from_pdf()
        email = deep_docs.get_email_from_pdf()
        phone_number = deep_docs.get_phone_number_from_pdf()
    """
    def __init__(self, document: str):
        self.document = document
        self.age = 0

    def get_kana_from_pdf(self) -> str:
        """

        PDF文書からかなを取得します。

        PDF文書に特定の文字列("個人情報詳細 "と "性別:")が含まれているかどうかをチェックします。

        パラメータ
        - self (NagamatsuDeepLearning)： NagamatsuDeepLearningクラスのインスタンス。

        戻り値
        - str： PDF文書から抽出されたカナ。必要な文字列が見つからない場合は空文字列が返される。

        """
        if not ("個人情報詳細" in self.document and "性別:" in self.document):
            return ""

        text_replace = self.document.replace("（", "%%%%%%%%%%").replace("）", "%%%%%%%%%%")
        name_split = text_replace.split("%%%%%%%%%%")
        kana = ""
        for i in range(4):
            if i % 2 != 0:
                kana = kana + " " + name_split[i]
        return kana.lstrip()

    def get_gender_from_pdf(self) -> str:
        """
        このメソッド get_gender_from_pdf は、PDF 文書から性別情報を抽出するために使用します。

        パラメータ
        - self: NagamatsuDeepLearningクラスのインスタンス。

        戻り値
        - str: 抽出された性別情報。これは "男性"、"女性"、または文書中に性別情報がない場合は空文字列のいずれかである。

        使用例
            deep_docs = NagamatsuDeepLearning("これは性別情報を含むサンプル文書です: 性別: 男性")
            gender = deep_docs.get_gender_from_pdf()
            print(gender) # 出力： "男性"
        """
        if "性別: 男性" in self.document:
            return "男性"
        elif "性別: 女性" in self.document:
            return "女性"
        else:
            return ""

    def get_birth_day_from_pdf(self):
        """
        PDF文書から誕生日を取得します。

        誕生日が見つからない場合は空文字列を返します。

        パラメータ
        - self (NagamatsuDeepLearning)： メソッドが呼び出されるNagamatsuDeepLearningのインスタンス。

        戻り値
        - str： str: 誕生日を 'YYYY/MM/DD' 形式の文字列で返す。
        """
        text = self.document.replace(" ", "")
        match = re.search('\d{4}-\d{1,2}-\d{1,2}', text)
        if match:
            birth_day = match.group(0)
            birth_date = datetime.strptime(birth_day, '%Y-%m-%d')

            self.age = self._get_age(birth_date)

            if not self.age >= 18:
                birth_day = ""
            return birth_day.replace("-", "/")
        else:
            return ""

    def get_email_from_pdf(self):
        """
        PDF 文書から電子メールアドレスを取得します。

        戻り値
            str： 文書内で見つかったメールアドレス。

        Example:
            >> pdf_doc = "This is a sample PDF document containing an email address test@example.com."
            >> dl = NagamatsuDeepLearning("XXXXXXXXX")
            >> email = dl.get_email_from_pdf()
            >> print(email)
            test@example.com
        """
        email_reg = r"[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*.)+[a-zA-Z]{2,}"
        email_match = re.search(email_reg, self.document)
        if email_match:
            return email_match.group(0)
        else:
            return ""

    def get_phone_number_from_pdf(self):
        """

        このメソッド `get_phone_number_from_pdf` は、PDF ドキュメントから電話番号を抽出するために使用します。このメソッドはパラメータをとらず、電話番号を文字列として返します。

        パラメータ
            このメソッドにはパラメータはありません。

        返り値
            - 文字列としての電話番号。ドキュメント内で有効な電話番号が見つかった場合、`080-4659-7272`という形式で返される。複数の電話番号が見つかった場合は、最初のものだけが返される。有効な電話番号が見つからない場合は、空の文字列が返される。
        Example usage:
            nagamatsu_dl = NagamatsuDeepLearning("XXXXXXXXX")
            phone_number = nagamatsu_dl.get_phone_number_from_pdf()
            print(phone_number)

        """
        matches = []
        pattern = ["080", "090", "070"]
        str_text = self.document.replace(".com", "\n").replace(".jp", "\n")
        sentences = str_text.split("\n")
        for sentence in sentences:
            word = re.sub(r'\s+', '', sentence)
            word = word.replace("+81", "0")
            word = re.sub('-', '', word)
            if len(word) != 11 or not word.isdigit():
                continue

            start = word[0:3]  # 080
            middle = word[3:7]  # 4659
            last = word[7:11]  # 7272
            if start not in pattern:
                continue

            phone = f"{start}-{middle}-{last}"  # 080-4659-7272
            if re.match(r"^0[789]0-[0-9]{4}-[0-9]{4}$", phone):
                matches.append(phone.replace("-", ""))

        if len(matches) == 1:
            return matches[0]

        return ""

    @staticmethod
    def _get_age(birth_date: datetime):
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
