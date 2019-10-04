import wx
import datetime
import os
import autopy
import time
import threading
from bs4 import BeautifulSoup


class Wind(wx.Frame):

    def __init__(self, parent, title, path_p, path_s):

        wx.Frame.__init__(self, parent, title=title, pos=(0, 0), size=(300, 300), style=wx.MINIMIZE_BOX |
                                                                                        wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.STAY_ON_TOP)
        self.script = []
        self.path = path_s
        self.path_p = path_p
        self.read()
        self.ruler = None
        self.cris = Cristina()
        self.Magi = None
        self.isClose = False

        self.panel = wx.Panel(self, pos=(0, 0), size=(300, 130))
        self.panel_1 = wx.Panel(self.panel, pos=(0, 0), size=(300, 50))
        # self.panel_1.SetBackgroundColour(wx.BLUE)
        self.panel_2 = wx.Panel(self.panel, pos=(0, 50), size=(300, 50))
        # self.panel_2.SetBackgroundColour(wx.RED)
        self.panel_3 = wx.Panel(self.panel, pos=(0, 100), size=(300, 30))
        # self.panel_3.SetBackgroundColour(wx.YELLOW)
        self.panel_4 = wx.Panel(self, pos=(0, 130), size=(300, 130))
        # self.panel_4.SetBackgroundColour(wx.GREEN)

        self.combo = wx.ComboBox(self.panel_1, pos=(15, 10), size=(120, 30), style=wx.CB_READONLY, choices=self.script)
        self.combo.SetSelection(0)
        self.btn_load = wx.Button(self.panel_1, pos=(165, 10), size=(50, 25), label='Load')
        self.btn_load.Bind(wx.EVT_BUTTON, self.on_load)
        self.btn_flash = wx.Button(self.panel_1, pos=(225, 10), size=(50, 25), label='Flash')
        self.btn_flash.Bind(wx.EVT_BUTTON, self.flash)

        self.slider = wx.Slider(self.panel_2, pos=(15, 10), size=(120, 30), value=7, minValue=0, maxValue=50)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slide)
        self.text_input = wx.TextCtrl(self.panel_2, pos=(165, 10), size=(50, 25), value=str(self.slider.GetValue()))
        self.text_input.Bind(wx.EVT_TEXT, self.on_input)
        self.btn_confirm = wx.Button(self.panel_2, pos=(225, 10), size=(50, 25), label='Confirm')
        self.btn_confirm.Bind(wx.EVT_BUTTON, self.on_confirm)

        self.check_close = wx.CheckBox(self.panel_3, pos=(15, 10), label='Close? ', style=wx.ALIGN_RIGHT)
        self.check_close.Bind(wx.EVT_CHECKBOX, self.on_close)
        self.check_stone = wx.CheckBox(self.panel_3, pos=(75, 10), label='Stone? ', style=wx.ALIGN_RIGHT)
        self.btn_start = wx.Button(self.panel_3, pos=(165, 5), size=(50, 25), label='Start')
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_start)
        self.btn_reset = wx.Button(self.panel_3, pos=(225, 5), size=(50, 25), label='Reset')
        self.btn_reset.Bind(wx.EVT_BUTTON, self.on_reset)

        self.text_msg = wx.TextCtrl(self.panel_4, pos=(15, 10), size=(250, 100), style=wx.TE_MULTILINE)
        self.collapse = wx.Button(self.panel_4, pos=(265, 10), size=(20, 20), label='C')
        self.collapse.Bind(wx.EVT_BUTTON, self.on_collapse)
        self.expand = wx.Button(self.panel_4, pos=(265, 30), size=(20, 20), label='E')
        self.expand.Bind(wx.EVT_BUTTON, self.on_expand)
        self.clear = wx.Button(self.panel_4, pos=(265, 50), size=(20, 20), label='R')
        self.clear.Bind(wx.EVT_BUTTON, self.on_clear)

        self.Bind(wx.EVT_CLOSE, self.on_kill_thread)

        self.Show()

    def on_kill_thread(self, e):
        try:
            if self.Magi is not None:
                self.Magi.stop = True
            # self.Show(False)
            wx.Exit()
        except Exception:
            self.message('Exit Error Occurred')

    def read(self):
        for path, dir, files in os.walk(self.path):
            for file in files:
                self.script.append(file.split('.')[0])

    def flash(self, e):
        self.read()
        self.message('Flashed')

    def message(self, msg):
        stamp = datetime.datetime.now()
        now_time = stamp.strftime('%H:%M')
        self.text_msg.AppendText(now_time + "  Jeanne d'Arc  :  " + msg + '\n')

    def on_load(self, e):
        root = self.path + '/' + self.combo.GetStringSelection() + '.txt'
        self.ruler = Ruler(root)
        self.message('Loaded-' + self.ruler.title)
        self.message('Detail-' + self.ruler.detail)

    def on_slide(self, e):
        value = self.slider.GetValue()
        self.text_input.SetLabelText(str(value))

    def on_input(self, e):
        value = int(self.text_input.GetValue())
        if value < 0:
            self.slider.SetValue(0)
        elif value > 50:
            self.slider.SetValue(50)
        else:
            self.slider.SetValue(value)

    def on_confirm(self, e):
        if self.ruler is not None:
            self.Magi = Core(self.slider.GetValue(), self.ruler, self)
            self.message('All set Ready to Roll')
        else:
            self.message("Didn't select ruler")

    def on_start(self, e):
        if self.Magi is not None and self.Magi.thread.isAlive():
            self.message('Already start')
        elif self.Magi is None:
            self.message("Didn't confirm")
        elif self.ruler is None:
            self.message("Didn't select Ruler")
        else:
            self.Magi.thread.start()

    def on_reset(self, e):
        if self.Magi is None:
            self.message("Didn't Confirm")
        else:
            self.Magi.stop = True
            self.Magi = None
            self.ruler = None
            self.message('All Reset')

    def on_close(self, e):
        self.isClose = self.check_close.GetValue()
        self.message('After Finished Close Monitor')

    def on_collapse(self, e):
        self.message('Collapsed')
        self.panel_4.SetPosition((0, 0))
        self.panel.SetPosition((0, 130))
        self.SetSize((300, 160))

    def on_expand(self, e):
        self.message('Expanded')
        self.panel.SetPosition((0, 0))
        self.panel_4.SetPosition((0, 130))
        self.SetSize((300, 300))
        pass

    def on_clear(self, e):
        self.text_msg.SetLabelText('')


