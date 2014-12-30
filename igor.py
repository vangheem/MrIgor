import sublime
import sublime_plugin
import subprocess


class IgorSaveCommand(sublime_plugin.EventListener):

    def on_post_save(self, view):
        if not 'python' in view.settings().get('syntax').lower():
            return

        plugin_settings = sublime.load_settings('MrIgor.sublime-settings')
        mrigor_bin = view.settings().get(
            'mrigor_path',
            plugin_settings.get('mrigor_path', '/usr/local/bin/mrigor')
        )

        filename = view.file_name()
        igor_cmd = '%s --reap "%s"' % (mrigor_bin, filename,)
        out = subprocess.Popen(igor_cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        if out[1]:
            if 'could not compile' in out[1]:
                sublime.status_message("mr.igor could not compile '%s'" % filename)
            else:
                sublime.error_message(
                    "mr.igor could not be found. " +
                    "Please make sure you have installed mr.igor properly and " +
                    "the mrigor_bin setting points to the correct path. " +
                    "Error message was: '%s'" % out[1].decode('utf-8')
                )
        else:
            sublime.status_message("mr.igor reaped file '%s'" % filename)


class IgorReplaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if not 'python' in self.view.settings().get('syntax').lower():
            return

        plugin_settings = sublime.load_settings('MrIgor.sublime-settings')
        mrigor_bin = self.view.settings().get(
            'mrigor_path',
            plugin_settings.get('mrigor_path', '/usr/local/bin/mrigor')
        )

        filename = self.view.file_name()
        igor_cmd = '%s --print "%s"' % (mrigor_bin, filename,)

        self.view.run_command('save')

        out = subprocess.Popen(igor_cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()

        if out[1]:
            sublime.error_message(out[1].decode('utf-8'))
        else:
            if out[0]:
                out = out[0].decode("utf-8")
                out = out.replace('%s:' % filename, '')
                replacement = out.strip()

                region = sublime.Region(0, self.view.size())
                self.view.replace(edit, region, replacement)
                sublime.status_message("Igor Updated")
