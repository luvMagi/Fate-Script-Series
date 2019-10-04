import wx
import wx.xrc
import os
from bs4 import BeautifulSoup


class FateKE(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Fate~K Editor", pos=wx.DefaultPosition,
                          size=wx.Size(900, 800), style=wx.DEFAULT_FRAME_STYLE | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)
        base_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.back_ground = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        base_sizer_b = wx.BoxSizer(wx.HORIZONTAL)

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

        self.Centre(wx.BOTH)
        # </editor-fold>

    def set_title(self, strings):
        self.label_title.SetLabelText('Title:' + strings)

    def set_detail(self, strings):
        self.label_detail.SetLabelText('Note*:' + strings)

    def get_title(self):
        return self.label_title.GetLabel()[6:]

    def get_detail(self):
        return self.label_detail.GetLabel()[6:]

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

            sizer_per_1 = self.Person(parent, 1, path_photos + 'back1.bmp')

            self.Add(sizer_per_1, 1, wx.EXPAND, 5)

            sizer_per_2 = self.Person(parent, 2, path_photos + 'back2.bmp')

            self.Add(sizer_per_2, 1, wx.EXPAND, 5)

            sizer_per_3 = self.Person(parent, 3, path_photos + 'back3.bmp')

            self.Add(sizer_per_3, 1, wx.EXPAND, 5)

            sizer_per_4 = self.Person(parent, 4, path_photos + 'back4.bmp')

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
            with open(path_scripts + parent.get_title() + '.txt', 'w+') as file:
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


def search_path(target):
    root = './'
    for i in range(3):
        lis = os.listdir(root)
        if target not in lis:
            root = '.' + root
        else:
            return root


if __name__ == '__main__':
    path_photos = search_path('Photos') + 'Photos/'
    path_scripts = search_path('Scripts') + 'Scripts/'
    app = wx.App(False)
    frame = FateKE(None)
    frame.Show()
    app.MainLoop()
