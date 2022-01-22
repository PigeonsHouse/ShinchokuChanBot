from datetime import timedelta
from typing import List
import discord
from db.main import get_db
from db.schemas import Guild, Joining, Task, User

db = next(get_db())

async def check_new_guild(ctx: discord.ApplicationContext) -> None:
    guild = db.query(Guild).get(ctx.guild_id)
    if guild is None:
        new_guild = Guild(
            guild_id = ctx.guild_id,
            guild_name = ctx.guild.name,
            notify_channel_id = ctx.guild.text_channels[0].id
        )
        db.add(new_guild)
        db.commit()

async def check_new_user(ctx: discord.ApplicationContext) -> None:
    user_id = ctx.author.id
    guild_id = ctx.guild_id
    user = db.query(User).get(user_id)
    if user is None:
        new_user = User(
            user_id = user_id,
            user_name = ctx.author.name
        )
        db.add(new_user)
        db.commit()
    
    join_info = db.query(Joining).filter(Joining.user_id == user_id, Joining.guild_id == guild_id).first()
    if join_info is None:
        new_joining = Joining(
            user_id = user_id,
            guild_id = guild_id
        )
        db.add(new_joining)
        db.commit()

async def get_task_id(user_id:int, title: str) -> str:
    task = db.query(Task).filter(Task.user_id == user_id, Task.task_name == title).first()
    if task is None:
        new_task = Task(
            task_name = title,
            user_id = user_id
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        task = new_task
    return task.task_id

async def add_progress_time(task_id: int, duration: timedelta) -> bool:
    task = db.query(Task).get(task_id)
    if task is None:
        return False
    task.duration += duration
    db.commit()
    return True

async def set_notify_channel(guild_id: int, channel_id: int) -> bool:
    guild = db.query(Guild).filter(Guild.guild_id == guild_id).first()
    if guild is None:
        return False
    guild.notify_channel_id = channel_id
    db.commit()
    return True

async def get_guild_list() -> List[Guild]:
    return db.query(Guild).all()

async def get_joining_user(guild_id: int) -> List[Joining]:
    return db.query(Joining).filter(Joining.guild_id == guild_id).all()

async def get_task_list(user_id: int) -> List[Task]:
    return db.query(Task).filter(Task.user_id == user_id).all()

async def delete_user_and_task() -> None:
    db.query(User).delete()
    db.query(Task).delete()
    db.commit()

async def recreate_user(wd_list) -> None:
    for wd in wd_list:
        user = User(
            user_id = wd['user_id'],
            user_name = wd['name']
        )
        db.add(user)
    db.commit()    
