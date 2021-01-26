import hoshino
import sqlite3
import os
from hoshino import Service, priv, util, R, HoshinoBot
import math

sv = Service('hades', enable_on_default=True, help_="无")
DB_PATH = os.path.expanduser("~/.hoshino/rate.db")
base64 = '''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'''
helpp = '''
帮助
买家指令:
!o - 创建订单
!ca - 取消订单
!c - 完成订单
卖家指令
!a - 接受订单
!rej - 取消接受订单
!c - 完成订单
综合指令
!r - 显示汇率
!l - 显示目前待处理的订单
!s - 显示你目前的订单
如果要得到更多资讯请打 !help <指令>'''
helpo = '''
用法: !o <你有的等级> <你需要的等级> <你拥有的数量><需要的种类代码（见下）> 
栗子: !o 7 9 60 6 就代表要混合的9，你有60个7
用户: 任何非封禁用户

种类代码:
0 紫
1 黄
2 蓝
3 黄蓝
4 蓝紫
5 紫黄
6 蓝紫黄
给R9-10订单的提醒
一些红星等级的紫是比蓝黄贵，这是因为用户需求和供应的偏差
'''
helpca = '''
用法: !ca<订单ID>
栗子: !ca 123
用户: <订单ID>的卖家和买家

买方可以由于不可预见的情况或进行修改取消订单<订单ID>。
'''
helpc = '''
用法：!c <订单ID>
栗子: !c 123
用户: <订单ID>的卖家和买家

买方或卖方标记的订单<订单ID>已成功完成。
'''
helpa = '''
用法: !a <订单ID>
栗子: !a 123
用户：具有卖方资格的用户

卖方接受订单<订单ID>，并被分配为买方完成订单。'''
helprej = '''
用法: !rej <订单ID>
栗子: !rej 123
用户：<订单ID>的卖方

卖方拒绝订单<订单ID>，并将其恢复为待处理状态，以便其他卖方可以接手。
'''
helps = '''
用法:!s
用户:任何用户

查看自己现在所有未完成或取消的订单。
'''
helpl = '''
用法:!l <神器等级>
用户:任何用户

查询目前所有<神器等级>的待处理订单，以便卖家评估。'''
helpr = '''
用法:!r
用户:任何用户

查询目前的最新汇率（机器人将会发送图片，请耐心等待）'''


