import asyncio
from tortoise import Tortoise
from database.mysql import DB_ORM_CONFIG
from models.base import User, Contacts, Message, Favorites, Moments
from database.contacts import add_contact, get_contacts, remove_contact
from database.messages import send_message, get_messages
from database.user import create_user, get_user_by_account, delete_user

async def run_tests():
    print("Connecting to database...")
    # 初始化数据库连接
    await Tortoise.init(config=DB_ORM_CONFIG)
    
    print("Database connected. Starting integration test...")

    try:
        # 1. 环境预清理 (防止上次运行失败遗留数据导致 Duplicate entry 报错)
        u1 = await get_user_by_account("test_u1")
        if u1: await delete_user(u1.id)
        u2 = await get_user_by_account("test_u2")
        if u2: await delete_user(u2.id)

        # 2. 测试 User CRUD
        user1 = await create_user(account="test_u1", password="123", name="Test User 1")
        user2 = await create_user(account="test_u2", password="123", name="Test User 2")
        print(f"[OK] User CRUD - User1 ID: {user1.id}, User2 ID: {user2.id}")
        
        # 3. 测试 Contacts CRUD
        contact = await add_contact(user1.id, user2.id)
        contacts = await get_contacts(user1.id)
        print(f"[OK] Contacts CRUD - Friends of U1: {[c.friend_id for c in contacts]}")
        
        # 4. 测试 Messages CRUD
        msg = await send_message(user1.id, user2.id, "Hello from automated test!")
        messages = await get_messages(user1.id, user2.id)
        print(f"[OK] Messages CRUD - U1 -> U2 messages: {[m.content for m in messages]}")
        
        # 清理测试数据
        print("Cleaning up test data...")
        await remove_contact(user1.id, user2.id)
        await msg.delete()
        await delete_user(user1.id)
        await delete_user(user2.id)
        print("[OK] Test data cleaned.")

        print("All database CRUD integration tests passed successfully!")
    
    except Exception as e:
        print(f"Error occurred during testing: {e}")
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()
        print("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(run_tests())
