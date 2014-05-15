import sublime
import sublime_plugin
import subprocess

COMMAND = '/usr/local/bin/igor'


class PostSave(sublime_plugin.EventListener):

    def on_post_save(self, view):
        if not 'python' in view.settings().get('syntax').lower():
            return

        filename = view.file_name()
        igor_cmd = '%s --reap "%s"' % (COMMAND, filename,)
        out = subprocess.Popen(igor_cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        #sublime.message_dialog("mr.igor could not be found in '%s'." % COMMAND)
        if out[1]:
            sublime.error_message(out[1].decode('utf-8'))
        else:
            sublime.status_message("mr.igor reaped file '%s'" % filename)


class IgorReplaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if not 'python' in self.view.settings().get('syntax').lower():
            return

        filename = self.view.file_name()
        igor_cmd = '%s --print "%s"' % (COMMAND, filename,)

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
