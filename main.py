
from telegram import *
from telegram.ext import *
from telegram.utils.request import Request

from configure import config
import os

token = config['token']
url = config['url']



def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.full_name
    chat_id = update.effective_user.id
    
    button1 = KeyboardButton('Button1')
    button2 = KeyboardButton('Button2')
    
    keyboard = [
        [button1, button2],
        [button1, button2, button1],
        [button1, button2]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        text=f"Hello {user_name}, \nWelcome to the New BOT",
        reply_markup=reply_markup
    )

def custom(update: Update, context: CallbackContext):
    user_name = update.effective_user.full_name
    chat_id = update.effective_user.id
    
    update.message.reply_text(
        text=f"Custom command called!"
    )
    
def msg_handler(update: Update, context: CallbackContext):
    user_name = update.effective_user.full_name
    chat_id = update.effective_user.id
    
    text = update.message.text
    
    inline_btn1 = InlineKeyboardButton("Test", callback_data="test")
    btn1_keyboard = [[inline_btn1]]
    reply_markup = InlineKeyboardMarkup(btn1_keyboard)
    
    if text == 'Button1':
        update.message.reply_text(
            text=f"Sizin textiniz: {text}",
            reply_markup=reply_markup
        )

    # Delete the message
    delete = InlineKeyboardButton("Delete me", callback_data="delete_message")
    delete_keyboard = [[delete]]
    reply_markup1 = InlineKeyboardMarkup(delete_keyboard)
    
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup1
    )
    
    # Update the message button
    update_btn = InlineKeyboardButton("Update inline btn", callback_data="update_button")
    update_keyboard = [[update_btn]]
    reply_markup2 = InlineKeyboardMarkup(update_keyboard)
    
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup2
    )
    
    # Update the message
    update_msg = InlineKeyboardButton("Update message text", callback_data="update_message")
    update_msg_keyboard = [[update_msg, delete]]
    reply_markup3 = InlineKeyboardMarkup(update_msg_keyboard)
    
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup3
    )

def query_handler(update: Update, context: CallbackContext, **kwargs):
    query = update.callback_query
    data = query.data
    
    query_id = query.id
    
    user_name = update.effective_user.full_name
    chat_id = update.effective_user.id
    message_id = update.effective_message.message_id
    
    text = update.effective_message.text
    
    
    if data == "test":
        query.answer(text="Test clicked!", show_alert=True)
    elif data == "delete_message":
        query.answer()
        context.bot.delete_message(chat_id, message_id)
        context.bot.send_message(chat_id, "Message deleted!")
    elif data == "update_button":
        new_button = InlineKeyboardButton("New Button!", callback_data="new_button_clicked")
        new_keyboard = [[new_button]]
        new_reply_markup = InlineKeyboardMarkup(new_keyboard)
        
        query.edit_message_reply_markup(reply_markup=new_reply_markup)
    
    elif data == "new_button_clicked":
        query.edit_message_reply_markup(reply_markup=None)
    
    elif data == "update_message":
        query.edit_message_text("Message text updated!")

def set_note(update: Update, context: CallbackContext):
    note = ' '.join(context.args)
    
    if 'notes' not in context.user_data:
        context.user_data['notes'] = []
    
    context.user_data['notes'].append(note)
    update.message.reply_text(f"Note saved: {note}")

def get_note(update: Update, context: CallbackContext):
    
    notes = context.user_data.get('notes', [])
    if not notes:
        update.message.reply_text(f"You have no notes!")
        return
    
    notes_text = '\n'.join(notes)
    update.message.reply_text(notes_text)

def clear_notes(update: Update, context: CallbackContext):
    context.user_data['notes'] = []
    update.message.reply_text('All notes cleared!')

def send_notes_doc(update: Update, context: CallbackContext):
    notes = context.user_data.get('notes', [])
    if not notes:
        update.message.reply_text(f"You have no notes!")
        return
    
    notes_text = '\n'.join(notes)
    with open('notes.txt', 'w') as f:
        f.write(notes_text)
    
    with open('notes.txt', 'rb') as f:
        update.message.reply_document(document=f)
    
    os.remove('notes.txt')

def main():
    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0
    )
    
    bot = Bot(
        token=token,
        request=req,
        base_url=url
    )
    
    updater = Updater(
        bot=bot,
        use_context=True
    )
    
    
    start_handler = CommandHandler("start", start)
    custom_handler = CommandHandler("custom", custom)
    setnote_handler = CommandHandler("setnote", set_note, pass_args=True)
    getnote_handler = CommandHandler("getnote", get_note)
    clearnote_handler = CommandHandler("clearnotes", clear_notes)
    senddoc_handler = CommandHandler("senddoc", send_notes_doc)
    
    message_handler = MessageHandler(Filters.text, msg_handler)
    
    callback_handler = CallbackQueryHandler(callback=query_handler, pass_chat_data=True)
    
    dp = updater.dispatcher
    
    dp.add_handler(start_handler)
    dp.add_handler(custom_handler)
    dp.add_handler(setnote_handler)
    dp.add_handler(getnote_handler)
    dp.add_handler(clearnote_handler)
    dp.add_handler(senddoc_handler)
    
    dp.add_handler(message_handler)
    dp.add_handler(callback_handler)
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()