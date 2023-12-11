
import os
import telebot
from telebot import types

bot = telebot.TeleBot("6734872715:AAH51orbUim5luLE1cJ2x7xszSOz0nyzF9A")

# Add a dictionary to store thumbnail information
user_thumbnails = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"""<b>Welcome to the file renamer bot!</b>

Available commands:
/start - Show this message
/rename - Rename a file
/thumbnail - Set thumbnail for file renaming

Send me a document to rename it.""", parse_mode="HTML")

@bot.message_handler(commands=['rename'])
def start_rename(message):
    bot.reply_to(message, "Send me the files you want to rename (one at a time).")
    bot.register_next_step_handler(message, handle_rename_files)

@bot.message_handler(commands=['thumbnail'])
def set_thumbnail(message):
    bot.reply_to(message, "Send me the image you want to use as the thumbnail.")
    bot.register_next_step_handler(message, store_thumbnail)

@bot.message_handler(content_types=['document'])
def handle_rename_files(message):
    # Get user chat ID
    user_chat_id = message.chat.id

    # Check if user already has files to rename
    if user_chat_id in user_new_names and user_new_names[user_chat_id] is not None:
        existing_files = user_new_names[user_chat_id]
        existing_files.append((message.document.file_name, message.document.file_id))
        user_new_names[user_chat_id] = existing_files
    else:
        user_new_names[user_chat_id] = [(message.document.file_name, message.document.file_id)]

    # Check if user has set a thumbnail
    if user_chat_id in user_thumbnails:
        thumbnail = user_thumbnails[user_chat_id]
    else:
        thumbnail = None

    # Prompt user for confirmation
    bot.reply_to(message, f"""<b>Files to rename:</b>
{', '.join([filename for filename, _ in user_new_names[user_chat_id]])}

<b>Thumbnail:</b> {thumbnail if thumbnail else 'None'}

<b>Are you sure you want to rename these files?</b> (Yes/No)""", parse_mode="HTML")
    bot.register_next_step_handler(message, confirm_rename_files)

def handle_new_name(message):
    # Get user chat ID and rename information
    user_chat_id = message.chat.id
    original_files, downloaded_files = user_new_names[user_chat_id], dict()
    thumbnail = user_thumbnails[user_chat_id] if user_chat_id in user_thumbnails else None

    # Validate and process user input
    new_filenames = message.text.strip().split('\n')
    if len(new_filenames) != len(original_files):
        bot.reply_to(message, "Error: The number of new filenames doesn't match the number of files.")
        return

    # Rename files and send them back to the user
    for original_filename, downloaded_file, new_filename in zip(original_files, downloaded_files, new_filenames):
        renamed_file_name = os.path.join(os.getcwd(), new_filename)
        with open(renamed_file_name, 'wb') as renamed_file:
            renamed_file.write(downloaded_file)
        with open(renamed_file_name, 'rb') as renamed_file:
            bot.send_document(message.chat.id, renamed_file, thumb=thumbnail)
        os.remove(renamed_file_name)

    # Cleanup user information
    del user_new_names[user_chat_id]
    if user_chat_id in user_thumbnails:
        del user_thumbnails[user_chat_id]

    bot.reply_to(message, "Files renamed successfully!")

def store_thumbnail(message):
    # Get user chat ID and download thumbnail
    user_chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    

    
