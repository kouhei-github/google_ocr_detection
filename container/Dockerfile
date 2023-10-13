FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

# pipのアップデート
RUN pip install --upgrade pip

# pipでインストールしたいモジュールをrequirements.txtに記述しておいて、
# コンテナ内でpipにインストールさせる
# requirements.txtの書き方は[pip freeze]コマンドから参考に出来る
COPY ./container/requirements.txt ${LAMBDA_TASK_ROOT}
# アプリケーションコードをコンテナにコピー
COPY ./src ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt


CMD [ "main.lambda_handler" ]