class Core:

    def __init__(self, loop, ruler, wind):
        self.loop = loop
        self.Jeanne = ruler
        self.wind = wind
        self.cris = Cristina()
        self.stop = False
        self.thread = threading.Thread(target=self.start)

    def initialize(self):

        pass

    def stop_thread(self):
        if self.stop:
            exit(0)

    def start(self):
        self.wind.message('Target ' + str(self.loop) + ' loop')
        try:
            for i in range(self.loop):
                self.entrance()
                self.battle(500)
                self.end()
                self.wind.message('Finished ' + str(i + 1) + ' loop')
            self.wind.message('All Finished')
        except:
            self.wind.message('Location Beyond')
        if self.wind.isClose:
            Cristina.click(pos=self.cris.p_close, aft=1)
            Cristina.click(pos=self.cris.p_close_confirm, aft=1)

    def entrance(self):
        self.stop_thread()
        Cristina.click(self.cris.p_entrance, bef=5, aft=2)
        screen = autopy.bitmap.capture_screen()
        if screen.find_bitmap(self.cris.sapple):
            print('Found sapple')
            Cristina.click(self.cris.p_silverapple, aft=2)
            print('Clicked')
            Cristina.click(self.cris.p_appleconfirm, aft=4)
            print('Confirmed')
        elif screen.find_bitmap(self.cris.gapple):
            print('Found Gapple')
            Cristina.click(self.cris.p_goldapple, aft=2)
            print('Clicked')
            Cristina.click(self.cris.p_appleconfirm, aft=4)
            print('Confirmed')
        elif screen.find_bitmap(self.cris.stone) and self.wind.check_stone.GetValue():
            Cristina.click(self.cris.p_silverapple, aft=2)
            Cristina.click(self.cris.p_appleconfirm, aft=4)
        self.stop_thread()
        Cristina.click(self.cris.p_support, aft=4)
        self.stop_thread()
        Cristina.click(self.cris.p_startbattle, aft=20)
        self.stop_thread()

    def get_round(self):

        if Cristina.judge_color(self.cris.p_rnumber1, (151, 151, 151), limit=50):
            return 1
        if Cristina.judge_color(self.cris.p_rnumber2, (238, 238, 238), limit=50):
            return 2
        return 3

    def battle(self, timelimit):
        clock = 0
        round = 0
        while clock < timelimit:
            screen = autopy.bitmap.capture_screen()
            if screen.find_bitmap(self.cris.attack):
                newround = not (round == self.get_round())
                round = self.get_round()

                self.Jeanne.round_select(round, newround)
                self.stop_thread()

                time.sleep(7)
            if screen.find_bitmap(self.cris.end):
                return

    def end(self):
        self.stop_thread()
        Cristina.click(self.cris.p_empty, aft=1)
        self.stop_thread()
        Cristina.click(self.cris.p_empty, aft=1)
        self.stop_thread()
        Cristina.click(self.cris.p_empty, aft=1)
        self.stop_thread()
        Cristina.click(self.cris.p_empty, aft=1)
        self.stop_thread()
        Cristina.click(self.cris.p_empty, aft=1)
        self.stop_thread()
        Cristina.click(self.cris.p_endconfirm, aft=15)
        self.stop_thread()
        Cristina.click(self.cris.p_empty, aft=3)
        self.stop_thread()


