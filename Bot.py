import telebot
import os
import ffmpeg
import re

# Create a Telegram bot object
bot = telebot.TeleBot('6337637965:AAFVJc09tFgqgeAszChm_XdjTYaQA24HFRw')

# Define a function to rename a file
def rename_file(file_path, episode_number, format):
    """Renames a file to the specified episode number.

    Args:
        file_path: The path to the file to rename.
        episode_number: The episode number to rename the file to.
        format: The format of the new file name.

    Returns:
        The new file path.
    """

    # Get the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Create a new file path with the episode number
    new_file_path = os.path.join(os.path.dirname(file_path), format.format(episode_number, file_extension))

    # Rename the file
    os.rename(file_path, new_file_path)

    return new_file_path

# Define a function to set the thumbnail of a file
def set_thumbnail(file_path, thumbnail_path):
    """Sets the thumbnail of a file.

    Args:
        file_path: The path to the file to set the thumbnail for.
        thumbnail_path: The path to the thumbnail image.
    """

    # Create an FFmpeg object
    ffmpeg_command = ffmpeg.input(file_path).output(file_path, tn=thumbnail_path).overwrite_output().run_pipe()

# Define a function to handle forwarded messages
@bot.message_handler(func=lambda message: message.content_type == 'message_document')
def handle_forwarded_messages(message):
    """Handles forwarded messages.

    Args:
        message: The Telegram message object.
    """

    # Get the file path of the forwarded file
    file_path = bot.get_file_path(message.document.file_id)

    # Get the episode number from the file name
    episode_number_regex = re.compile(r'EP-(\d+)')
    episode_number = int(episode_number_regex.search(message.document.file_name).group(1))

    # Get the format of the new file name
    format = '[SAW] EP- {0:02d} {1}'

    # Rename the file
    new_file_path = rename_file(file_path, episode_number, format)

    # Set the thumbnail of the file
    thumbnail_path = os.path.join(os.path.dirname(file_path), 'thumbnail.jpg')
    set_thumbnail(new_file_path, thumbnail_path)

    # Send the renamed file to the user
    bot.send_document(message.chat.id, new_file_path)

# Start the Telegram bot
bot.polling()
