from app.queries.queries_users import get_user_list_by_active_time, \
    get_email_check_exist, \
    get_uid_check_exist, \
    get_user_password, \
    get_user_name_check_exist, \
    get_uid_list, \
    get_user_by_uid_check, \
    get_uid_by_user_name, \
    get_user_name_by_uid, \
    get_user_email_by_uid, \
    get_user_info_by_uid
import pytest

from .db import DB


@pytest.fixture
async def init_db():
    await DB.connect()
    yield
    await DB.close()


@pytest.mark.asyncio
async def test_get_top_players_by_active_time(init_db):
    ok = await get_user_list_by_active_time()
    assert ok == [{'user_name': 'Admin', 'user_active_time': '0'},
                  {'user_name': 'TestUser11', 'user_active_time': '639'}]


@pytest.mark.asyncio
async def test_get_email_check_exist(init_db):
    check = await get_email_check_exist('admin@mail.ru')
    assert check is True


@pytest.mark.asyncio
async def test_get_uid_check_exist(init_db):
    check = await get_uid_check_exist(11)
    assert check is True


@pytest.mark.asyncio
async def test_get_user_password(init_db):
    password = await get_user_password('TestUser11')
    assert password == '{"salt":"c65a93e8b7caae850446cfcd0135a28d6dc5673403a8312e36371c4a2fd95efd",' \
                       '"key":"d06daa55ae261ecb893bf98f6b24d207fee29a3d2da123c623afd7eff7617e88"}'


@pytest.mark.asyncio
async def test_get_user_name_check_exist(init_db):
    check = await get_user_name_check_exist('TestUser11')
    assert check is True


@pytest.mark.asyncio
async def test_get_uid_list(init_db):
    uid_list = await get_uid_list()
    assert uid_list == [{'uid': 11}, {'uid': 14}]


@pytest.mark.asyncio
async def test_get_user_by_uid_check(init_db):
    check = await get_user_by_uid_check(11)
    assert check is True


@pytest.mark.asyncio
async def test_get_uid_by_user_name(init_db):
    check = await get_uid_by_user_name('TestUser11')
    assert check == 11


@pytest.mark.asyncio
async def test_get_user_name_by_uid(init_db):
    check = await get_user_name_by_uid(11)
    assert check == 'TestUser11'


@pytest.mark.asyncio
async def test_get_user_email_by_uid(init_db):
    check = await get_user_email_by_uid(11)
    assert check == 'roki218@mail.ru'


@pytest.mark.asyncio
async def test_get_user_info_by_uid(init_db):
    check = await get_user_info_by_uid(11)
    assert check == {'user_name': 'TestUser11', 'user_email': 'roki218@mail.ru',
                     'user_active_time': {'hours': 0, 'minutes': 10, 'seconds': 39}}

