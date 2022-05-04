from app.db import DB

from app.routes.schemas.notifications import Notifications_List


async def get_ntfct_list_by_username(username: str) -> list:
    query = f"""
         select n.ntfct_title, n.ntfct_text, n.ntfct_date, nu.ntfct_opened
         from notifications n
         join notifications_users nu on nu.ntfct_id=n.ntfct_id
         where nu.uid=(select uid from users where username = $1)
         order by n.ntfct_date
       """
    result_list = await DB.conn.fetch(query, username)
    return list(map(lambda row: Notifications_List(**row).dict(), result_list))


async def get_ntfct_id_by_title_text_date(ntfct_title: str, ntfct_text: str, ntfct_date: str) -> list:
    query = f"""
         select ntfct_id
         from notifications 
         where ntfct_title = $1
         and ntfct_text = $2
         and ntfct_date = $3
       """
    return await DB.conn.fetchval(query, ntfct_title, ntfct_text, ntfct_date)


# __________POST____________


async def post_ntfct_body(ntfct_title: str, ntfct_text: str, ntfct_date: str) -> str:
    query = f"""
         insert into notifications(ntfct_title, ntfct_text, ntfct_date) 
         values ($1, $2, $3)
        """
    await DB.conn.execute(query, ntfct_title, ntfct_text, ntfct_date)


async def post_ntfct_for_user(ntfct_id: int, uid: int, ntfct_opened: bool) -> list:
    query = f"""
         insert into notifications_users(ntfct_id, uid, ntfct_opened) 
         values ($1, $2, $3)
       """
    await DB.conn.execute(query, ntfct_id, uid, ntfct_opened)


async def post_ntfct_for_all(list_ntfct_uid: list) -> list:
    query = f"""
         insert into notifications_users(ntfct_id, uid, ntfct_opened) 
         values ($1, $2, $3)
       """
    await DB.conn.executemany(query, list_ntfct_uid)


# __________PuT____________

async def put_ntfct_for_user(ntfct_id: int, username: str) -> list:
    query = f"""
         update notifications_users
         set ntfct_opened = true
         where ntfct_id = $1
         and uid = (select uid from users where username = $2)
       """
    await DB.conn.execute(query, ntfct_id, username)