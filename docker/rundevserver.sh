pip3 install -r requirements.txt

alembic upgrade head  # 追記

uvicorn main:app\
    --reload\
    --port 8000\
    --host 0.0.0.0\
    --log-level debug