class CardRecordDAO:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self.connect() as conn:
            # group_id, user_id, card_id
            conn.execute(
                "CREATE TABLE IF NOT EXISTS orders"
                "(uidb INT NOT NULL, uids INT, stat INT NOT NULL, num INT NOT NULL, level INT NOT NULL, goal INT NOT NULL, oid INT NOT NULL, arttype INT NOT NULL, p INT NOT NULL, PRIMARY KEY(oid))"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS stats"
                "(uid INT NOT NULL, sell INT NOT NULL, buy INT NOT NULL, illegal INT NOT NULL, PRIMARY KEY(uid))"
            )

    def Getstat(self, uid):
        with self.connect() as conn:
            r = conn.execute(
                "SELECT * FROM stats WHERE uid=?", (uid,)
            ).fetchall()
        return r

    def aspt(self, uid):
        r = self.Getstat(uid)
        debug_print(r)
        r2 = r[0]
        temp = r2[1] + 1
        debug_print("aspt")
        debug_print(temp)
        debug_print(uid)
        with self.connect() as conn:
            conn.execute(
                "UPDATE stats SET sell=? WHERE uid=?", (temp, uid,),
            )
        return

    def abpt(self, uid):
        r = self.Getstat(uid)
        debug_print(r)
        r2 = r[0]
        temp = r2[2] + 1
        debug_print("abpt")
        debug_print(temp)
        debug_print(uid)
        with self.connect() as conn:
            conn.execute(
                "UPDATE stats SET buy=? WHERE uid=?", (temp, uid,),
            )
        return

    def createstat(self, uid):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO stats (uid,sell,buy,illegal) VALUES (?,0,0,0)", (uid,),
            )
        return

    def roundup(self, num, base):
        return int(math.floor(num / base)) * base

    def formatenum(self, num):
        if num < 20:
            msg = str(num)
        if num < 100 and num > 19:
            n = self.roundup(num, 10)
            msg = f"{n}"
            msg += "+"
        if num < 1000 and num > 99:
            n = self.roundup(num, 100)
            msg = f"{n}"
            msg += "+"
        if num > 999:
            n = self.roundup(num, 1000) / 1000
            msg = f"{n}"
            msg += "k+"
        return msg

    def add_order(self, uidb, num, level, goal, arttype, p):
        with self.connect() as conn:
            tempvar = conn.execute(
                "SELECT * FROM orders",
            ).fetchall()
            oid = len(tempvar) + 1
        debug_print(oid)
        with self.connect() as conn:
            r = conn.execute(
                "INSERT INTO orders (uidb, num, level, goal, stat, oid ,arttype ,p) VALUES (?, ?, ?, ?, 0, ?, ?, ?)",
                (uidb, num, level, goal, oid, arttype, p),
            ).fetchall()
        return oid

    def get_needed_arts(self, level, goal, num):
        r = -1
        if level == 4:
            if goal == 6:
                r = 2.5
            elif goal == 7:
                r = 4
            elif goal == 8:
                r = 5
            elif goal == 9:
                r = 7
            elif goal == 19:
                r = 7
        if level == 5:
            if goal == 6:
                r = 2
            elif goal == 7:
                r = 3
            elif goal == 8:
                r = 4
            elif goal == 9:
                r = 5
            elif goal == 19:
                r = 5
        if level == 6:
            if goal == 7:
                r = 2
            elif goal == 8:
                r = 3
            elif goal == 9:
                r = 4
            elif goal == 10:
                r = 7
            elif goal == 19:
                r = 4
            elif goal == 20:
                r = 8
        if level == 7:
            if goal == 8:
                r = 2
            elif goal == 9:
                r = 3
            elif goal == 10:
                r = 5
            elif goal == 19:
                r = 3
            elif goal == 20:
                r = 6
        if level == 8:
            if goal == 9:
                r = 2
            elif goal == 19:
                r = 2
            elif goal == 10:
                r = 4
            elif goal == 20:
                r = 5
        if level == 9:
            if goal == 10:
                r = 3
            elif goal == 20:
                r = 4
        return r

    def get_order_by_uid(self, uidb):
        with self.connect() as conn:
            r = conn.execute(
                "SELECT * FROM orders WHERE uidb=? AND stat<2", (uidb,)
            ).fetchall()
        return r

    def get_list(self, goal):
        with self.connect() as conn:
            r = conn.execute(
                "SELECT * FROM orders WHERE stat=0 AND goal=?", (goal,)
            ).fetchall()
        return r

    def get_order_by_oid(self, oid):
        with self.connect() as conn:
            r = conn.execute(
                "SELECT * FROM orders WHERE oid=?", (oid,)
            ).fetchall()
            r2 = r[0]
        return r2

    def formate(self, uidb, uids, oid, state, num, level, goal, arttype, p):
        statb = self.Getstat(uidb)
        statb2 = statb[0]
        buyerstat = self.formatenum(statb2[2])
        stats = ""
        artstr = ""
        if state == 0:
            stats = "待处理"
        if state == 1:
            stats = "接收"
        if state == 2:
            stats = "完成"
        if state == 4:
            stats = "取消"
        if arttype == 0:
            artstr = "紫"
            p2 = p
        if arttype == 1:
            artstr = "黄"
            p2 = p
        if arttype == 2:
            artstr = "蓝"
            p2 = p
        if arttype == 3:
            artstr = "黄+蓝"
            p2 = p / 2
        if arttype == 4:
            artstr = "蓝+紫"
            p2 = p / 2
        if arttype == 5:
            artstr = "紫+黄"
            p2 = p / 2
        if arttype == 6:
            artstr = "蓝+紫+黄"
            p2 = p / 3
        debug_print(uids)
        if uids == "None" or uids is None:
            debug_print("No")
            seller = "还没有"
        else:
            debug_print("Yes")
            stats = self.Getstat(uidb)
            debug_print(stats)
            stats2 = stats[0]
            sellererstat = self.formatenum(stats2[1])
            seller = f"[CQ:at,qq={uids}]({sellererstat}订单)"
        p2 = int(p2)
        buyer = f"[CQ:at,qq={uidb}]({buyerstat}订单)"
        msg = f"_______订单#{oid}_______\n买家：{buyer}\n卖家：{seller}\n目前状态：{stats}\n以{num}个{level}交换{p}个{goal}(各{p2}个{artstr})"
        return msg

    def cancel_order(self, oid):
        with self.connect() as conn:
            conn.execute(
                "UPDATE orders SET stat=4 WHERE oid=?", (oid,),
            )
        return

    def accept_order(self, oid, uids):
        with self.connect() as conn:
            conn.execute("UPDATE orders SET stat=1 WHERE oid=?", (oid,), )
            conn.execute("UPDATE orders SET uids=? WHERE oid=?", (uids, oid,), )
        return

    def complete_order(self, oid, uidb, uids):
        with self.connect() as conn:
            conn.execute(
                "UPDATE orders SET stat=2 WHERE oid=?", (oid,),
            )
        return

    def reject_order(self, oid):
        with self.connect() as conn:
            conn.execute("UPDATE orders SET stat=0 WHERE oid=?", (oid,), )
            conn.execute("UPDATE orders SET uids=null WHERE oid=?", (oid,), )
        return


