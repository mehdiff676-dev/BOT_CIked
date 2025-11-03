import telebot
import threading
import time
import concurrent.futures

TOKEN = "8367901434:AAGV8OXzNRYoIu8F8mWgFiae9zbluFFY9NA"
DEVELOPER_ID = 6859427488  # ضع هنا الأيدي الخاص بك

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['massban'])
def mass_ban(message):
    # التحقق من أن المستخدم هو المطور فقط
    if message.from_user.id != DEVELOPER_ID:
        bot.reply_to(message, "❌ هذا الأمر متاح للمطور فقط.")
        return

    chat_id = message.chat.id
    
    # التحقق من أن البوت مشرف في المجموعة/القناة
    try:
        bot_member = bot.get_chat_member(chat_id, bot.get_me().id)
        if bot_member.status not in ['administrator', 'creator']:
            bot.reply_to(message, "❌ البوت ليس مشرفاً في هذه المجموعة/القناة.")
            return
    except:
        bot.reply_to(message, "❌ لا يمكن الوصول إلى هذه المجموعة/القناة.")
        return

    members_count = bot.get_chat_members_count(chat_id)
    bot.reply_to(message, f"🚀 بدأ عملية حظر {members_count} عضو... (الوضع السريع)")

    def ban_members():
        banned_count = 0
        failed_count = 0
        members_list = []

        try:
            # جمع جميع الأعضاء أولاً
            offset = 0
            limit = 200  # زيادة الحد
            
            while True:
                members = bot.get_chat_members(chat_id, offset, limit)
                if not members:
                    break
                
                members_list.extend(members)
                offset += limit
                time.sleep(0.05)  # تقليل وقت الانتظار

        except Exception as e:
            bot.send_message(chat_id, f"❌ خطأ في جمع الأعضاء: {e}")
            return

        # وظيفة للحظر السريع
        def ban_single_member(member):
            try:
                if (member.user.id != DEVELOPER_ID and 
                    not member.user.is_bot and 
                    member.status != 'creator'):
                    
                    bot.ban_chat_member(chat_id, member.user.id)
                    return "success"
                else:
                    return "skipped"
            except Exception as e:
                return "failed"

        # استخدام ThreadPoolExecutor للحظر المتوازي
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(ban_single_member, members_list))
        
        banned_count = results.count("success")
        failed_count = results.count("failed")
        skipped_count = results.count("skipped")

        bot.send_message(chat_id, f"✅ تم الانتهاء بسرعة!\nتم حظر: {banned_count} عضو\nفشل في حظر: {failed_count} عضو\nتم تخطي: {skipped_count} عضو")

    # تشغيل العملية في خيط منفصل
    thread = threading.Thread(target=ban_members)
    thread.start()

@bot.message_handler(commands=['xza'])
def fast_mass_ban(message):
    if message.from_user.id != DEVELOPER_ID:
        bot.reply_to(message, "❌ هذا الأمر متاح للمطور فقط.")
        return

    chat_id = message.chat.id
    
    try:
        bot_member = bot.get_chat_member(chat_id, bot.get_me().id)
        if bot_member.status not in ['administrator', 'creator']:
            bot.reply_to(message, "❌ البوت ليس مشرفاً في هذه المجموعة/القناة.")
            return
    except:
        bot.reply_to(message, "❌ لا يمكن الوصول إلى هذه المجموعة/القناة.")
        return

    bot.reply_to(message, "⚡ بدأ الحظر السريع الفائق...")

    def super_fast_ban():
        banned_count = 0
        failed_count = 0

        try:
            offset = 0
            limit = 300
            
            while True:
                members = bot.get_chat_members(chat_id, offset, limit)
                if not members:
                    break

                # حظر مجموعة من الأعضاء دفعة واحدة
                for member in members:
                    try:
                        if (member.user.id != DEVELOPER_ID and 
                            not member.user.is_bot and 
                            member.status != 'creator'):
                            
                            # حظر بدون انتظار
                            bot.ban_chat_member(chat_id, member.user.id)
                            banned_count += 1
                            # إزالة وقت الانتظار للسرعة القصوى
                            
                    except Exception as e:
                        failed_count += 1
                        continue

                offset += limit
                # وقت انتظار أقل بين المجموعات
                time.sleep(0.02)

        except Exception as e:
            pass

        bot.send_message(chat_id, f"⚡ تم الانتهاء بسرعة فائقة!\nتم حظر: {banned_count} عضو\nفشل في حظر: {failed_count} عضو")

    thread = threading.Thread(target=super_fast_ban)
    thread.start()

# عند إضافة البوت إلى مجموعة أو قناة
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    bot_id = bot.get_me().id
    for new_member in message.new_chat_members:
        if new_member.id == bot_id:
            chat_id = message.chat.id
            bot.send_message(chat_id, "🤖 البوت السريع جاهز للعمل!\n/massban - حظر سريع\n/fastban - حظر فائق السرعة\n(المطور فقط)")
            break

# تشغيل البوت
print("البوت السريع يعمل...")
bot.polling(none_stop=True)