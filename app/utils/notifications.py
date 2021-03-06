from ..queries.queries_users import get_uid_list, get_uid_by_user_name
from ..queries.queries_notifications import post_ntfct_for_user, \
                                            post_ntfct_for_all


async def get_list_uids_and_ntfct(ntfct_id: int, username: str) -> bool:
    if username == 'all':
        await post_ntfct_for_all(map(lambda row: (ntfct_id, row.get('uid'), False), await get_uid_list()))
    else:
        await post_ntfct_for_user(ntfct_id, await get_uid_by_user_name(username), False)
    return True


