from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import *
from discord.utils import get
import discord,asyncio,datetime,json,config,random,smtplib,time

with open("setting.json") as file:
    load_bot = json.load(file)
    토큰 = load_bot["token"]
    접두사 = load_bot["prefix"]
    admins_id = load_bot["owner"]



intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


smtp_config1 = {
                    "smtp_server": config.smtp_google,  
                    "smtp_user_id": config.smtp_email,
                    "smtp_user_pw": config.smtp_pw,
                    "smtp_port": config.smtp_port 
}


y = datetime.datetime.now().year
m = datetime.datetime.now().month
d = datetime.datetime.now().day
h = datetime.datetime.now().hour
mn = datetime.datetime.now().minute
se = datetime.datetime.now().second 

now_time = "{0}-{1}-{2} {3}:{4}:{5}".format(y, m, d, h, mn, se)


@client.event
async def on_connect():
   print(f'[!] 봇이름 : {client.user.name}\n[!] 봇아이디 : {client.user.id}\n[!] 로그인시간 : {now_time}\n[!] 초대링크 : https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot\n[!] 개발자 : 화이트홀\n_________________________________________________')
   await client.change_presence(activity=discord.Streaming(name= "인증봇", url="https://www.twitch.tv/whitehole"))



@client.event
async def on_message(message):


    
        

    if message.content.startswith(접두사+"인증"):
        def msg_channel_check1(msg1):
                return (isinstance(msg1.channel, discord.channel.DMChannel) and (message.author.id == msg1.author.id))
        try:
                await message.author.send("> ✅ 코드를 받으실 이메일을 적어주세요. ✅")
        except:
                await message.channel.send(":x:개인정보 보호 설정에서 디엠을 켜주세요!:x:")
                return
        await message.channel.send(f"> <@{message.author.id}>님 디엠을 확인해주세요!\n> 제한시간 60초")
        try:
                get_email = await client.wait_for("message", timeout=60, check=msg_channel_check1)
                get_email_content = get_email.content
                random_code =random.randint(111111,999999)
                verify_code = []
                verify_code.append(random_code)
                mail_msg = MIMEMultipart()
                con_tent = str(random_code) + f" \n{message.author.name}님 인증코드 입니다.\n보낸사람 : 화이트홀미만잡#6229\n받는사람 : {message.author.name}"
                mail_msg['Subject'] = f'WhiteHole Asked Terror Tool Verify Code : ' + str(verify_code) # 메일 제목
                mail_msg['From'] = 'whitehole'   
                mail_msg['To'] = get_email_content
                mail_msg.attach(MIMEText(con_tent, 'plain'))
                smtp_send = smtplib.SMTP(smtp_config1['smtp_server'], smtp_config1['smtp_port'])
                smtp_send.ehlo
                smtp_send.starttls()
                smtp_send.login(config.smtp_email , config.smtp_pw)   
                smtp_send.sendmail(mail_msg['From'], mail_msg['To'], mail_msg.as_string())
                smtp_send.quit()
                await message.author.send(f'<@{message.author.id}>님 이메일이 전송되셨습니다!')
                time.sleep(2)
        except asyncio.TimeoutError:
                try:
                    await message.author.send("> :x: 시간이 초과 되셨습니다! :x:")
                except:
                    pass
                return
        await message.author.send("> ✅ 이메일로 온 코드를 입력해주세요 ✅")
        try:
                get_code = await client.wait_for("message", timeout=60, check=msg_channel_check1)
                get_code_content = get_code.content
        except asyncio.TimeoutError:
                try:
                    await message.author.send("> :x: 시간이 초과 되셨습니다! :x:")
                except:
                    pass
                return
        if int(get_code_content) in verify_code:
            await message.author.send('인증완료!')
            fucking_user = message.author
            role = discord.utils.get(message.guild.roles, name="인증댐") #역할이름
            await fucking_user.add_roles(role)
        else:
            await message.author.send('다시 시도 해 주세요.')               

client.run(토큰)            