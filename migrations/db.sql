CREATE TABLE achievements_list (
  achv_id integer NOT NULL,
  achv_name varchar(255) NOT NULL,
  achv_req integer NOT NULL,
  achv_is_limit boolean NOT NULL,
  achv_date_end_if_limit date DEFAULT NULL,
  PRIMARY KEY (achv_id)
);

CREATE TABLE bd_options (
  id_option integer NOT NULL,
  name_option varchar(255) DEFAULT NULL,
  value_option varchar(255) NOT NULL,
  PRIMARY KEY (id_option)
);

CREATE TABLE puzzles_list (
  puz_id integer NOT NULL,
  puz_name varchar(255) NOT NULL,
  PRIMARY KEY (puz_id)
);

CREATE TABLE users (
  uid integer NOT NULL,
  username varchar(255) DEFAULT NULL,
  email varchar(255) NOT NULL,
  hash_pass varchar(255) NOT NULL,
  active_time varchar(255) DEFAULT NULL,
  PRIMARY KEY (uid)
);

CREATE TABLE complete_achievements (
  com_achv_id integer NOT NULL,
  achv_id integer NOT NULL,
  uid integer NOT NULL,
  receive_date timestamp NOT NULL,
  PRIMARY KEY (com_achv_id),
  CONSTRAINT complete_achievements_uid_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid),
  CONSTRAINT complete_achievements_id_ach_achievements_list_id_ach_foreign FOREIGN KEY (achv_id) REFERENCES achievements_list (achv_id)
);

CREATE TABLE messages (
  msg_id integer NOT NULL,
  sender_uid integer NOT NULL,
  recipient_uid integer NOT NULL,
  msg_text varchar(255) NOT NULL,
  msg_time varchar(255) NOT NULL,
  PRIMARY KEY (msg_id),
  CONSTRAINT messages_uid_sender_users_uid_foreign FOREIGN KEY (sender_uid) REFERENCES users (uid),
  CONSTRAINT messages_uid_recipient_users_uid_foreign FOREIGN KEY (recipient_uid) REFERENCES users (uid)
);

CREATE TABLE process_achievements (
  prc_achv_id integer NOT NULL,
  achv_id integer NOT NULL,
  uid integer NOT NULL,
  achv_pass integer NOT NULL,
  PRIMARY KEY (prc_achv_id),
  CONSTRAINT process_achievements_uid_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid),
  CONSTRAINT process_achievements_id_ach_achievements_list_id_ach_foreign FOREIGN KEY (achv_id) REFERENCES achievements_list (achv_id)
);

CREATE TABLE saves (
  save_id integer NOT NULL,
  uid integer NOT NULL,
  save_date timestamp NOT NULL,
  save_name varchar(255) NOT NULL,
  puz_id integer NOT NULL,
  PRIMARY KEY (save_id),
  CONSTRAINT saves_id_save_users_uid_foreign FOREIGN KEY (uid) REFERENCES users (uid)
);

CREATE TABLE complete_puzzles (
  com_puz_id integer NOT NULL,
  puz_id integer NOT NULL,
  receive_date timestamp NOT NULL,
  save_id integer NOT NULL,
  PRIMARY KEY (com_puz_id),
  CONSTRAINT complete_puzzles_save_id_saves_save_id_foreign FOREIGN KEY (save_id) REFERENCES saves (save_id),
  CONSTRAINT complete_puzzles_puz_id_puzzles_list_puz_id_foreign FOREIGN KEY (puz_id) REFERENCES puzzles_list (puz_id)
);

CREATE TABLE coordinations (
  coord_id integer NOT NULL,
  coord_pos varchar(255) NOT NULL,
  coord_rot varchar(255) NOT NULL,
  save_id integer NOT NULL,
  PRIMARY KEY (coord_id),
  CONSTRAINT coordinations_save_id_saves_save_id_foreign FOREIGN KEY (save_id) REFERENCES saves (save_id)
);