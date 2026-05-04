import discord
from discord import app_commands
from discord.ext import commands

class ServerSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_server", description="Automatically Make Server (Categories & Channels & Roles)")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_server(self, interaction: discord.Interaction):
        # Notify the user that the process has started
        await interaction.response.send_message("🏗️ Starting server structure setup... This may take a moment.", ephemeral=True)
        guild = interaction.guild
        everyone = guild.default_role

        # ==============================================
        # 🆕 ส่วนเพิ่มเติม: สร้างยศและเรียงลำดับตามรูป
        # ==============================================
        role_names = [
            "Owner", "Manager", "-", "Assistant Manager",
            "========== BOT ==========",
            "Administrator",
            "========== STAFF ==========",
            "HEAD OF STAFF", "Senior Moderator", "Moderator", "Junior Moderator",
            "========== OTHER ==========",
            "CC Manager", "Content Creator", "TESTER", "Server Booster",
            "========== Helpers ==========",
            "Trello Manager", "Helper Lead", "Trello Team", "Giveaway Host",
            "========== LEVELS ==========",
            "Radiant", "Immortal", "Radiant", "Diamond", "Platinum", "Gold", "Silver", "Bronze",
            "========== STATUS ==========",
            "Verified", "Unverified",
            "========== INTERNATIONAL ==========",
            "Thai Access", "Brazil Access", "Spain Access", "Vietnam Access",
            "========== PINGS ==========",
            "Announcement Ping", "SneakPeak Ping", "Update Ping", "Giveaway ping", "Community Ping",
       ]
        created_roles = {}
        for name in role_names:
            role = discord.utils.get(guild.roles, name=name)
            if not role:
                role = await guild.create_role(name=name)
            created_roles[name] = role
            # ขยับยศขึ้นเรื่อยๆ เพื่อให้เรียงลำดับถูกต้อง
            # ขยับยศโดยเช็คไม่ให้ต่ำกว่าตำแหน่งที่ 1
            new_pos = max(1, guild.me.top_role.position - 1)
            try:
                await role.edit(position=new_pos)
            except discord.Forbidden:
                print(f"❌ ไม่สามารถขยับยศ {name} ได้ (สิทธิ์ไม่พอ)")
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาดกับยศ {name}: {e}")


        # ดึงยศสำคัญๆ มาใช้งาน
        r_unverified = created_roles["Unverified"]
        r_verified = created_roles["Verified"]
        r_staff = created_roles["========== STAFF =========="]
        r_cc = created_roles["========== OTHER =========="] # ใช้ OTHER เป็นฐานของ CC
        r_tester = created_roles["TESTER"]

        # ==============================================
        # 🆕 ส่วนเพิ่มเติม: ตั้งค่าสิทธิ์ (Permissions)
        # ==============================================
        # Unverified: เห็นแค่ห้อง verify
        ov_unverified = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            r_unverified: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # Verified: อ่านได้ พิมพ์ได้ แต่สร้าง thread ไม่ได้
        ov_standard = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            r_verified: discord.PermissionOverwrite(view_channel=True, send_messages=True, create_public_threads=False),
            r_staff: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # Read Only: อ่านอย่างเดียว
        ov_readonly = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            r_verified: discord.PermissionOverwrite(view_channel=True, send_messages=False, create_public_threads=False),
            r_staff: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # Staff Only
        ov_staff = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            r_staff: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # CC Only
        ov_cc = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            created_roles["CC Manager"]: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            created_roles["Content Creator"]: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            r_staff: discord.PermissionOverwrite(view_channel=True)
        }

        # Tester Only
        ov_tester = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            r_tester: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            r_staff: discord.PermissionOverwrite(view_channel=True)
        }

        # Logs: อ่านอย่างเดียว
        ov_logs = {
            everyone: discord.PermissionOverwrite(view_channel=False),
            r_staff: discord.PermissionOverwrite(view_channel=True, send_messages=False)
        }

        # ==============================================
        # โค้ดเดิม: สร้างช่องพร้อมใส่ Permissions
        # ==============================================
        structure = {
            "✅ | Verification": {"perms": ov_unverified, "channels": [("【🔒】verification", "text"), ("【❓】how-to-verify", "text")]},
            "TOP": {"perms": None, "channels": [("【🏃】welcome", "text"), ("【🌸】boosts", "text")]},
            "🔔 | Important": {"perms": ov_readonly, "channels": [("【📢】announcements", "news"), ("【📢】sub-announcements", "text"), ("【📖】rules", "text"), ("【📃】information", "text"), ("【🔗】links", "text")]},
            "🏰 | N/A": {"perms": ov_standard, "channels": [("【📢】updates-log", "news"), ("【👀】sneaks", "text"), ("【📊】polls", "text"), ("【💎】codes", "text")]},
            "📄 | Information": {"perms": ov_readonly, "channels": [("【🧩】trello-posts", "text"), ("【❓】faq", "text"), ("【📊】level", "text")]},
            "🎩 | Engagement": {"perms": ov_readonly, "channels": [("【🎁】giveaway", "text"), ("【🎁】staff-giveaway", "text"), ("【🎪】event", "text"), ("【🎥】content", "text"), ("【🌟】staff-post", "text"), ("【🎤】Stage", "stage")]},
            "🔴 | CC": {"perms": ov_cc, "channels": [("【💬】verified-cc-chat", "text"), ("【💬】cc-chat", "text"), ("【🎙️】Content Creator VC", "voice"), ("【🎙️】Verified Creator VC", "voice")]},
            "🎨 | Artist": {"perms": ov_standard, "channels": [("【📢】artist-announcements", "text"), ("【💬】artist-chat", "text"), ("【💡】artist-suggestions", "forum")]},
            "📍 | Community": {"perms": ov_standard, "channels": [("【🎨】artwork", "text"), ("【🌸】booster-chat", "text"), ("【💬】general", "text"), ("【❓】questions", "text"), ("【🤖】bot-commands", "text")]},
            "🌎 | International chats": {"perms": ov_standard, "channels": [("【】general", "text"), ("【】geral", "text"), ("【】general", "text"), ("【】gerneral", "text"), ("【】general", "text")]},
            "🎤 | Voice Channels": {"perms": ov_standard, "channels": [("【🎙️】VC", "voice"), ("【🎙️】VC", "voice"), ("【🎙️】VC", "voice"), ("【🎙️】VC", "voice")]},
            "🧪 | Tester": {"perms": ov_tester, "channels": [("【📢】tester-announcements", "text"), ("【📚】tester-guidelines", "text"), ("【📊】tester-polls", "text"), ("【💬】tester-chat", "text"), ("【🎮】tester-usernames", "text"), ("【‼️】tester-loa", "text"), ("【🐛】tester-bug-report", "forum"), ("【💡】tester-suggestions", "forum"), ("【🎙️】Tester VC", "voice")]},
            "📋 | Staff Rubric": {"perms": ov_staff, "channels": [("【📰】staff-announcements", "text"), ("【📚】staff-guidelines", "text"), ("【📔】staff-roster", "text"), ("【❓】staff-faq", "text")]},
            "🔨 | Staff": {"perms": ov_staff, "channels": [("【💬】staff-chat", "text"), ("【🤖】staff-cmds", "text"), ("【📑】proof", "text"), ("【🔨】ban-proof", "text"), ("【⚖️】discord-ban-appeals", "text"), ("【‼️】staff-loa", "text"), ("【💡】staff-suggestions", "forum"), ("【🎙️】Staff VC", "voice")]},
            "📁 | Logs": {"perms": ov_logs, "channels": [("【📑】mod-logs", "text"), ("【📑】message-logs", "text"), ("【📑】automod-logs", "text"), ("【📑】nickname-logs", "text"), ("【📑】noping-logs", "text"), ("【📑】role-logs", "text"), ("【📑】join-leave-logs", "text"), ("【📑】vc-logs", "text"), ("【📑】command-logs", "text")]}
        }

        try:
            for category_name, data in structure.items():
                if category_name == "TOP":
                    for name, c_type in data["channels"]:
                        await self.create_ch(guild, name, c_type)
                else:
                    # สร้าง Category พร้อมกับตั้งค่า Permissions เลย
                    category = await guild.create_category(category_name, overwrites=data["perms"])
                    for name, c_type in data["channels"]:
                        await self.create_ch(guild, name, c_type, category)

            await interaction.followup.send("✅ Server setup complete! All categories, channels, roles and permissions have been created.")
        except Exception as e:
            print(f"Setup Error: {e}")
            await interaction.followup.send(f"❌ An error occurred: {e}")

    async def create_ch(self, guild, name, c_type, category=None):
        try:
            if c_type == "text":
                await guild.create_text_channel(name, category=category)
            elif c_type == "voice":
                await guild.create_voice_channel(name, category=category)
            elif c_type == "news":
                await guild.create_text_channel(name, category=category, news=True)
            elif c_type == "stage":
                await guild.create_stage_channel(name, category=category)
            elif c_type == "forum":
                # Forum channels require Community to be enabled
                try:
                    await guild.create_forum_channel(name, category=category)
                except:
                    # Fallback to text channel if forum fails
                    await guild.create_text_channel(name, category=category)
        except Exception as e:
            print(f"Could not create channel {name}: {e}")

async def setup(bot):
    await bot.add_cog(ServerSetup(bot))
    