debug_mode = False


def debug_print(msg):
    if debug_mode:
        print(msg)


db = CardRecordDAO(DB_PATH)


@sv.on_prefix("!help")
async def help(bot, ev):
    args = ev.message.extract_plain_text().split()
    if len(args) == 0:
        msg = helpp
        await bot.send(ev, msg)
        return
    debug_print(args[0])
    if args[0] == "o":
        msg = helpo
    if args[0] == "ca":
        msg = helpca
    if args[0] == "c":
        msg = helpc
    if args[0] == "a":
        msg = helpa
    if args[0] == "rej":
        msg = helprej
    if args[0] == "r":
        msg = helpr
    if args[0] == "l":
        msg = helpl
    if args[0] == "s":
        msg = helps
    await bot.send(ev, msg)


@sv.on_prefix("!r")
async def rate(bot, ev):
    msg = f"[CQ:cardimage,file=base64://{base64}]"
    await bot.send(ev, msg)


@sv.on_prefix('!a')
async def accept(bot, ev):
    is_su = hoshino.priv.check_priv(ev, hoshino.priv.SUPERUSER)
    uid = ev['user_id']
    args = ev.message.extract_plain_text().split()
    oid = int(args[0])
    row = db.get_order_by_oid(oid)
    r = db.Getstat(uid)
    debug_print(r)
    if not r:
        msg = f"欢迎[CQ:at,qq={uid}]第一次使用本系统，正在为你初始化"
        await bot.send(ev, msg)
        db.createstat(uid)
        msg = "初始化成功"
        await bot.send(ev, msg)
    if uid == row[0] and not is_su:
        msg = '你不能接受自己的订单'
        await bot.send(ev, msg)
        return
    if not all(item.isnumeric() for item in args):
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    if not row[2] == 0:
        msg = '订单并不处于能够接受的状态'
        await bot.send(ev, msg)
        return
    db.accept_order(oid, uid)
    row = db.get_order_by_oid(oid)
    msg = db.formate(row[0], row[1], row[6], row[2], row[3], row[4], row[5], row[7], row[8])
    debug_print(msg)
    await bot.send(ev, msg)


