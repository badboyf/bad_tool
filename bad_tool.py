import sublime
import sublime_plugin
import json
import time,datetime

panel_name = 'bad_tool_panel'

class FzkBaseCommand(object):
    # 写入panal
    # eg: self.panel_log(["Writing... {} 1\n", "Writing...。 {} 2\n"])
    def panel_log(self, txts):
        if self._edit == None:
            return
        # 显示panel
        pt = self._panel
        self.view.window().run_command("show_panel", {"panel": "output." + panel_name})
        pt.set_read_only(False)
        if isinstance(txts, list):
            for x in txts:
                pt.insert(self._edit, pt.size(), x)
        else:
            pt.insert(self._edit, pt.size(), str(txts))
        pt.set_read_only(True)

    # 初始化 edit panel  find_output_panel/get_output_panel
    # find_output_panel 每次都是同一个，保留以前日志
    # get_output_panel  每次新创建一个，无法保留以前日志
    def init_base(self, edit):
        self._edit = edit
        self._panel = self.view.window().find_output_panel(panel_name)
        if self._panel == None:
            self._panel = self.view.window().get_output_panel(panel_name)
        self._settings = sublime.load_settings("bad_tool.sublime-settings")

    # 写入文件
    def write_file(self, filename: '', content: ''):
        try:
            # self.view.window().status_message('正在写入文件:'.format(filename))
            with open(filename, 'wb') as f:
                f.write(content.encode('utf-8'))
            # self.view.window().status_message('写入文件成功:'.format(filename))
        except Exception as e:
            self.panel_log(e)
            raise e

class runjsCommand(FzkBaseCommand, sublime_plugin.TextCommand):
    def run(self, edit):
        self.init_base(edit)
        self.doRun(edit)

    def doRun(self, edit):
        # 获取配置
        filename = self._settings.get('run_js_tmp_file_path')
        log_tmp_file_path = self._settings.get('log_tmp_file_path')

        regions = self.view.sel()
        for region in regions:
            # 获取选中区域
            region, _ = get_selection_from_region(region=region, regions_length=len(region), view=self.view)
            if region is None:
                continue
            # 获取文本
            selection_text = self.view.substr(region)
            # 写入临时文件
            self.write_file(filename=filename, content=selection_text)

        self.view.window().run_command("build", {})

        # 是否打印临时文件地址 到 output.exec
        if log_tmp_file_path:
            pt = self.view.window().find_output_panel("exec")
            pt.insert(self._edit, 0, '[write to tmplate file {}]\n'.format(filename))

# 清空panel
class clear_panelCommand(FzkBaseCommand, sublime_plugin.TextCommand):
    def run(self, edit):
        self._panel = self.view.window().get_output_panel(panel_name)
        self.view.window().status_message('clear panel success')

# 时间转换
class timeformatCommand(FzkBaseCommand, sublime_plugin.TextCommand):
    def run(self, edit):
        self.init_base(edit)
        self.doRun(edit)

    def doRun(self, edit):
        regions = self.view.sel()
        for region in regions:
            # 获取选中区域
            region, is_entire = get_selection_from_region(region=region, regions_length=len(region), view=self.view)
            if region is None:
                continue
            # 获取文本
            selection_text = self.view.substr(region)
        try:
            # 仅支持处理 2023-01-04 08:46:00  2023-01-04 1672793160937  1672793160
            if len(selection_text) == 10 and '-' in selection_text:  # 2023-01-04
                time_int = int(time.mktime(time.strptime(selection_text,'%Y-%m-%d'))) * 100
                self.panel_log('{}          {}\n'.format(selection_text, time_int))
            elif len(selection_text) == 19 and '-' in selection_text and ':' in selection_text: # 2023-01-04 08:46:00
                time_int = int(time.mktime(time.strptime(selection_text,'%Y-%m-%d %H:%M:%S'))) * 100
                self.panel_log('{} {}\n'.format(selection_text, time_int))
            elif len(selection_text) == 10 and selection_text.isdigit(): # 1672793160
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(selection_text)))
                self.panel_log('{}          {}\n'.format(selection_text, time_str))
            elif len(selection_text) == 13 and selection_text.isdigit(): # 1672793160937
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(selection_text)/1000))
                self.panel_log('{}       {}\n'.format(selection_text, time_str))
            else:
                if is_entire:
                    self.panel_log('not support\n')
                else:
                    self.panel_log('not support: {}\n'.format(selection_text))
        except Exception as e:
            self.panel_log(e)

# 获取选中的区域，((0, 100), false)，没有选中取全部文件
def get_selection_from_region(region: sublime.Region, regions_length: int, view: sublime.View):
    entire_file = False
    if region.empty() and regions_length > 1:
        return None, None
    elif region.empty():
        region = sublime.Region(0, view.size())
        entire_file = True

    return region, entire_file



