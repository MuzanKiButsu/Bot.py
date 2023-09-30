import sqlite3

conn = sqlite3.connect("file_storage.db")
cursor = conn.cursor()

# Create a table to store file information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_id TEXT,
        file_name TEXT
    )
""")
conn.commit()

def start(update, context):
    update.message.reply_text("Welcome! Send a file to store it.")

def help(update, context):
    update.message.reply_text("Send a file to store it with /storefile command.")

def store_file(update, context):
    user_id = update.message.from_user.id
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name

    # Store file information in the database
    cursor.execute("INSERT INTO files (user_id, file_id, file_name) VALUES (?, ?, ?)",
                   (user_id, file_id, file_name))
    conn.commit()

    update.message.reply_text(f"File '{file_name}' stored successfully.")

# Set up command handlers
updater = Updater(token="YOUR_API_TOKEN", use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(MessageHandler(Filters.document.mime("application/*"), store_file))
updater.start_polling()
updater.idle()
