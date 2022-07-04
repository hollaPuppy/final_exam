"""init

Revision ID: 4d8011806ae6
Revises: 0f959aa12006
Create Date: 2022-06-24 19:50:43.243003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d8011806ae6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE achievements_list (
                  achv_id integer NOT NULL,
                  achv_name varchar(255) NOT NULL,
                  achv_req integer NOT NULL,
                  achv_is_limit boolean NOT NULL,
                  achv_date_end_if_limit date DEFAULT NULL,
                  PRIMARY KEY (achv_id));""")
    op.execute("""CREATE TABLE db_options (
                  option_id integer NOT NULL,
                  option_name varchar(255) NOT NULL,
                  option_value varchar(255) NOT NULL,
                  PRIMARY KEY (option_id));""")
    op.execute("""CREATE TABLE lobbies (
                  lob_id integer NOT NULL,
                  lob_is_closed boolean NOT NULL,
                  lob_pass_code varchar(255) DEFAULT NULL,
                  lob_name varchar(255) NOT NULL,
                  lob_create_date timestamp NOT NULL,
                  lob_is_full boolean NOT NULL,
                  PRIMARY KEY (lob_id));""")
    op.execute("""CREATE TABLE notifications (
                  ntfct_id integer NOT NULL,
                  ntfct_title varchar(255) NOT NULL,
                  ntfct_text varchar(255) NOT NULL,
                  ntfct_date timestamp NOT NULL,
                  PRIMARY KEY (ntfct_id));""")
    op.execute("""CREATE TABLE puzzles_list (
                  puz_id integer NOT NULL,
                  puz_name varchar(255) NOT NULL,
                  PRIMARY KEY (puz_id));""")
    op.execute("""CREATE TABLE users (
                  uid integer NOT NULL,
                  user_name varchar(255) NOT NULL,
                  user_email varchar(255) NOT NULL,
                  user_hash_pass varchar(255) NOT NULL,
                  user_active_time varchar(255) NOT NULL,
                  user_is_admin boolean NOT NULL,
                  PRIMARY KEY (uid));""")
    op.execute("""CREATE TABLE complete_achievements (
                  com_achv_id integer NOT NULL,
                  achv_id integer NOT NULL,
                  uid integer NOT NULL,
                  com_achv_receive_date timestamp NOT NULL,
                  PRIMARY KEY (com_achv_id),
                  CONSTRAINT complete_achievements_uid_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid),
                  CONSTRAINT complete_achievements_id_ach_achievements_list_id_ach_foreign FOREIGN KEY (achv_id) 
                  REFERENCES achievements_list (achv_id));""")
    op.execute("""CREATE TABLE lobbies_users (
                  lob_usr_id integer NOT NULL,
                  uid integer NOT NULL,
                  lob_is_cap boolean NOT NULL,
                  lob_id integer NOT NULL,
                  PRIMARY KEY (lob_usr_id),
                  CONSTRAINT lobby_user_list_uid_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid),
                  CONSTRAINT lobbies_users_lob_id_lobbies_lob_id_foreign FOREIGN KEY (lob_id) 
                  REFERENCES lobbies (lob_id));""")
    op.execute("""CREATE TABLE notifications_users (
                  ntfct_usr_id integer NOT NULL,
                  ntfct_id integer NOT NULL,
                  uid integer NOT NULL,
                  ntfct_opened boolean NOT NULL,
                  PRIMARY KEY (ntfct_usr_id),
                  CONSTRAINT notifications_users_ntfct_id_notifications_ntfct_id_foreign FOREIGN KEY (ntfct_id) 
                  REFERENCES notifications (ntfct_id),
                  CONSTRAINT notifications_users_uid_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid));""")
    op.execute("""CREATE TABLE process_achievements (
                  prc_achv_id integer NOT NULL,
                  achv_id integer NOT NULL,
                  uid integer NOT NULL,
                  prc_achv_pass integer NOT NULL,
                  PRIMARY KEY (prc_achv_id),
                  CONSTRAINT process_achievements_uid_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid),
                  CONSTRAINT process_achievements_id_ach_achievements_list_id_ach_foreign FOREIGN KEY (achv_id) 
                  REFERENCES achievements_list (achv_id));""")
    op.execute("""CREATE TABLE saves (
                  save_id integer NOT NULL,
                  uid integer NOT NULL,
                  save_date timestamp NOT NULL,
                  save_name varchar(255) NOT NULL,
                  PRIMARY KEY (save_id),
                  CONSTRAINT saves_id_save_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid));""")
    op.execute("""CREATE TABLE complete_puzzles (
                  com_puz_id integer NOT NULL,
                  puz_id integer NOT NULL,
                  com_puz_receive_date timestamp NOT NULL,
                  save_id integer NOT NULL,
                  PRIMARY KEY (com_puz_id),
                  CONSTRAINT complete_puzzles_save_id_saves_save_id_foreign FOREIGN KEY (save_id) 
                  REFERENCES saves (save_id),
                  CONSTRAINT complete_puzzles_puz_id_puzzles_list_puz_id_foreign FOREIGN KEY (puz_id) 
                  REFERENCES puzzles_list (puz_id));""")
    op.execute("""CREATE TABLE coordinations (
                  coord_id integer NOT NULL,
                  coord_pos varchar(255) NOT NULL,
                  coord_rot varchar(255) NOT NULL,
                  save_id integer NOT NULL,
                  PRIMARY KEY (coord_id),
                  CONSTRAINT coordinations_save_id_saves_save_id_foreign FOREIGN KEY (save_id) 
                  REFERENCES saves (save_id));""")


def downgrade() -> None:
    pass