@sv.on_prefix('!rej')
async def reject(bot, ev):
    uid = ev['user_id']
    args = ev.message.extract_plain_text().split()
    oid = int(args[0])
    row = db.get_order_by_oid(oid)
    if uid != row[1]:
        msg = '非卖家无法拒绝订单'
        await bot.send(ev, msg)
        return
    if not all(item.isnumeric() for item in args):
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    if row[2] != 1:
        msg = '订单并不处于能够拒绝的状态'
        await bot.send(ev, msg)
        return
    db.reject_order(oid)
    row = db.get_order_by_oid(oid)
    msg = db.formate(row[0], row[1], row[6], row[2], row[3], row[4], row[5], row[7], row[8])
    debug_print(msg)
    await bot.send(ev, msg)


@sv.on_prefix('!c')
async def complete(bot, ev):
    uid = ev['user_id']
    args = ev.message.extract_plain_text().split()
    oid = int(args[0])
    row = db.get_order_by_oid(oid)
    if uid != row[0] and uid != row[1]:
        msg = '非买家或卖家无法完成订单'
        await bot.send(ev, msg)
        return
    if not all(item.isnumeric() for item in args):
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    if not row[2] == 1:
        msg = '订单并不处于能够完成的状态'
        await bot.send(ev, msg)
        return
    db.complete_order(oid, row[0], row[1])
    debug_print(row[0])
    debug_print(row[1])
    db.abpt(row[0])
    db.aspt(row[1])
    row = db.get_order_by_oid(oid)
    msg = db.formate(row[0], row[1], row[6], row[2], row[3], row[4], row[5], row[7], row[8])
    debug_print(msg)
    await bot.send(ev, msg)


@sv.on_prefix('!l')
async def listall(bot, ev):
    args = ev.message.extract_plain_text().split()
    if not args:
        await bot.send(ev, "缺失参数")
    if not all(item.isnumeric() for item in args):
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    goal = int(args[0])
    msg = f"_____ R{goal}待处理订单列表_____\n"
    r = db.get_list(goal)
    for row in r:
        debug_print(r)
        if row[7] == 0:
            artstr = "紫"
        if row[7] == 1:
            artstr = "黄"
        if row[7] == 2:
            artstr = "蓝"
        if row[7] == 3:
            artstr = "黄+蓝"
        if row[7] == 4:
            artstr = "蓝+紫"
        if row[7] == 5:
            artstr = "紫+黄"
        if row[7] == 6:
            artstr = "蓝+紫+黄"
        msg += f"#{row[6]}来自[CQ:at,qq={row[0]}],{row[3]}xR{row[4]}:{row[8]}xR{row[5]}({artstr}))\n"
    await bot.send(ev, msg)


@sv.on_prefix('!ca')
async def cancel(bot, ev):
    is_su = hoshino.priv.check_priv(ev, hoshino.priv.SUPERUSER)
    uid = ev['user_id']
    args = ev.message.extract_plain_text().split()
    oid = int(args[0])
    row = db.get_order_by_oid(oid)
    if uid != row[0] and uid != row[1] and not is_su:
        msg = '非买家或卖家无法取消订单'
        await bot.send(ev, msg)
        return
    if not all(item.isnumeric() for item in args):
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    if row[2] > 1:
        msg = '订单并不处于能够取消的状态'
        await bot.send(ev, msg)
        return
    db.cancel_order(oid)
    row = db.get_order_by_oid(oid)
    msg = db.formate(row[0], row[1], row[6], row[2], row[3], row[4], row[5], row[7], row[8])
    debug_print(msg)
    await bot.send(ev, msg)


@sv.on_prefix('!s')
async def stat(bot, ev):
    uid = ev['user_id']
    r = db.get_order_by_uid(uid)
    for row in r:
        msg = db.formate(row[0], row[1], row[6], row[2], row[3], row[4], row[5], row[7], row[8])
        await bot.send(ev, msg)


