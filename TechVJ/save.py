import os
import asyncio
from pyrogram import Client, types

async def process_message(client: Client, message: types.Message):
    msg = message.reply_to_message
    msg_type = get_message_type(msg)

    if msg_type == "Text":
        try:
            await client.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {str(e)}", reply_to_message_id=message.id)
            return

    smsg = await client.send_message(message.chat.id, 'Downloading...', reply_to_message_id=message.id)
    dosta = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg))
    
    try:
        file = await client.download_media(msg, progress=progress, progress_args=[message, "down"])
        os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        await client.send_message(message.chat.id, f"Error: {str(e)}", reply_to_message_id=message.id)
        return
    
    upsta = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg))
    caption = msg.caption if msg.caption else None

    try:
        if msg_type == "Document":
            ph_path = await try_download_thumb(acc, msg.document.thumbs)

            await client.send_document(message.chat.id, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
            if ph_path: os.remove(ph_path)

        elif msg_type == "Video":
            ph_path = await try_download_thumb(acc, msg.video.thumbs)

            await client.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
            if ph_path: os.remove(ph_path)

        elif msg_type == "Animation":
            await client.send_animation(message.chat.id, file, reply_to_message_id=message.id)

        elif msg_type == "Sticker":
            await client.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

        elif msg_type == "Voice":
            await client.send_voice(message.chat.id, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

        elif msg_type == "Audio":
            ph_path = await try_download_thumb(acc, msg.audio.thumbs)

            await client.send_audio(message.chat.id, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
            if ph_path: os.remove(ph_path)

        elif msg_type == "Photo":
            await client.send_photo(message.chat.id, file, caption=caption, reply_to_message_id=message.id)

    except Exception as e:
        await client.send_message(message.chat.id, f"Error: {str(e)}", reply_to_message_id=message.id)

    finally:
        if os.path.exists(f'{message.id}upstatus.txt'):
            os.remove(f'{message.id}upstatus.txt')
        if os.path.exists(file):
            os.remove(file)
        await client.delete_messages(message.chat.id, [smsg.id])

# Helper function to download thumbnails
async def try_download_thumb(acc, thumbs):
    try:
        return await acc.download_media(thumbs[0].file_id)
    except:
        return None

def get_message_type(msg: types.Message):
    if msg.document:
        return "Document"
    if msg.video:
        return "Video"
    if msg.animation:
        return "Animation"
    if msg.sticker:
        return "Sticker"
    if msg.voice:
        return "Voice"
    if msg.audio:
        return "Audio"
    if msg.photo:
        return "Photo"
    if msg.text:
        return "Text"
    return "Unknown"
