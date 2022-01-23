import os
import asyncio
from datetime import datetime, timedelta
import re
import discord
from dotenv import load_dotenv
from cruds import add_progress_time, check_new_guild, check_new_user, delete_user_and_task, get_guild_list, get_joining_user, get_task_id, get_task_list, recreate_user, set_notify_channel
from db.main import engine
from db.schemas import Base

load_dotenv()
TOKEN = os.environ.get('TOKEN')

client = discord.Bot()

Base.metadata.create_all(bind=engine)

watching_data_list = []

def view(duration):
    return_duration = str(duration)
    seconds = str(int(duration / timedelta(seconds=1)) % 60).zfill(2)
    minutes = str(int(duration / timedelta(minutes=1)) % 60).zfill(2)
    hours   = int(duration / timedelta(hours=1)) % 60
    return_duration = f"{hours}:{minutes}:{seconds}"
    return return_duration

async def report_progress():
    for watching_data in watching_data_list:
        duration = datetime.now() - datetime.fromisoformat(watching_data['start_at'])
        await add_progress_time(watching_data['task_id'], duration)
    guild_list = await get_guild_list()
    for guild in guild_list:
        notify_channel = client.get_channel(guild.notify_channel_id)
        await notify_channel.send('みんな今月もいっぱい頑張ったね！みんなの今月の進捗を報告するよ！')
        joining_user_id_list = await get_joining_user(guild.guild_id)
        for joining in joining_user_id_list:
            user_id = joining.user_id
            task_list = await get_task_list(user_id)
            if len(task_list):
                sendText = f'<@!{user_id}>さん'
                for task in task_list:
                    view_duration = view(task.duration)
                    sendText = f'{sendText}\n【{task.task_name}】{view_duration}'
                await notify_channel.send(sendText)
    await delete_user_and_task()
    await recreate_user(watching_data_list)
    for watching_data in watching_data_list:
        watching_data['start_at'] = datetime.now().isoformat()
        watching_data['task_id'] = await get_task_id(watching_data['user_id'], watching_data['task'])

@client.event
async def on_ready():
    print('sintyokuBot is running')
    while True:
        nowTime = datetime.now()
        if nowTime.strftime('%d-%H:%M') == '01-00:00':
            await report_progress()
        await asyncio.sleep(60)

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel == None:
        user_id = member.id
        for watching_data in watching_data_list:
            if watching_data['user_id'] == user_id:
                duration = datetime.now() - datetime.fromisoformat(watching_data['start_at'])
                task_name = watching_data['task']
                view_duration = view(duration)
                success = await add_progress_time(watching_data['task_id'], duration)
                if success is None:
                    await watching_data['channel'].send('タスク時間の計上に失敗したよ…ごめんね…')
                    return
                await watching_data['channel'].send(f'お疲れ様！頑張ったね！\n【{task_name}】{view_duration}')
                watching_data_list.remove(watching_data)
                return

# @client.event
# async def on_message(message):
#     content = message.content
#     if re.match(r'月が変わりました', content):
#         await report_progress()

@client.slash_command()
async def set_here(ctx: discord.ApplicationContext):
    await check_new_guild(ctx)
    guild_id = ctx.guild_id
    channel_id = ctx.channel_id

    success = await set_notify_channel(guild_id, channel_id)
    if not success:
        await ctx.respond('ごめん…設定に失敗したよ…')
        return
    await ctx.respond('月頭報告をこのチャンネルでするね！')

@client.slash_command()
async def start_task(ctx: discord.ApplicationContext, title: discord.Option(str, 'Input your task title') = 'test task'):
    user_vc = ctx.author.voice
    if user_vc is None:
        await ctx.respond('VCに入ってから作業を始めてね！')
        return
    if title is None:
        await ctx.respond('タスク名を入力してね！')
        return
    await check_new_guild(ctx)
    await check_new_user(ctx)
    user_id = ctx.author.id
    if len(title) > 125:
        await ctx.respond('タスク名が長すぎるよ！\n短くまとめて宣言し直してくれたら嬉しいなっ！')
        return
    for watching_data in watching_data_list:
        if watching_data['user_id'] == user_id:
            if watching_data['task'] == title:
                await ctx.respond(f'`{title}`をしてるのはちゃんと見てるよ？\n応援してるよ！頑張ってね！')
                return
            else:
                await ctx.respond('作業を変更するときは一度終了してからもう一度宣言してね！')
                return
    task_id = await get_task_id(ctx.author.id, title)
    await ctx.respond(f'{title}をやるんだね！\n今日も頑張ろう！')
    watching_data_list.append({
        'user_id': user_id,
        'name': ctx.author.name,
        'start_at': datetime.now().isoformat(),
        'task': title,
        'task_id': task_id,
        'channel': ctx.channel
    })
    
@client.slash_command()
async def end_task(ctx: discord.ApplicationContext):
    user_vc = ctx.author.voice
    if user_vc is None:
        await ctx.respond('VCに入って終了宣言をしてね')
        return
    await check_new_guild(ctx)
    await check_new_user(ctx)
    user_id = ctx.author.id
    for watching_data in watching_data_list:
        if watching_data['user_id'] == user_id:
            duration = datetime.now() - datetime.fromisoformat(watching_data['start_at'])
            task_name = watching_data['task']
            view_duration = view(duration)
            success = await add_progress_time(watching_data['task_id'], duration)
            if success is None:
                await ctx.respond('タスク時間の計上に失敗したよ…ごめんね…')
                return
            await ctx.respond(f'お疲れ様！頑張ったね！\n【{task_name}】{view_duration}')
            watching_data_list.remove(watching_data)
            return
    await ctx.respond('まだ作業開始の宣言をしてないよ？\n何の作業をしてるか教えてね！')

def run_bot(token: str):
    try:
        client.run(token)
    except Exception as e:
        print(e)

run_bot(TOKEN)