@sv.on_prefix('!o')
async def order(bot, ev):
    uid = ev['user_id']
    args = ev.message.extract_plain_text().split()
    r = db.Getstat(uid)
    debug_print(r)
    if not r:
        msg = f"欢迎[CQ:at,qq={uid}]第一次使用本系统，正在为你初始化"
        await bot.send(ev, msg)
        db.createstat(uid)
        msg = "初始化成功"
        await bot.send(ev, msg)
    if not all(item.isnumeric() for item in args):
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    level = int(args[0])
    goal = int(args[1])
    num = int(args[2])
    arttype = int(args[3])
    debug_print(f"{level}\n{goal}\n{num}")
    if len(args) < 3:
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    if num < 1:
        msg = '数字必须大于0'
        await bot.send(ev, msg)
        return
    if goal > 10:
        msg = '目前只支持购买r6到r10的神器'
        await bot.send(ev, msg)
        return
    if goal < 6:
        msg = '目前只支持购买r6到r10的神器'
        await bot.send(ev, msg)
        return
    if level > 9:
        msg = '目前只支持使用r4到r9的神器购买'
        await bot.send(ev, msg)
        return
    if level < 4:
        msg = '目前只支持使用r4到r9的神器购买'
        await bot.send(ev, msg)
        return
    if level >= goal:
        msg = '目前不支持反向购买'
        await bot.send(ev, msg)
        return
    if arttype > 6 or arttype < 0:
        msg = '无效参数'
        await bot.send(ev, msg)
        return
    else:
        if arttype == 0 and goal > 8:
            goaltemp = goal + 10
            n = db.get_needed_arts(level, goaltemp, num)
            p = int(num / n)
            debug_print("only tets")
        elif (arttype == 4 or arttype == 5) and goal > 8:
            numtemp = int(num / 2)
            goaltemp = goal + 10
            n1 = db.get_needed_arts(level, goal, numtemp)
            n2 = db.get_needed_arts(level, goaltemp, numtemp)
            n = (n1 + n2) / 2
            num = numtemp * 2
            p = int(int(num / n) / 2) * 2
            debug_print("2mix")
        elif arttype == 6 and goal > 8:
            numtemp = int(num / 3)
            goaltemp = goal + 10
            n1 = db.get_needed_arts(level, goal, numtemp) * 2
            n2 = db.get_needed_arts(level, goaltemp, numtemp)
            n = (n1 + n2) / 3
            num = numtemp * 3
            p = int(int(num / n) / 3) * 3
            debug_print("Mixed")
            if db.get_needed_arts(level, goaltemp, num) < 0:
                msg = "无效比率"
                await bot.send(ev, msg)
                return
        elif arttype == 6 and goal < 9:
            n = db.get_needed_arts(level, goal, num)
            p = int((num / n) / 3) * 3
            debug_print("OtherMix")
            if db.get_needed_arts(level, goal, num) < 0:
                msg = "无效比率"
                await bot.send(ev, msg)
                return
        elif (arttype == 4 or arttype == 5) and goal < 9:
            n = db.get_needed_arts(level, goal, num)
            p = int((num / n) / 2) * 2
            debug_print("Other2")
            if db.get_needed_arts(level, goal, num) < 0:
                msg = "无效比率"
                await bot.send(ev, msg)
                return
        elif arttype == 3:
            n = db.get_needed_arts(level, goal, num)
            p = int((num / n) / 2) * 2
            debug_print("Other2")
            if db.get_needed_arts(level, goal, num) < 0:
                msg = "无效比率"
                await bot.send(ev, msg)
                return
        else:
            n = db.get_needed_arts(level, goal, num)
            p = int(num / n)
            debug_print("Other")
            if db.get_needed_arts(level, goal, num) < 0:
                msg = "无效比率"
                await bot.send(ev, msg)
                return
        num = math.ceil(n * p)
        oid = db.add_order(uid, num, level, goal, arttype, p)
        msg = db.formate(uid, "None", oid, 0, num, level, goal, arttype, p)
    await bot.send(ev, msg)
