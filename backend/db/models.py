# app/models/match.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Enum, UniqueConstraint

db = SQLAlchemy()

class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.BigInteger, primary_key=True)

    # identifiers
    division_code = db.Column(db.String(16), nullable=False)
    season        = db.Column(db.String(12), nullable=True)

    # who/when
    match_date    = db.Column(db.Date, nullable=False)
    kickoff_time  = db.Column(db.Time, nullable=True)  # local time from CSV
    home_team     = db.Column(db.String(64), nullable=False)
    away_team     = db.Column(db.String(64), nullable=False)
    referee_name  = db.Column(db.String(64), nullable=True)

    # full-time result
    ft_home_goals = db.Column(db.SmallInteger, nullable=True)
    ft_away_goals = db.Column(db.SmallInteger, nullable=True)
    ft_result     = db.Column(Enum("H", "D", "A", name="result_enum"), nullable=True)

    # half-time
    ht_home_goals = db.Column(db.SmallInteger, nullable=True)
    ht_away_goals = db.Column(db.SmallInteger, nullable=True)
    ht_result     = db.Column(Enum("H", "D", "A", name="ht_result_enum"), nullable=True)

    # team stats
    shots_home            = db.Column(db.SmallInteger, nullable=True)
    shots_away            = db.Column(db.SmallInteger, nullable=True)
    shots_on_target_home  = db.Column(db.SmallInteger, nullable=True)
    shots_on_target_away  = db.Column(db.SmallInteger, nullable=True)
    fouls_committed_home  = db.Column(db.SmallInteger, nullable=True)
    fouls_committed_away  = db.Column(db.SmallInteger, nullable=True)
    corners_home          = db.Column(db.SmallInteger, nullable=True)
    corners_away          = db.Column(db.SmallInteger, nullable=True)
    yellow_cards_home     = db.Column(db.SmallInteger, nullable=True)
    yellow_cards_away     = db.Column(db.SmallInteger, nullable=True)
    red_cards_home        = db.Column(db.SmallInteger, nullable=True)
    red_cards_away        = db.Column(db.SmallInteger, nullable=True)

    __table_args__ = (
        # Avoid duplicate rows per fixture
        UniqueConstraint("match_date", "home_team", "away_team", name="uq_match_unique"),
        # Keep integer stats non-negative if provided
        CheckConstraint("ft_home_goals >= 0", name="ck_ft_hg_nonneg"),
        CheckConstraint("ft_away_goals >= 0", name="ck_ft_ag_nonneg"),
    )
