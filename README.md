This is a Personal Life Analytics app. The core functions separate into three main sections: personal development, finance tracking, and basic health (mental wellbeing, sleep, mood)
Setup: create the venv, run pip install -r requirements.txt, copy .env.example to .env and fill it in
Database: PostgresSQL
Project layout:
life-analytics/
├── README.md
├── requirements.txt
├── .env            (never committed)
├── .env.example
├── .gitignore / .gitattributes
├── sql/            001_initial_schema.sql, 002_...
├── src/
│   ├── db.py
│   ├── checkin.py
│   └── synthetic/generate.py
├── scripts/        check_db.py
├── notebooks/
└── tests/