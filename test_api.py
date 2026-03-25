# -*- coding:utf-8 -*-
"""
API 全功能测试用例
接口地址：POST http://127.0.0.1:8000/api/v1/service
运行方式：python test_api.py
依赖：pip install requests
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/service"

# ─────────────────────────────────────────────
# 全局状态（由测试流程动态填充）
# ─────────────────────────────────────────────
STATE = {
    "user_id_a": None,   # 用户 A 的 ID
    "user_id_b": None,   # 用户 B 的 ID
    "message_id": None,  # 测试消息 ID
    "moments_id": None,  # 测试朋友圈 ID
    "favorites_id": None # 测试收藏 ID
}

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

def req(payload: dict) -> dict:
    resp = requests.post(BASE_URL, json=payload, timeout=10)
    return resp.json()

def check(title: str, resp: dict, expect_result: str = "success", extra_checks: dict = None):
    """
    通用结果校验器
    - expect_result: "success" / "fail" / None（不检查 result 字段）
    - extra_checks: {key: expected_value}
    """
    ok = True
    if expect_result is not None and resp.get("result") != expect_result:
        ok = False
    if extra_checks:
        for k, v in extra_checks.items():
            if resp.get(k) != v:
                ok = False
    tag = PASS if ok else FAIL
    print(f"{tag} {title}")
    print(f"       响应: {json.dumps(resp, ensure_ascii=False)}\n")
    return ok

def sep(title: str):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


# ══════════════════════════════════════════════
# 1. 用户注册
# ══════════════════════════════════════════════
def test_register():
    sep("1. 用户注册")

    # 1-1 正常注册用户 A
    r = req({"operation": "register", "table_name": "user",
             "data": {"account": "test_user_a", "password": "pass123", "name": "用户A",
                      "status": "在线", "profile_picture_id": "1"}})
    if check("1-1 正常注册用户A", r):
        STATE["user_id_a"] = r.get("user_id")

    # 1-2 正常注册用户 B（缺省 status / profile_picture_id，应默认为空/0）
    r = req({"operation": "register", "table_name": "user",
             "data": {"account": "test_user_b", "password": "pass456", "name": "用户B"}})
    if check("1-2 正常注册用户B（缺省可选参数）", r):
        STATE["user_id_b"] = r.get("user_id")

    # 1-3 重复账号注册（应失败）
    r = req({"operation": "register", "table_name": "user",
             "data": {"account": "test_user_a", "password": "xxx", "name": "重复"}})
    check("1-3 重复账号注册（应失败）", r, expect_result="fail")

    # 1-4 缺少必需参数 name（应失败）
    r = req({"operation": "register", "table_name": "user",
             "data": {"account": "test_no_name", "password": "xxx"}})
    check("1-4 缺少必需参数 name（应失败）", r, expect_result="fail")

    # 1-5 缺少必需参数 password（应失败）
    r = req({"operation": "register", "table_name": "user",
             "data": {"account": "test_no_pass", "name": "xxx"}})
    check("1-5 缺少必需参数 password（应失败）", r, expect_result="fail")

    # 1-6 缺少必需参数 account（应失败）
    r = req({"operation": "register", "table_name": "user",
             "data": {"password": "xxx", "name": "xxx"}})
    check("1-6 缺少必需参数 account（应失败）", r, expect_result="fail")


# ══════════════════════════════════════════════
# 2. 用户登录
# ══════════════════════════════════════════════
def test_login():
    sep("2. 用户登录")

    # 2-1 正确账号密码登录
    r = req({"operation": "login", "table_name": "user",
             "data": {"account": "test_user_a", "password": "pass123"}})
    check("2-1 正确账号密码登录", r)

    # 2-2 错误密码（应失败）
    r = req({"operation": "login", "table_name": "user",
             "data": {"account": "test_user_a", "password": "wrong"}})
    check("2-2 错误密码（应失败）", r, expect_result="fail")

    # 2-3 不存在的账号（应失败）
    r = req({"operation": "login", "table_name": "user",
             "data": {"account": "not_exist_xyz", "password": "xxx"}})
    check("2-3 不存在账号（应失败）", r, expect_result="fail")


# ══════════════════════════════════════════════
# 3. 个人主页 & 修改个人信息
# ══════════════════════════════════════════════
def test_personal_homepage():
    sep("3. 个人主页 & 修改个人信息")
    uid = STATE["user_id_a"]

    # 3-1 查询个人主页
    r = req({"operation": "query_personal_homepage", "table_name": "user",
             "data": {"user_id": uid}})
    check("3-1 查询个人主页", r, expect_result=None,
          extra_checks={"user_id": uid})

    # 3-2 修改所有字段
    r = req({"operation": "recompose_personal_homepage", "table_name": "user",
             "data": {"user_id": uid, "name": "用户A改名", "status": "忙碌", "profile_picture_id": "2"}})
    check("3-2 修改全部字段", r)

    # 3-3 只修改 name，其余字段应保持不变
    r = req({"operation": "recompose_personal_homepage", "table_name": "user",
             "data": {"user_id": uid, "name": "用户A再改"}})
    check("3-3 只修改 name（其余保持不变）", r)

    # 3-4 不存在的 user_id（应失败）
    r = req({"operation": "recompose_personal_homepage", "table_name": "user",
             "data": {"user_id": "9999999", "name": "不存在"}})
    check("3-4 不存在user_id修改（应失败）", r, expect_result="fail")


# ══════════════════════════════════════════════
# 4. 通讯录 & 添加好友
# ══════════════════════════════════════════════
def test_contacts():
    sep("4. 通讯录 & 添加好友")
    uid_a = STATE["user_id_a"]
    uid_b = STATE["user_id_b"]

    # 4-1 A 添加 B 为好友（通过账号）
    r = req({"operation": "add_friend", "table_name": "contacts",
             "data": {"user_id": uid_a, "account": "test_user_b"}})
    check("4-1 A 添加 B 为好友", r)

    # 4-2 重复添加（应失败）
    r = req({"operation": "add_friend", "table_name": "contacts",
             "data": {"user_id": uid_a, "account": "test_user_b"}})
    check("4-2 重复添加好友（应失败）", r, expect_result="fail")

    # 4-3 添加不存在的账号（应失败）
    r = req({"operation": "add_friend", "table_name": "contacts",
             "data": {"user_id": uid_a, "account": "no_such_account_xyz"}})
    check("4-3 添加不存在账号（应失败）", r, expect_result="fail")

    # 4-4 B 也添加 A 为好友（双向）
    r = req({"operation": "add_friend", "table_name": "contacts",
             "data": {"user_id": uid_b, "account": "test_user_a"}})
    check("4-4 B 添加 A 为好友（双向）", r)

    # 4-5 查询通讯录
    r = req({"operation": "query_contacts", "table_name": "contacts",
             "data": {"user_id": uid_a}})
    check("4-5 查询通讯录", r, expect_result=None)

    # 4-6 通讯录搜索（有关键词）
    r = req({"operation": "query_contacts_", "table_name": "contacts",
             "data": {"user_id": uid_a, "friend_name": "用户B"}})
    check("4-6 通讯录搜索（有关键词）", r, expect_result=None)

    # 4-7 通讯录搜索（空关键词，返回全部）
    r = req({"operation": "query_contacts_", "table_name": "contacts",
             "data": {"user_id": uid_a, "friend_name": ""}})
    check("4-7 通讯录搜索（空关键词返回全部）", r, expect_result=None)

    # 4-8 通讯录搜索（不存在名称，返回空列表）
    r = req({"operation": "query_contacts_", "table_name": "contacts",
             "data": {"user_id": uid_a, "friend_name": "不存在的人"}})
    check("4-8 通讯录搜索（无结果）", r, expect_result=None)


# ══════════════════════════════════════════════
# 5. 朋友主页
# ══════════════════════════════════════════════
def test_friend_homepage():
    sep("5. 朋友主页")
    uid_a = STATE["user_id_a"]
    uid_b = STATE["user_id_b"]

    # 5-1 查看 B 的主页（传 B 的 user_id）
    r = req({"operation": "query_friend_homepage", "table_name": "user",
             "data": {"user_id": uid_b}})
    check("5-1 查看好友主页", r, expect_result=None,
          extra_checks={"friend_id": uid_b})

    # 5-2 查看不存在用户主页（返回空对象）
    r = req({"operation": "query_friend_homepage", "table_name": "user",
             "data": {"user_id": "9999999"}})
    check("5-2 查看不存在用户主页（返回空对象）", r, expect_result=None)


# ══════════════════════════════════════════════
# 6. 消息功能
# ══════════════════════════════════════════════
def test_messages():
    sep("6. 消息功能")
    uid_a = STATE["user_id_a"]
    uid_b = STATE["user_id_b"]

    # 6-1 A 发消息给 B
    r = req({"operation": "add_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b, "content": "你好，B！这是测试消息"}})
    check("6-1 A 发消息给 B", r)

    # 6-2 B 发消息给 A（反向）
    r = req({"operation": "add_message", "table_name": "message",
             "data": {"user_id": uid_b, "friend_id": uid_a, "content": "你好，A！我是B"}})
    check("6-2 B 发消息给 A（反向）", r)

    # 6-3 发送空内容（应失败）
    r = req({"operation": "add_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b, "content": ""}})
    check("6-3 发送空内容（应失败）", r, expect_result="fail")

    # 6-4 A 再发一条（用于后续搜索/收藏测试）
    r = req({"operation": "add_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b, "content": "搜索关键词Hello"}})
    check("6-4 A 发第二条消息", r)

    # 6-5 查询消息列表
    r = req({"operation": "query_message_list", "table_name": "message",
             "data": {"user_id": uid_a}})
    check("6-5 查询消息列表", r, expect_result=None)

    # 6-6 查询消息记录（双向）
    r = req({"operation": "query_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b}})
    check("6-6 查询消息记录（应含双向消息）", r, expect_result=None)
    msgs = r.get(uid_a, [])
    if msgs:
        STATE["message_id"] = msgs[0]["message_id"]
        print(f"  {INFO} 记录的 message_id = {STATE['message_id']}")

    # 6-7 查找消息（含 B 发给 A 的）
    r = req({"operation": "search_message", "table_name": "message",
             "data": {"user_id": uid_a, "content": "Hello"}})
    check("6-7 查找消息（模糊，含好友发给自己）", r, expect_result=None)

    # 6-8 查找消息（空关键词，所有可见消息）
    r = req({"operation": "search_message", "table_name": "message",
             "data": {"user_id": uid_a, "content": ""}})
    check("6-8 查找消息（空关键词）", r, expect_result=None)


# ══════════════════════════════════════════════
# 7. 删除消息（发送方 & 接收方独立删除）
# ══════════════════════════════════════════════
def test_delete_message():
    sep("7. 删除消息")
    uid_a = STATE["user_id_a"]
    uid_b = STATE["user_id_b"]

    # 先 A 再发一条，专门用于删除测试
    r = req({"operation": "add_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b, "content": "这条消息将被删除"}})
    check("7-0 发送待删除消息", r)

    # 查询记录，取最新一条 message_id
    r = req({"operation": "query_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b}})
    msgs = r.get(uid_a, [])
    del_msg_id = msgs[0]["message_id"] if msgs else None
    print(f"  {INFO} 待删除 message_id = {del_msg_id}")

    # 7-1 发送方（A）删除（只对 A 隐藏）
    if del_msg_id:
        r = req({"operation": "delete_message", "table_name": "message",
                 "data": {"user_id": uid_a, "message_id": del_msg_id}})
        check("7-1 发送方删除消息（只对 A 隐藏）", r)

    # 7-2 B 同样可以删除收到的消息（接收方删除）
    # 先查 B 视角的消息，找一条 A 发给 B 的
    r = req({"operation": "query_message", "table_name": "message",
             "data": {"user_id": uid_b, "friend_id": uid_a}})
    msgs_b = r.get(uid_b, [])
    recv_del_id = None
    for m in msgs_b:
        if m["message_user_id"] == uid_a:  # 找 A 发的那一条
            recv_del_id = m["message_id"]
            break
    print(f"  {INFO} B 视角待删除 message_id = {recv_del_id}")

    if recv_del_id:
        r = req({"operation": "delete_message", "table_name": "message",
                 "data": {"user_id": uid_b, "message_id": recv_del_id}})
        check("7-2 接收方（B）删除消息（只对 B 隐藏）", r)

    # 7-3 删除不存在的消息（应失败）
    r = req({"operation": "delete_message", "table_name": "message",
             "data": {"user_id": uid_a, "message_id": "9999999"}})
    check("7-3 删除不存在消息（应失败）", r, expect_result="fail")


# ══════════════════════════════════════════════
# 8. 朋友圈
# ══════════════════════════════════════════════
def test_moments():
    sep("8. 朋友圈")
    uid_a = STATE["user_id_a"]
    uid_b = STATE["user_id_b"]

    # 8-1 A 发朋友圈
    r = req({"operation": "add_moments", "table_name": "moments",
             "data": {"user_id": uid_a, "content": "A 的朋友圈动态"}})
    check("8-1 A 发朋友圈", r)

    # 8-2 B 发朋友圈
    r = req({"operation": "add_moments", "table_name": "moments",
             "data": {"user_id": uid_b, "content": "B 的朋友圈动态"}})
    check("8-2 B 发朋友圈", r)

    # 8-3 A 查看朋友圈（应含自己和 B 的动态）
    r = req({"operation": "query_moments", "table_name": "moments",
             "data": {"user_id": uid_a}})
    check("8-3 A 查看朋友圈（含自己+好友动态）", r, expect_result=None)
    mlist = r.get(uid_a, [])
    if mlist:
        STATE["moments_id"] = mlist[0]["moments_id"]
        print(f"  {INFO} 记录的 moments_id = {STATE['moments_id']}")

    # 8-4 删除朋友圈
    if STATE["moments_id"]:
        moments_owner = mlist[0]["moments_user_id"]
        r = req({"operation": "delete_moments", "table_name": "moments",
                 "data": {"user_id": moments_owner, "moments_id": STATE["moments_id"]}})
        check("8-4 删除朋友圈", r)

    # 8-5 删除不存在的朋友圈（应失败）
    r = req({"operation": "delete_moments", "table_name": "moments",
             "data": {"user_id": uid_a, "moments_id": "9999999"}})
    check("8-5 删除不存在朋友圈（应失败）", r, expect_result="fail")

    # 8-6 删除别人的朋友圈（应失败，user_id 不匹配）
    r = req({"operation": "add_moments", "table_name": "moments",
             "data": {"user_id": uid_b, "content": "B 的另一条动态"}})
    r2 = req({"operation": "query_moments", "table_name": "moments",
              "data": {"user_id": uid_b}})
    b_moments = r2.get(uid_b, [])
    b_mid = next((m["moments_id"] for m in b_moments if m["moments_user_id"] == uid_b), None)
    if b_mid:
        r3 = req({"operation": "delete_moments", "table_name": "moments",
                  "data": {"user_id": uid_a, "moments_id": b_mid}})
        check("8-6 删除别人的朋友圈（应失败）", r3, expect_result="fail")


# ══════════════════════════════════════════════
# 9. 收藏
# ══════════════════════════════════════════════
def test_favorites():
    sep("9. 收藏")
    uid_a = STATE["user_id_a"]
    uid_b = STATE["user_id_b"]

    # 取一条可收藏的消息 ID
    r = req({"operation": "query_message", "table_name": "message",
             "data": {"user_id": uid_a, "friend_id": uid_b}})
    msgs = r.get(uid_a, [])
    fav_msg_id = msgs[0]["message_id"] if msgs else STATE.get("message_id")
    print(f"  {INFO} 待收藏 message_id = {fav_msg_id}")

    # 9-1 A 收藏消息
    r = req({"operation": "add_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "message_id": fav_msg_id}})
    check("9-1 A 收藏消息", r)

    # 9-2 B 也收藏同一条消息（不同用户收藏同一条消息）
    r = req({"operation": "add_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_b, "message_id": fav_msg_id}})
    check("9-2 B 收藏同一条消息（跨用户）", r)

    # 9-3 A 重复收藏（应失败）
    r = req({"operation": "add_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "message_id": fav_msg_id}})
    check("9-3 A 重复收藏（应失败）", r, expect_result="fail")

    # 9-4 收藏不存在的消息（应失败）
    r = req({"operation": "add_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "message_id": "9999999"}})
    check("9-4 收藏不存在的消息（应失败）", r, expect_result="fail")

    # 9-5 查询收藏列表
    r = req({"operation": "query_favorites", "table_name": "favorites",
             "data": {"user_id": uid_a}})
    check("9-5 查询收藏列表", r, expect_result=None)
    flist = r.get(uid_a, [])
    if flist:
        STATE["favorites_id"] = flist[0]["favorites_id"]
        print(f"  {INFO} 记录的 favorites_id = {STATE['favorites_id']}")

    # 9-6 搜索收藏（有关键词）
    r = req({"operation": "query_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "content": "Hello"}})
    check("9-6 搜索收藏（有关键词）", r, expect_result=None)

    # 9-7 搜索收藏（空关键词，应返回空列表）
    r = req({"operation": "query_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "content": ""}})
    check("9-7 搜索收藏（空关键词返回空列表）", r, expect_result=None)
    assert r.get(uid_a) == [], f"空关键词应返回空列表，实际: {r.get(uid_a)}"

    # 9-8 删除收藏
    r = req({"operation": "delete_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "message_id": fav_msg_id}})
    check("9-8 删除收藏", r)

    # 9-9 删除不存在的收藏（应失败）
    r = req({"operation": "delete_favorites_message", "table_name": "favorites",
             "data": {"user_id": uid_a, "message_id": "9999999"}})
    check("9-9 删除不存在收藏（应失败）", r, expect_result="fail")


# ══════════════════════════════════════════════
# 10. 无效操作兜底
# ══════════════════════════════════════════════
def test_invalid():
    sep("10. 无效操作兜底")

    r = req({"operation": "unknown_op", "table_name": "user", "data": {}})
    check("10-1 未知 operation（应返回 fail）", r, expect_result="fail")

    r = req({"operation": "query_contacts", "table_name": "unknown_table", "data": {}})
    check("10-2 未知 table_name（应返回 fail）", r, expect_result="fail")


# ══════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════
if __name__ == "__main__":
    print("\n" + "█" * 55)
    print("  WeChat API 全功能测试")
    print("  服务地址：" + BASE_URL)
    print("█" * 55)

    try:
        test_register()
        test_login()
        test_personal_homepage()
        test_contacts()
        test_friend_homepage()
        test_messages()
        test_delete_message()
        test_moments()
        test_favorites()
        test_invalid()
    except requests.exceptions.ConnectionError:
        print(f"\n\033[91m[ERROR] 无法连接到服务器，请先启动服务：uvicorn app:app --reload\033[0m\n")
    except AssertionError as e:
        print(f"\n\033[91m[ASSERT ERROR] {e}\033[0m\n")

    print("\n" + "─" * 55)
    print("  测试完成")
    print("─" * 55 + "\n")
