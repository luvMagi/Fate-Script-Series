# -*- coding: utf-8 -*-

import wx
import wx.xrc
import os
import win32api, win32con
import autopy
import time
import datetime
import threading
import inspect
import ctypes
# import win32process
from bs4 import BeautifulSoup


class FateK(wx.Frame):

    def __init__(self, parent, app):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Jeanne d'Arc", pos=(0, 0),
                          size=wx.Size(300, 320),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.STAY_ON_TOP | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.app = app
        self.SetMaxSize((300, 320))
        self.SetMinSize((300, 160))
        self.edit_state = False
        self.cris = self.Cristina()
        self.editor = self.FateKE(None, self.cris)
        self.Jeanne = None
        self.Magi = self.Core(self)
        self.state = 'E'

        self.const_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.sizer_base = wx.BoxSizer(wx.VERTICAL)
        self.text_message = wx.TextCtrl(self.const_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_MULTILINE | wx.TE_READONLY)

        self.script_list = self.get_script_list()

        self.cons_sizer = wx.BoxSizer(wx.VERTICAL)

        self.sizer_top_group = wx.GridSizer(0, 2, 0, 0)

        sizer_top_left_group = wx.BoxSizer(wx.VERTICAL)

        self.combo = wx.ComboBox(self.const_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                 self.script_list, wx.CB_DROPDOWN | wx.CB_READONLY)
        self.combo.SetSelection(0)
        self.combo.Bind(wx.EVT_COMBOBOX, self.on_combo_change)
        sizer_top_left_group.Add(self.combo, 0, wx.ALL, 5)

        self.slider = wx.Slider(self.const_panel, wx.ID_ANY, 7, 0, 48, wx.DefaultPosition, wx.DefaultSize,
                                wx.SL_HORIZONTAL)
        sizer_top_left_group.Add(self.slider, 0, wx.ALL, 5)

        sizer_checks_group_1 = wx.BoxSizer(wx.HORIZONTAL)

        self.check_close = wx.CheckBox(self.const_panel, wx.ID_ANY, u"Close?", wx.DefaultPosition, wx.DefaultSize,
                                       wx.ALIGN_RIGHT)
        sizer_checks_group_1.Add(self.check_close, 0, wx.TOP | wx.BOTTOM | wx.RIGHT, 5)

        self.check_stone = wx.CheckBox(self.const_panel, wx.ID_ANY, u"Stone?", wx.DefaultPosition, wx.DefaultSize,
                                       wx.ALIGN_RIGHT)
        sizer_checks_group_1.Add(self.check_stone, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        sizer_top_left_group.Add(sizer_checks_group_1, 1, wx.EXPAND, 5)

        sizer_checks_group_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.check_send = wx.CheckBox(self.const_panel, wx.ID_ANY, u"Send?", wx.DefaultPosition, wx.DefaultSize,
                                      wx.ALIGN_RIGHT)
        sizer_checks_group_2.Add(self.check_send, 0, wx.ALL, 5)

        sizer_top_left_group.Add(sizer_checks_group_2, 1, wx.EXPAND, 5)

        self.sizer_top_group.Add(sizer_top_left_group, 1, wx.EXPAND, 5)

        sizer_top_right_group = wx.BoxSizer(wx.VERTICAL)

        gSizer4 = wx.GridSizer(4, 2, 0, 0)

        self.btn_load = wx.Button(self.const_panel, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize,
                                  wx.NO_BORDER)
        self.btn_load.SetMaxSize(wx.Size(50, 50))

        gSizer4.Add(self.btn_load, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        self.btn_flash = wx.Button(self.const_panel, wx.ID_ANY, u"Flash", wx.DefaultPosition, wx.DefaultSize,
                                   wx.NO_BORDER)
        self.btn_flash.SetMaxSize(wx.Size(50, 50))

        gSizer4.Add(self.btn_flash, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        self.text_times = wx.TextCtrl(self.const_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                      0)
        self.text_times.SetMaxSize(wx.Size(50, -1))

        self.text_times.SetValue(str(self.slider.GetValue()))

        gSizer4.Add(self.text_times, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.btn_confirm = wx.Button(self.const_panel, wx.ID_ANY, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_confirm.SetMaxSize(wx.Size(50, -1))

        gSizer4.Add(self.btn_confirm, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.btn_start = wx.Button(self.const_panel, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_start.SetMaxSize(wx.Size(50, -1))

        gSizer4.Add(self.btn_start, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.btn_reset = wx.Button(self.const_panel, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_reset.SetMaxSize(wx.Size(50, -1))

        gSizer4.Add(self.btn_reset, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.btn_edit = wx.Button(self.const_panel, wx.ID_ANY, u"Editor", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_edit.SetMaxSize(wx.Size(50, -1))

        gSizer4.Add(self.btn_edit, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.btn_setting = wx.Button(self.const_panel, wx.ID_ANY, u"Setting", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer4.Add(self.btn_setting, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        sizer_top_right_group.Add(gSizer4, 1, wx.EXPAND, 5)

        self.sizer_top_group.Add(sizer_top_right_group, 1, wx.EXPAND, 5)

        self.sizer_base.Add(self.sizer_top_group, 1, wx.EXPAND, 5)

        self.sizer_bottom_group = wx.BoxSizer(wx.HORIZONTAL)


        self.sizer_bottom_group.Add(self.text_message, 9, wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.TOP, 5)

        sizer_bot_right_btn_group = wx.BoxSizer(wx.VERTICAL)

        self.btn_collapse = wx.Button(self.const_panel, wx.ID_ANY, u"C", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_collapse.SetMaxSize(wx.Size(25, 25))

        sizer_bot_right_btn_group.Add(self.btn_collapse, 0, wx.TOP, 5)

        self.btn_expand = wx.Button(self.const_panel, wx.ID_ANY, u"E", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_expand.SetMaxSize(wx.Size(25, 25))

        sizer_bot_right_btn_group.Add(self.btn_expand, 0, 0, 5)
        self.btn_clear = wx.Button(self.const_panel, wx.ID_ANY, u"R", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_clear.SetMaxSize(wx.Size(25, 25))

        sizer_bot_right_btn_group.Add(self.btn_clear, 0, 0, 5)

        self.btn_start_b = wx.Button(self.const_panel, wx.ID_ANY, u"S", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btn_start_b.SetMaxSize(wx.Size(25, 25))

        sizer_bot_right_btn_group.Add(self.btn_start_b, 0, 0, 5)

        self.sizer_bottom_group.Add(sizer_bot_right_btn_group, 1, 0, 5)

        self.sizer_base.Add(self.sizer_bottom_group, 1, wx.EXPAND, 5)

        self.const_panel.SetSizer(self.sizer_base)
        self.const_panel.Layout()
        self.sizer_base.Fit(self.const_panel)
        self.cons_sizer.Add(self.const_panel, 1, wx.EXPAND, 5)

        self.SetSizer(self.cons_sizer)
        self.Layout()

        self.Magi.set_loop(self.slider.GetValue())
        self.message('Target Loop: ' + str(self.Magi.loop))
        self.message('All Set')

        # Connect Events
        self.slider.Bind(wx.EVT_SCROLL, self.on_flash_text)
        # self.btn_load.Bind(wx.EVT_BUTTON, self.on_click_load)
        self.btn_load.Enable(False)
        self.btn_flash.Bind(wx.EVT_BUTTON, self.on_click_flash)
        self.text_times.Bind(wx.EVT_TEXT, self.on_flash_slider)
        # self.btn_confirm.Bind(wx.EVT_BUTTON, self.on_confirm)
        self.btn_confirm.Enable(False)
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_click_start)
        self.btn_reset.Bind(wx.EVT_BUTTON, self.on_click_reset)
        self.btn_edit.Bind(wx.EVT_BUTTON, self.on_click_editor)
        # self.btn_setting.Bind(wx.EVT_BUTTON, self.on_click_setting)
        self.btn_setting.Enable(False)
        self.btn_collapse.Bind(wx.EVT_BUTTON, self.on_click_collapse)
        self.btn_expand.Bind(wx.EVT_BUTTON, self.on_click_expand)
        self.btn_clear.Bind(wx.EVT_BUTTON, self.on_click_clear)
        self.btn_start_b.Bind(wx.EVT_BUTTON, self.on_click_start)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def message(self, msg):
        stamp = datetime.datetime.now()
        now_time = stamp.strftime('%H:%M')
        self.text_message.AppendText(now_time + "  Jeanne d'Arc  :  " + msg + '\n')

    def get_script_list(self):
        tmp = []
        for i in os.listdir(self.cris.path_script):
            tmp.append(i.split('.')[0])
        root = self.cris.path_script + '/' + tmp[0] + '.txt'
        self.Jeanne = self.Ruler(self.cris, root)
        self.message('Loaded-' + self.Jeanne.title)
        self.message('Detail-' + self.Jeanne.detail)
        return tmp

    def on_flash_text(self, event):
        self.text_times.SetLabelText(str(self.slider.GetValue()))
        self.Magi.set_loop(self.slider.GetValue())

    def on_click_flash(self, event):
        self.script_list = self.get_script_list()
        self.combo.SetItems(self.script_list)
        self.combo.SetSelection(0)
        root = self.cris.path_script + '/' + self.combo.GetStringSelection() + '.txt'
        self.Jeanne = self.Ruler(self.cris, root)
        self.message('Loaded-' + self.Jeanne.title)
        self.message('Detail-' + self.Jeanne.detail)

    def on_combo_change(self, e):
        root = self.cris.path_script + '/' + self.combo.GetStringSelection() + '.txt'
        self.Jeanne = self.Ruler(self.cris, root)
        self.message('Loaded-' + self.Jeanne.title)
        self.message('Detail-' + self.Jeanne.detail)
        self.message('Target Loop: ' + str(self.Magi.loop))
        self.message('All Set')

    def on_flash_slider(self, event):
        try:
            value = int(self.text_times.GetValue())
            if value < 0:
                self.slider.SetValue(0)
            elif value > 50:
                self.slider.SetValue(50)
            else:
                self.slider.SetValue(value)
            self.Magi.set_loop(self.slider.GetValue())
        except:
            pass

    def on_confirm(self, event):

        self.message('Target Loop: ' + str(self.Magi.loop))
        self.message('All Set')

    def on_click_start(self, event):
        self.Magi.thread_start = threading.Thread(target=self.Magi.start)
        self.Magi.thread_start.start()
        self.message('ミッション、スタート')

    def on_click_reset(self, event):
        self.Magi.thread_stop = threading.Thread(target=self.Magi.stop_thread)
        self.Magi.thread_stop.start()

    def on_click_editor(self, event):

        # try:
        #     win32process.CreateProcess(self.cris.path_editor + 'Fate~KE.exe', '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None,
        #                            win32process.STARTUPINFO())
        # except Exception as e:
        #     self.message('Could not find Editor')

        if self.edit_state:
            self.editor.Hide()
            self.edit_state = False
        else:
            self.edit_state = True
            self.editor.Show()

    def on_click_setting(self, event):
        event.Skip()

    def on_click_collapse(self, event):
        if self.state is 'E':
            self.sizer_base.Hide(0)
            self.SetSize((300, 150))
            self.sizer_base.Layout()
            self.cons_sizer.Layout()
            self.state = 'C'
            self.message('Collapse')

    def on_click_expand(self, event):
        if self.state is 'C':
            self.sizer_base.Show(0)
            self.SetSize((300, 320))
            self.sizer_base.Layout()
            self.cons_sizer.Layout()
            self.state = 'E'
            self.message('Expand')

    def on_click_clear(self, event):
        self.text_message.SetValue('')

    def on_close(self, e):
        if self.btn_reset.IsEnabled() and self.Magi.thread_start is not None:
            self.Magi.async_raise(self.Magi.thread_start.ident, SystemExit)
        app.ExitMainLoop()

    class Core:

        def __init__(self, witch):
            self.loop = -1
            self.Jeanne = None
            self.witch = witch
            self.cris = witch.cris
            self.thread_start = None
            self.thread_stop = None

        def set_loop(self, n):
            self.loop = n

        def set_ruler(self, ruler):
            self.Jeanne = ruler

        def async_raise(self, tid, exctype):
            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:                # and you should call it again with exc=NULL to revert the effect"""

                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        def stop_thread(self):
            if self.thread_start is not None:
                self.witch.btn_reset.Enable(False)
                self.async_raise(self.thread_start.ident, SystemExit)
                self.witch.message('Thread Stopped')
                self.thread_start = None
                time.sleep(3)
                if self.witch.btn_reset.Enable:
                    self.witch.btn_reset.Enable(True)
            else:
                self.witch.message('Did Not Run')

        def start(self):
            try:
                index = 0
                while True:
                    index += 1
                    if index > self.loop:
                        break
                    self.witch.message('Start ' + str(index) + '/' + str(self.loop))
                    self.entrance()
                    self.battle(500)
                    self.end()
                    self.witch.message('Finished ' + str(index + 1) + ' loop')

                self.witch.message('All Finished')
                if self.witch.check_close.GetValue():
                    self.cris.click(pos=self.cris.p_close, aft=1)
                    self.cris.click(pos=self.cris.p_close_confirm, aft=1)
            except RuntimeError as e:
                self.witch.message(e)
                if self.witch.check_close.GetValue():
                    self.cris.click(pos=self.cris.p_close, aft=1)
                    self.cris.click(pos=self.cris.p_close_confirm, aft=1)
            except Exception as e:
                self.witch.message(e)

        def entrance(self):
            self.cris.click(self.cris.p_entrance, bef=5, aft=2)
            screen = autopy.bitmap.capture_screen()
            if screen.find_bitmap(self.cris.sapple):
                self.cris.click(self.cris.p_silverapple, aft=2)
                self.cris.click(self.cris.p_appleconfirm, aft=4)
            elif screen.find_bitmap(self.cris.gapple):
                self.cris.click(self.cris.p_goldapple, aft=2)
                self.cris.click(self.cris.p_appleconfirm, aft=4)
            elif screen.find_bitmap(self.cris.stone) and self.witch.check_stone.GetValue():
                self.cris.click(self.cris.p_silverapple, aft=2)
                self.cris.click(self.cris.p_appleconfirm, aft=4)
            self.cris.click(self.cris.p_support, aft=4)
            self.cris.click(self.cris.p_startbattle, aft=20)

        def get_round(self):

            if self.cris.judge_color(self.cris.p_rnumber1, (151, 151, 151), limit=50):
                return 1
            if self.cris.judge_color(self.cris.p_rnumber2, (238, 238, 238), limit=50):
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

                    time.sleep(7)
                if screen.find_bitmap(self.cris.end):
                    return
            raise RuntimeError('Runtime Error!')

        def end(self):
            self.cris.click(self.cris.p_empty, aft=1)
            self.cris.click(self.cris.p_empty, aft=1)
            self.cris.click(self.cris.p_empty, aft=1)
            self.cris.click(self.cris.p_empty, aft=1)
            self.cris.click(self.cris.p_empty, aft=1)
            self.cris.click(self.cris.p_endconfirm, aft=15)
            self.cris.click(self.cris.p_empty, aft=3)

    class Ruler:

        def __init__(self, cris, root):
            self.title = ''
            self.detail = ''
            self.max_round = ''
            self.total_order = []
            self.skill_list = []
            self.order_list = []
            self.cris = cris
            self.read(root)

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
                    self.cris.click(self.cris.p_sk11, aft=aft)
                elif a == 'A_2':
                    self.cris.click(self.cris.p_sk12, aft=aft)
                elif a == 'A_3':
                    self.cris.click(self.cris.p_sk13, aft=aft)
                elif a == 'B_1':
                    self.cris.click(self.cris.p_sk21, aft=aft)
                elif a == 'B_2':
                    self.cris.click(self.cris.p_sk22, aft=aft)
                elif a == 'B_3':
                    self.cris.click(self.cris.p_sk23, aft=aft)
                elif a == 'C_1':
                    self.cris.click(self.cris.p_sk31, aft=aft)
                elif a == 'C_2':
                    self.cris.click(self.cris.p_sk32, aft=aft)
                elif a == 'C_3':
                    self.cris.click(self.cris.p_sk33, aft=aft)
                elif a == 'E_1':
                    self.cris.click(self.cris.p_e1, aft=0.5)
                elif a == 'E_2':
                    self.cris.click(self.cris.p_e2, aft=0.5)
                elif a == 'E_3':
                    self.cris.click(self.cris.p_e3, aft=0.5)
                elif a == 'M_1':
                    self.cris.click(self.cris.p_msk, aft=0.5)
                    self.cris.click(self.cris.p_msk1, aft=aft)
                elif a == 'M_2':
                    self.cris.click(self.cris.p_msk, aft=0.5)
                    self.cris.click(self.cris.p_msk2, aft=aft)
                elif a == 'M_3':
                    self.cris.click(self.cris.p_msk, aft=0.5)
                    self.cris.click(self.cris.p_msk3, aft=aft)
                if order.count('_') == 2:
                    self.cris.click(self.cris.p_skt[int(order[-1])], aft=3)
                if order.count('_') == 3:
                    self.cris.click(self.cris.p_mskswitch[int(order[-3])], aft=0.5)
                    self.cris.click(self.cris.p_mskswitch[int(order[-1])], aft=5)

        def round_select(self, round, news):
            if news:
                self.select_skill(round)
            self.cris.click(self.cris.p_attack, aft=1.5)
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
                self.cris.click(i)

    class Cristina:

        def __init__(self):

            self.xpix = 1920
            self.ypix = 1080
            self.nxpix = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            self.nypix = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

            self.path_photo = self.search_path('Photos')
            self.path_script = self.search_path('Scripts')
            # self.path_editor = self.search_path('FateKE')

            # <editor-fold desc="Positions">
            self.p_entrance = [1660, 320]
            self.p_stone = [700, 300]
            self.p_goldapple = [700, 500]
            self.p_silverapple = [700, 700]
            self.p_appleconfirm = [1232, 820]
            self.p_support = [700, 445]
            self.p_startbattle = [1719, 975]

            self.p_e1 = [255, 420]
            self.p_e2 = [475, 103]
            self.p_e3 = [902, 103]

            self.p_sk11 = [170, 840]
            self.p_sk12 = [300, 840]
            self.p_sk13 = [430, 840]
            self.p_sk21 = [610, 840]
            self.p_sk22 = [740, 840]
            self.p_sk23 = [870, 840]
            self.p_sk31 = [1050, 840]
            self.p_sk32 = [1175, 840]
            self.p_sk33 = [1300, 840]

            self.p_msk = [1720, 470]
            self.p_msk1 = [1320, 475]
            self.p_msk2 = [1450, 475]
            self.p_msk3 = [1570, 475]

            self.p_carda = [650, 340]
            self.p_cardb = [960, 340]
            self.p_cardc = [1300, 340]

            self.p_rnumber1 = [1280, 75]
            self.p_rnumber2 = [1280, 86]
            self.p_attack = [1640, 860]

            self.p_empty = [152, 413]
            self.p_endconfirm = [1600, 980]

            self.p_close = [1893, 20]
            self.p_close_confirm = [1040, 557]

            self.p_mskswitch = [[], [270, 520], [540, 520], [820, 520], [1100, 520], [1370, 520], [1640, 520]]
            self.p_skt = [[], [520, 660], [960, 660], [1400, 660]]
            self.p_card = [[], [255, 745], [610, 745], [960, 745], [1310, 745], [1670, 745]]
            self.p_carddet = [257, 612, 966, 1324, 1683]
            self.p_carddety = 835

            # </editor-fold>

            if self.xpix != self.nxpix and self.ypix != self.nypix:
                self.auto_adjust()

            self.rbg_a = (120, 230, 245)
            self.rbg_b = (251, 241, 97)

            # <editor-fold desc="Bitmap">
            self.gapple = autopy.bitmap.Bitmap.open(self.path_photo + 'gApple.png')
            self.sapple = autopy.bitmap.Bitmap.open(self.path_photo + 'sApple.png')
            self.stone = autopy.bitmap.Bitmap.open(self.path_photo + 'stone.png')
            self.attack = autopy.bitmap.Bitmap.open(self.path_photo + 'Attack.png')
            self.end = autopy.bitmap.Bitmap.open(self.path_photo + 'end.png')
            # </editor-fold>

        def auto_adjust(self):

            self.p_entrance = self.__calculate(self.p_entrance)
            self.p_stone = self.__calculate(self.p_stone)
            self.p_goldapple = self.__calculate(self.p_goldapple)
            self.p_silverapple = self.__calculate(self.p_silverapple)
            self.p_appleconfirm = self.__calculate(self.p_appleconfirm)
            self.p_support = self.__calculate(self.p_support)
            self.p_startbattle = self.__calculate(self.p_startbattle)

            self.p_e1 = self.__calculate(self.p_e1)
            self.p_e2 = self.__calculate(self.p_e2)
            self.p_e3 = self.__calculate(self.p_e3)

            self.p_sk11 = self.__calculate(self.p_sk11)
            self.p_sk12 = self.__calculate(self.p_sk12)
            self.p_sk13 = self.__calculate(self.p_sk13)
            self.p_sk21 = self.__calculate(self.p_sk21)
            self.p_sk22 = self.__calculate(self.p_sk22)
            self.p_sk23 = self.__calculate(self.p_sk23)
            self.p_sk31 = self.__calculate(self.p_sk31)
            self.p_sk32 = self.__calculate(self.p_sk32)
            self.p_sk33 = self.__calculate(self.p_sk33)

            self.p_msk = self.__calculate(self.p_msk)
            self.p_msk1 = self.__calculate(self.p_msk1)
            self.p_msk2 = self.__calculate(self.p_msk2)
            self.p_msk3 = self.__calculate(self.p_msk3)

            self.p_carda = self.__calculate(self.p_carda)
            self.p_cardb = self.__calculate(self.p_cardb)
            self.p_cardc = self.__calculate(self.p_cardc)

            self.p_rnumber1 = self.__calculate(self.p_rnumber1)
            self.p_rnumber2 = self.__calculate(self.p_rnumber2)
            self.p_attack = self.__calculate(self.p_attack)

            self.p_empty = self.__calculate(self.p_empty)
            self.p_endconfirm = self.__calculate(self.p_endconfirm)

            self.p_close = self.__calculate(self.p_close)
            self.p_close_confirm = self.__calculate(self.p_close_confirm)

            self.p_mskswitch = [[],
                                self.__calculate(self.p_mskswitch[1]),
                                self.__calculate(self.p_mskswitch[2]),
                                self.__calculate(self.p_mskswitch[3]),
                                self.__calculate(self.p_mskswitch[4]),
                                self.__calculate(self.p_mskswitch[5]),
                                self.__calculate(self.p_mskswitch[6])]

            self.p_skt = [[],
                          self.__calculate(self.p_skt[1]),
                          self.__calculate(self.p_skt[2]),
                          self.__calculate(self.p_skt[3])]

            self.p_card = [[],
                           self.__calculate(self.p_card[1]),
                           self.__calculate(self.p_card[2]),
                           self.__calculate(self.p_card[3]),
                           self.__calculate(self.p_card[4]),
                           self.__calculate(self.p_card[5])]

            self.p_carddet = self.__calculate_list(self.p_carddet)
            self.p_carddety = self.__calculate_num(self.p_carddety)

        def __calculate(self, pos):
            return [self.nxpix * pos[0] // self.xpix, self.nypix * pos[1] // self.ypix]

        def __calculate_num(self, num):
            return self.nypix * num // self.ypix

        def __calculate_list(self, lis):
            tmp = []
            for i in lis:
                tmp.append(self.nxpix * i // self.xpix)
            return tmp

        @classmethod
        def search_path(cls, target):
            root = './'
            for i in range(4):
                lis = os.listdir(root)
                if target not in lis:
                    root = '.' + root
                else:
                    return root + target + '/'

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

    class FateKE(wx.Frame):

        def __init__(self, parent, Cristina):
            wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Fate~K Editor", pos=(300, 0),
                              size=wx.Size(900, 800), style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)
            base_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.back_ground = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
            base_sizer_b = wx.BoxSizer(wx.HORIZONTAL)

            cris = Cristina
            self.path_photo = cris.path_photo
            self.path_script = cris.path_script

            self.base_left = wx.BoxSizer(wx.VERTICAL)
            self.title_show = wx.BoxSizer(wx.VERTICAL)
            # <editor-fold desc="Title&Notes Label">
            self.label_title = wx.StaticText(self.back_ground, wx.ID_ANY, u"Title:", wx.DefaultPosition, wx.DefaultSize,
                                             0)
            self.label_title.SetFont(wx.Font(14, 72, 90, 92, False, "Lucida Fax"))
            self.label_title.Wrap(-1)
            self.title_show.Add(self.label_title, 0, wx.ALIGN_TOP | wx.ALL, 5)

            self.label_detail = wx.StaticText(self.back_ground, wx.ID_ANY, u"Note*:", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
            self.label_detail.SetFont(wx.Font(14, 72, 90, 92, False, "Lucida Fax"))
            self.label_detail.Wrap(-1)
            self.title_show.Add(self.label_detail, 0, wx.ALIGN_TOP | wx.ALL, 5)
            # </editor-fold>
            self.skill_show = self.Left(self)

            self.base_left.Add(self.title_show)
            self.base_left.Add(self.skill_show, 10, wx.EXPAND, 5)

            self.base_right = wx.BoxSizer(wx.VERTICAL)

            # <editor-fold desc="Skill Selection to Right">
            skill_selection = self.SkillSelect(self)
            self.base_right.Add(skill_selection, 3, wx.EXPAND, 5)
            # </editor-fold>

            # <editor-fold desc="Setting Module">
            right_setting = self.SettingBox(self)

            self.base_right.Add(right_setting, 1, 0, 5)
            # </editor-fold>

            base_sizer_b.Add(self.base_left, 3, wx.EXPAND, 5)
            base_sizer_b.Add(self.base_right, 1, wx.ALIGN_RIGHT | wx.EXPAND, 0)

            # <editor-fold desc="BASE B TO BASE BACKGROUND">
            self.back_ground.SetSizer(base_sizer_b)
            self.back_ground.Layout()
            base_sizer_b.Fit(self.back_ground)
            base_sizer.Add(self.back_ground, 1, wx.EXPAND | wx.ALL, 5)
            self.SetSizer(base_sizer)
            self.Layout()

            # </editor-fold>

        def set_title(self, strings):
            self.label_title.SetLabelText('Title:' + strings)

        def set_detail(self, strings):
            self.label_detail.SetLabelText('Note*:' + strings)

        def get_title(self):
            return self.label_title.GetLabel()[6:]

        def get_detail(self):
            return self.label_detail.GetLabel()[6:]

        # def on_close(self, e):
        #     # wx.Exit()
        #     # self.Destroy()
        #     self.Hide()

        class Left(wx.BoxSizer):

            def __init__(self, parent):
                wx.BoxSizer.__init__(self, wx.VERTICAL)
                self.focus = -1
                self.parent = parent
                self.round_list = []
                self.Add(wx.StaticText(self.parent.back_ground, label=''))

            def add_round(self):
                sizer_round = self.Round(self.parent, len(self.round_list))  # ~
                self.Add(sizer_round, 0, 0)
                sizer_round.set_focus(0)
                self.focus = len(self.round_list)
                self.round_list.append(sizer_round)
                self.Layout()
                for i in self.round_list:
                    i.Layout()
                self.parent.base_left.Layout()

            def remove_round(self):
                if len(self.round_list) > 0:
                    self.Hide(len(self.round_list))
                    self.Remove(len(self.round_list))
                    self.round_list = self.round_list[:-1]
                    self.focus = -1
                    for i in self.round_list:
                        i.leave_focus()
                    self.Layout()
                    for i in self.round_list:
                        i.Layout()
                    self.parent.base_left.Layout()

            class Round(wx.BoxSizer):

                def __init__(self, parent, identify):
                    wx.BoxSizer.__init__(self, wx.VERTICAL)
                    self.skill_focus = False
                    self.identify = identify
                    self.parent = parent
                    self.sizer_round_skill_line = wx.BoxSizer(wx.VERTICAL)  # Skill list display Module

                    # <editor-fold desc="Round & Skill Label">
                    self.label_round = wx.StaticText(parent.back_ground, wx.ID_ANY, "Round " + str(identify+1),
                                                     wx.DefaultPosition, wx.DefaultSize,
                                                     0)
                    self.label_round.Wrap(-1)
                    self.label_round.SetFont(wx.Font(9, 70, 93, 90, False, "Sitka Display"))
                    self.label_round.Bind(wx.EVT_MOUSE_EVENTS, self.set_focus)
                    self.Add(self.label_round, 0, wx.ALL, 5)

                    self.m_staticText16 = wx.StaticText(parent.back_ground, wx.ID_ANY, u"           Skill:", wx.DefaultPosition,
                                                        wx.DefaultSize, 0)
                    self.m_staticText16.Wrap(-1)
                    self.m_staticText16.SetFont(wx.Font(9, 70, 93, 90, False, "Sitka Display"))

                    self.sizer_round_skill_line.Add(self.m_staticText16, 0, wx.ALL, 5)
                    # </editor-fold>

                    # <editor-fold desc="skill line">
                    self.skill_list = []
                    # </editor-fold>

                    self.Add(self.sizer_round_skill_line, 0, 0)

                    self.sizer_round_order = self.Orders(parent)

                    self.Add(self.sizer_round_order, 0, 0)

                def add_skill(self, string):
                    sizer_skill_line_txt = self.SkillDisplay(self.parent, string, len(self.skill_list), self)
                    self.skill_list.append(sizer_skill_line_txt)
                    self.sizer_round_skill_line.Add(sizer_skill_line_txt, 0, 0)
                    self.Layout()
                    self.parent.skill_show.Layout()
                    self.parent.base_left.Layout()

                def insert_skill(self, string):
                    self.skill_list[-1].insert_string(string)
                    self.Layout()
                    self.parent.skill_show.Layout()
                    self.parent.base_left.Layout()

                def delete_skill(self, number):
                    self.sizer_round_skill_line.Hide(number + 1) #
                    self.sizer_round_skill_line.Remove(number + 1) #
                    try:
                        self.skill_list = self.skill_list[:number] + self.skill_list[number + 1:]
                    except IndexError:
                        self.skill_list = self.skill_list[:-1]
                    for index, i in enumerate(self.skill_list):
                        i.set_identify(index)
                    self.Layout()
                    self.parent.skill_show.Layout()
                    self.skill_focus = False

                def get_order(self):
                    orders = []
                    for i in self.sizer_round_order.combo_list:
                        orders.append(i.GetStringSelection())
                    return orders

                def set_focus(self, e):
                    self.parent.skill_show.focus = self.identify
                    self.label_round.SetFont(wx.Font(9, 70, 93, 90, True, "Sitka Display"))
                    for i in self.parent.skill_show.round_list:
                        if i.identify is not self.identify:
                            i.leave_focus()

                def leave_focus(self):
                    self.label_round.SetFont(wx.Font(9, 70, 93, 90, False, "Sitka Display"))

                class Orders(wx.BoxSizer):

                    def __init__(self, parent):
                        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
                        self.m_staticText13 = wx.StaticText(parent.back_ground, wx.ID_ANY, u"Orders:", wx.DefaultPosition,
                                                            wx.DefaultSize,
                                                            0)
                        self.m_staticText13.Wrap(-1)
                        self.m_staticText13.SetFont(wx.Font(9, 70, 93, 90, False, "Sitka Display"))

                        self.Add(self.m_staticText13, 0, wx.ALL, 5)

                        m_combo_choices = [u"B", u"A", u"Q", u"H1", u"H2", u"H3"]

                        self.combo_list = []

                        for i in range(6):
                            self.combo_list.append(wx.ComboBox(parent.back_ground, wx.ID_ANY, u"Combo!", wx.DefaultPosition,
                                                               wx.DefaultSize, m_combo_choices, 0))
                            self.combo_list[i].SetSelection(2)
                            self.Add(self.combo_list[i], 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
                        self.combo_list[0].SetSelection(4)
                        self.combo_list[1].SetSelection(0)
                        self.combo_list[2].SetSelection(1)

                class SkillDisplay(wx.BoxSizer):

                    def __init__(self, parent, strings, identify, rounds):
                        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
                        self.identify = identify
                        self.rounds = rounds
                        self.label_SPACE = wx.StaticText(parent.back_ground, wx.ID_ANY, u"                 ",
                                                         wx.DefaultPosition,
                                                         wx.DefaultSize, 0)
                        self.label_SPACE.Wrap(-1)
                        self.Add(self.label_SPACE, 0, wx.ALL, 5)
                        self.label_skill_info = wx.StaticText(parent.back_ground, wx.ID_ANY, strings, wx.DefaultPosition,
                                                              wx.DefaultSize,
                                                              0)
                        self.label_skill_info.Wrap(-1)
                        self.Add(self.label_skill_info, 0, wx.ALL, 5)

                        self.btn_delete = wx.Button(parent.back_ground, wx.ID_ANY, u"*", wx.Point(-1, -1), wx.DefaultSize, 0)
                        self.btn_delete.SetMaxSize(wx.Size(15, 15))
                        self.btn_delete.Bind(wx.EVT_BUTTON, self.on_click_delete)
                        self.Add(self.btn_delete, 0, wx.ALIGN_RIGHT, 5)

                    def get_skill_label(self):
                        return self.label_skill_info.GetLabel()

                    def insert_string(self, string):
                        strings = self.label_skill_info.GetLabel()
                        self.label_skill_info.SetLabel(strings + string)

                    def set_identify(self, i):
                        self.identify = i

                    def on_click_delete(self, e):
                        self.rounds.delete_skill(self.identify)

        class SkillSelect(wx.BoxSizer):

            def __init__(self, parent):
                wx.BoxSizer.__init__(self, wx.VERTICAL)

                sizer_per_1 = self.Person(parent, 1, parent.path_photo + 'back1.bmp')

                self.Add(sizer_per_1, 1, wx.EXPAND, 5)

                sizer_per_2 = self.Person(parent, 2, parent.path_photo + 'back2.bmp')

                self.Add(sizer_per_2, 1, wx.EXPAND, 5)

                sizer_per_3 = self.Person(parent, 3, parent.path_photo + 'back3.bmp')

                self.Add(sizer_per_3, 1, wx.EXPAND, 5)

                sizer_per_4 = self.Person(parent, 4, parent.path_photo + 'back4.bmp')

                self.Add(sizer_per_4, 1, wx.EXPAND, 5)

            class Person(wx.BoxSizer):

                def __init__(self, parent, identify, image):
                    # self = wx.BoxSizer(wx.HORIZONTAL)
                    wx.BoxSizer.__init__(self, wx.HORIZONTAL)
                    self.image = wx.Image(image, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
                    self.identify = identify
                    self.parent = parent
                    sizer_btn_group = wx.BoxSizer(wx.VERTICAL)

                    self.btn_per_1 = wx.Button(parent.back_ground, wx.ID_ANY, '<<', wx.DefaultPosition, wx.DefaultSize, 0)
                    self.btn_per_1.SetMaxSize(wx.Size(25, 25))
                    self.btn_per_1.Bind(wx.EVT_BUTTON, self.on_click)
                    sizer_btn_group.Add(self.btn_per_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.BOTTOM | wx.TOP, 2)

                    self.btn_per_2 = wx.Button(parent.back_ground, wx.ID_ANY, '<<', wx.DefaultPosition, wx.DefaultSize, 0)
                    self.btn_per_2.SetMaxSize(wx.Size(25, 25))
                    self.btn_per_2.Bind(wx.EVT_BUTTON, self.on_click)

                    sizer_btn_group.Add(self.btn_per_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.BOTTOM | wx.TOP, 2)

                    self.btn_per_3 = wx.Button(parent.back_ground, wx.ID_ANY, '<<', wx.DefaultPosition, wx.DefaultSize, 0)
                    self.btn_per_3.SetMaxSize(wx.Size(25, 25))
                    self.btn_per_3.Bind(wx.EVT_BUTTON, self.on_click)

                    sizer_btn_group.Add(self.btn_per_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.BOTTOM | wx.TOP, 2)

                    self.Add(sizer_btn_group, 1, wx.ALIGN_CENTER_VERTICAL, 5)

                    self.btn_per_to = wx.Button(parent.back_ground, wx.ID_ANY, u">>", wx.DefaultPosition, wx.DefaultSize, 0)
                    self.btn_per_to.SetMaxSize(wx.Size(25, 80))
                    self.btn_per_to.Bind(wx.EVT_BUTTON, self.on_click)

                    self.Add(self.btn_per_to, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)

                    self.bitmap_btn = wx.BitmapButton(parent.back_ground, -1, self.image)
                    # self.panel_image = wx.Panel(parent.back_ground, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                    #                             wx.TAB_TRAVERSAL)
                    self.bitmap_btn.SetMinSize(wx.Size(80, 80))
                    self.bitmap_btn.SetMaxSize(wx.Size(80, 80))
                    self.bitmap_btn.Bind(wx.EVT_BUTTON, self.on_click_bitmap)
                    # self.panel_image.SetMinSize(wx.Size(80, 80))
                    # self.panel_image.SetMaxSize(wx.Size(80, 80))
                    # self.panel_image.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase)
                    self.Add(self.bitmap_btn, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 7)

                def on_click_bitmap(self, event):
                    if self.parent.skill_show.focus >= 0:
                        self.parent.skill_show.round_list[self.parent.skill_show.focus].skill_focus = False

                def on_click(self, e):
                    event = e.GetEventObject()
                    ch = ['', 'A', 'B', 'C', 'M'][self.identify]
                    if event is self.btn_per_1:
                        ch += '_1'
                    elif event is self.btn_per_2:
                        ch += '_2'
                    elif event is self.btn_per_3:
                        ch += '_3'
                    else:
                        ch = '_' + str(self.identify)
                    if self.parent.skill_show.focus >= 0:
                        if self.parent.skill_show.round_list[self.parent.skill_show.focus].skill_focus:
                            self.parent.skill_show.round_list[self.parent.skill_show.focus].insert_skill(ch)
                        else:
                            self.parent.skill_show.round_list[self.parent.skill_show.focus].add_skill(ch)
                            self.parent.skill_show.round_list[self.parent.skill_show.focus].skill_focus = True

        class SettingBox(wx.GridSizer):

            def __init__(self, parent):
                wx.GridSizer.__init__(self, 2, 2, 0, 0)
                self.parent = parent
                self.btn_setting = wx.Button(parent.back_ground, wx.ID_ANY, u"Setting", wx.DefaultPosition, wx.DefaultSize, 0)
                self.Add(self.btn_setting, 0, wx.ALIGN_CENTER | wx.ALL, 5)
                self.btn_setting.Bind(wx.EVT_BUTTON, self.on_click)

                self.btn_new_round = wx.Button(parent.back_ground, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0)
                self.Add(self.btn_new_round, 0, wx.ALIGN_CENTER, 5)
                self.btn_new_round.Bind(wx.EVT_BUTTON, self.on_click)

                self.btn_remove = wx.Button(parent.back_ground, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0)
                self.Add(self.btn_remove, 0, wx.ALIGN_CENTER | wx.ALL, 5)
                self.btn_remove.Bind(wx.EVT_BUTTON, self.on_click)

                self.btn_generate = wx.Button(parent.back_ground, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0)
                self.Add(self.btn_generate, 0, wx.ALIGN_CENTER | wx.ALL, 5)
                self.btn_generate.Bind(wx.EVT_BUTTON, self.on_click_generate)

            def on_click(self, event):
                evt = event.GetEventObject()
                if evt is self.btn_setting:
                    setting_dialog = self.SettingDialog(self.parent)
                    setting_dialog.Show()

                elif evt is self.btn_new_round:
                    self.parent.skill_show.add_round()

                elif evt is self.btn_remove:
                    self.parent.skill_show.remove_round()
                    pass
                else:
                    pass

            def on_click_generate(self, event):
                parent = self.parent
                rounds = parent.skill_show.round_list
                head = '<TITLE>' + parent.get_title() + '</TITLE>\n' + '<DETAIL>' + parent.get_detail() + '</DETAIL>\n'
                bodys = ''
                for r in rounds:
                    tmp_string = ''
                    for skill in r.skill_list:
                        tmp_string += '<skill>' + skill.get_skill_label() + '</skill>\n'
                    for order in r.get_order():
                        tmp_string += '<order>' + order + '</order>\n'
                    bodys += '<round>\n' + tmp_string + '</round>\n'
                bodys = '<body>\n' + bodys + '</body>\n'
                with open(self.parent.path_script + parent.get_title() + '.txt', 'w+') as file:
                    file.write(head + bodys)

            class SettingDialog(wx.Dialog):

                def __init__(self, parent):
                    wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Scathach", pos=wx.DefaultPosition, size=wx.DefaultSize,
                                       style=wx.DEFAULT_DIALOG_STYLE)
                    self.parent = parent

                    bSizer14 = wx.BoxSizer(wx.VERTICAL)

                    sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

                    self.label_title = wx.StaticText(self, wx.ID_ANY, u"Title:   ", wx.DefaultPosition, wx.DefaultSize, 0)
                    self.label_title.Wrap(-1)
                    sizer_1.Add(self.label_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

                    self.text_title = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(140, -1), 0)
                    sizer_1.Add(self.text_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

                    bSizer14.Add(sizer_1, 1, wx.EXPAND, 5)

                    sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

                    self.label_detail = wx.StaticText(self, wx.ID_ANY, u"Detail:", wx.DefaultPosition, wx.DefaultSize, 0)
                    self.label_detail.Wrap(-1)
                    sizer_2.Add(self.label_detail, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

                    self.text_detail = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(140, -1), 0)
                    sizer_2.Add(self.text_detail, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

                    bSizer14.Add(sizer_2, 1, wx.EXPAND, 5)

                    bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

                    self.btn_confirm = wx.Button(self, label=u"Confirm")
                    self.btn_confirm.SetDefault()
                    self.btn_confirm.SetHelpText(u"Click to Confirm")
                    self.btn_confirm.Bind(wx.EVT_BUTTON, self.on_click)
                    bSizer20.Add(self.btn_confirm, 0, wx.ALL, 5)

                    self.btn_cancel = wx.Button(self, label=u"Cancel")
                    self.btn_cancel.SetHelpText(u"Click to Confirm")
                    self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_click)

                    bSizer20.Add(self.btn_cancel, 0, wx.ALL, 5)

                    bSizer14.Add(bSizer20, 1, wx.EXPAND, 5)

                    self.text_title.SetLabelText(parent.label_title.GetLabel()[6:])
                    self.text_detail.SetLabelText(parent.label_detail.GetLabel()[6:])
                    self.SetSizer(bSizer14)
                    self.Layout()
                    bSizer14.Fit(self)

                    self.Centre(wx.BOTH)

                def on_click(self, event):
                    if event.GetEventObject() is self.btn_confirm:
                        self.parent.set_title(self.text_title.GetValue())
                        self.parent.set_detail(self.text_detail.GetValue())
                    self.Close()

                def __del__(self):
                    pass


if __name__ == '__main__':

    app = wx.App(False)
    frame = FateK(None, app)
    frame.Show()
    app.MainLoop()