class Ruler:

    def __init__(self, path):
        self.title = ''
        self.detail = ''
        self.max_round = ''
        self.total_order = []
        self.skill_list = []
        self.order_list = []
        self.cris = Cristina()
        self.read(path)

    def read(self, path):
        with open(path, 'r') as file:
            string = file.read()
            soup = BeautifulSoup(string, 'lxml')
            self.skill_list = []
            self.order_list = []
            for r in soup.body.find_all('round'):
                sk = []
                for skill in r.find_all('skill'):
                    sk.append(skill.string.strip())
                self.skill_list.append(sk)
                orde = []
                for order in r.find_all('order'):
                    orde.append(order.string.strip())
                self.order_list.append(orde)
            self.title = soup.title.string
            self.detail = soup.detail.string

    def select_skill(self, round):
        for order in self.skill_list[round - 1]:
            a = order[:3]
            aft = 3
            if len(order) > 3:
                aft = 1.5
            if a == 'A_1':
                Cristina.click(self.cris.p_sk11, aft=aft)
            elif a == 'A_2':
                Cristina.click(self.cris.p_sk12, aft=aft)
            elif a == 'A_3':
                Cristina.click(self.cris.p_sk13, aft=aft)
            elif a == 'B_1':
                Cristina.click(self.cris.p_sk21, aft=aft)
            elif a == 'B_2':
                Cristina.click(self.cris.p_sk22, aft=aft)
            elif a == 'B_3':
                Cristina.click(self.cris.p_sk23, aft=aft)
            elif a == 'C_1':
                Cristina.click(self.cris.p_sk31, aft=aft)
            elif a == 'C_2':
                Cristina.click(self.cris.p_sk32, aft=aft)
            elif a == 'C_3':
                Cristina.click(self.cris.p_sk33, aft=aft)
            elif a == 'E_1':
                Cristina.click(self.cris.p_e1, aft=0.5)
            elif a == 'E_2':
                Cristina.click(self.cris.p_e2, aft=0.5)
            elif a == 'E_3':
                Cristina.click(self.cris.p_e3, aft=0.5)
            elif a == 'M_1':
                Cristina.click(self.cris.p_msk, aft=0.5)
                Cristina.click(self.cris.p_msk1, aft=aft)
            elif a == 'M_2':
                Cristina.click(self.cris.p_msk, aft=0.5)
                Cristina.click(self.cris.p_msk2, aft=aft)
            elif a == 'M_3':
                Cristina.click(self.cris.p_msk, aft=0.5)
                Cristina.click(self.cris.p_msk3, aft=aft)
            if order.count('_') == 2:
                Cristina.click(self.cris.p_skt[int(order[-1])], aft=3)
            if order.count('_') == 3:
                Cristina.click(self.cris.p_mskswitch[int(order[-3])], aft=0.5)
                Cristina.click(self.cris.p_mskswitch[int(order[-1])], aft=5)

    def round_select(self, round, news):
        if news:
            self.select_skill(round)
        Cristina.click(self.cris.p_attack, aft=1.5)
        self.select_card(round)

    def distance(self, source, target, limit=70):
        if abs(source[0] - target[0]) > limit:
            return False
        if abs(source[1] - target[1]) > limit:
            return False
        if abs(source[2] - target[2]) > limit:
            return False
        return True

    def transform(self, lis):
        res = []
        for i in lis:
            if self.distance(i, self.cris.rbg_a):
                res.append('A')
            elif self.distance(i, self.cris.rbg_b):
                res.append('B')
            else:
                res.append('Q')
        return res

    def get_color(self, fig):
        avglist = []
        for j in range(5):

            lis = []
            r = 0
            g = 0
            b = 0
            for i in range(10):
                lis.append(fig.get_color(self.cris.p_carddet[j], self.cris.p_carddety + 2 * i))
            for i in lis:
                r += i[0]
                g += i[1]
                b += i[2]
            avg = (r // 10, g // 10, b // 10)
            avglist.append(avg)
        return self.transform(avglist)

    def get_seq(self, lis, orders):
        res = []
        for i in range(5):
            try:
                res.append(lis.index(orders) + 1)
                lis[lis.index(orders)] = '-1'
            except:
                break
        return res

    def select_card(self, round):
        time.sleep(1)
        colorlis = self.get_color(autopy.bitmap.capture_screen())
        clicklist = []
        for order in self.order_list[round - 1]:
            if order == 'H1':
                clicklist.append(self.cris.p_carda)
            elif order == 'H2':
                clicklist.append(self.cris.p_cardb)
            elif order == 'H3':
                clicklist.append(self.cris.p_cardc)
            else:
                for i in self.get_seq(colorlis, order):
                    clicklist.append(self.cris.p_card[i])
        for i in clicklist[:5]:
            Cristina.click(i)


class Cristina:

    def __init__(self):
        self.xpix = 1920
        self.ypix = 1080

        self.p_entrance = (1660, 320)
        self.p_stone = (700, 300)
        self.p_goldapple = (700, 500)
        self.p_silverapple = (700, 700)
        self.p_appleconfirm = (1232, 820)
        self.p_support = (700, 445)
        self.p_startbattle = (1719, 975)

        self.p_e1 = (255, 420)
        self.p_e2 = (475, 103)
        self.p_e3 = (902, 103)

        self.p_sk11 = (170, 840)
        self.p_sk12 = (300, 840)
        self.p_sk13 = (430, 840)
        self.p_sk21 = (610, 840)
        self.p_sk22 = (740, 840)
        self.p_sk23 = (870, 840)
        self.p_sk31 = (1050, 840)
        self.p_sk32 = (1175, 840)
        self.p_sk33 = (1300, 840)

        self.p_skt = [(), (520, 660), (960, 660), (1400, 660)]

        self.p_msk = (1720, 470)
        self.p_msk1 = (1320, 475)
        self.p_msk2 = (1450, 475)
        self.p_msk3 = (1570, 475)

        self.p_mskswitch = [(), (270, 520), (540, 520), (820, 520), (1100, 520), (1370, 520), (1640, 520)]

        self.p_card = [(), (255, 745), (610, 745), (960, 745), (1310, 745), (1670, 745)]
        self.p_carda = (650, 340)
        self.p_cardb = (960, 340)
        self.p_cardc = (1300, 340)

        self.p_carddet = [257, 612, 966, 1324, 1683]
        self.p_carddety = 835
        self.rbg_a = (120, 230, 245)
        self.rbg_b = (251, 241, 97)

        self.p_rnumber1 = (1280, 75)
        self.p_rnumber2 = (1280, 86)
        self.p_attack = (1640, 860)

        self.p_empty = (152, 413)
        self.p_endconfirm = (1600, 980)

        self.p_close = (1893, 20)
        self.p_close_confirm = (1040, 557)

        self.gapple = autopy.bitmap.Bitmap.open(path_photo + 'gApple.png')
        self.sapple = autopy.bitmap.Bitmap.open(path_photo + 'sApple.png')
        self.stone = autopy.bitmap.Bitmap.open(path_photo + 'stone.png')

        self.attack = autopy.bitmap.Bitmap.open(path_photo + 'Attack.png')
        self.end = autopy.bitmap.Bitmap.open(path_photo + 'end.png')

    @classmethod
    def auto_adjust(csl, x, y):

        pass

    @classmethod
    def judge_color(cls, pos, color, limit=20):
        screen = autopy.bitmap.capture_screen()
        col = screen.get_color(pos[0], pos[1])
        if abs(col[0] - color[0]) > limit:
            return False
        if abs(col[1] - color[1]) > limit:
            return False
        if abs(col[2] - color[2]) > limit:
            return False
        return True

    @classmethod
    def click(cls, pos, bef=0.1, aft=0.3):
        time.sleep(bef)
        autopy.mouse.move(pos[0], pos[1])
        autopy.mouse.toggle(down=True)
        time.sleep(0.1)
        autopy.mouse.toggle(down=False)
        time.sleep(aft)


def search_path(target):
    root = './'
    for i in range(3):
        lis = os.listdir(root)
        if target not in lis:
            root = '.' + root
        else:
            return root


if __name__ == '__main__':
    path_photo = search_path('Photos') + 'Photos/'
    path_script = search_path('Scripts') + 'Scripts/'
    app = wx.App(False)
    frame = Wind(None, "Jeanne d'Arc", path_photo, path_script)
    app.MainLoop()
