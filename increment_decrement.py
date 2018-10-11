import sublime
import sublime_plugin

class NumberCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            try:
                # Try to operate on around the cursor if nothing is selected
                if region.empty():
                    begin = region.begin()
                    while begin >= 0:
                        if not self.view.substr(begin - 1).isdigit():
                            if self.view.substr(begin - 1) == '-':
                                begin -= 1
                            break
                        begin -= 1
                    end = region.end()
                    while end < self.view.size():
                        if not self.view.substr(end).isdigit():
                            break
                        end += 1
                    region = sublime.Region(begin, end)
                value = int(self.view.substr(region))
                self.view.replace(edit, region, str(self.op(value)))
            except ValueError:
                pass

    def is_enabled(self):
        return len(self.view.sel()) > 0

class IncrementCommand(NumberCommand):
    def op(self, value):
        return value + 1

class DecrementCommand(NumberCommand):
    def op(self, value):
        return value - 1
