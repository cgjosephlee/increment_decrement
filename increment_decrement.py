import sublime
import sublime_plugin

class NumberCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            try:
                # Try to operate on around the cursor if nothing is selected
                if region.empty():
                    begin = end = region.begin()
                    guess_type = 'int'
                    if self.view.substr(begin - 1).isdigit():
                        while begin >= 0:
                            if not self.view.substr(begin - 1).isdigit():
                                # integer
                                if self.view.substr(begin - 1) == '-':
                                    # guess_type = 'int'
                                    begin -= 1
                                    break
                                # decimal
                                elif self.view.substr(begin - 1) == '.':
                                    if guess_type == 'dec':  # meet second time, maybe version or IP?
                                        break
                                    guess_type = 'dec'
                                    begin -= 1
                                    continue
                                # hexadecimal, not implemented
                                # elif self.view.substr(begin - 1) == 'x':
                                #     guess_type = 'hex'
                                #     pass
                                break
                            begin -= 1
                        while end < self.view.size():
                            if not self.view.substr(end).isdigit():
                                if self.view.substr(end) == '.':
                                    if guess_type == 'int':
                                        end += 1
                                        guess_type = 'dec'
                                        continue
                                    elif guess_type == 'dec':
                                        break
                                break
                            end += 1
                        region = sublime.Region(begin, end)
                    elif self.view.substr(begin - 1).isalpha():
                        region = self.view.word(region)
                        if self.view.substr(region) in ['TRUE', 'True', 'true', 'FALSE', 'False', 'false']:
                            guess_type = 'bool'
                        else:
                            raise ValueError
                    value = self.view.substr(region)
                else:
                    import re
                    value = self.view.substr(region)
                    if value in ['TRUE', 'True', 'true', 'FALSE', 'False', 'false']:
                        guess_type = 'bool'
                    elif re.match(r'[-]?\d+$', value):
                        guess_type = 'int'
                    elif re.match(r'\d+\.\d+$', value):
                        guess_type = 'dec'
                    else:
                        raise ValueError
                self.view.replace(edit, region, str(self.op(value, guess_type)))
                # print(value, str(self.op(value, guess_type)), guess_type)
            except ValueError:
                pass

    def is_enabled(self):
        return len(self.view.sel()) > 0

class IncrementCommand(NumberCommand):
    def op(self, value, guess_type):
        if guess_type == 'int':
            value = int(value)
            value += 1
        elif guess_type == 'dec':
            dec_part = len(value.split('.')[-1])
            value = '{:.{dec}f}'.format(float(value) + (10 ** -dec_part), dec=dec_part)
        elif guess_type == 'bool':
            convert_bool = {'TRUE': 'FALSE', 'True': 'False', 'true': 'false',
                            'FALSE': 'TRUE', 'False': 'True', 'false': 'true'}
            value = convert_bool[value]
        return value

class DecrementCommand(NumberCommand):
    def op(self, value, guess_type):
        if guess_type == 'int':
            value = int(value)
            value -= 1
        elif guess_type == 'dec':
            dec_part = len(value.split('.')[-1])
            value = '{:.{dec}f}'.format(float(value) - (10 ** -dec_part), dec=dec_part)
        elif guess_type == 'bool':
            convert_bool = {'TRUE': 'FALSE', 'True': 'False', 'true': 'false',
                            'FALSE': 'TRUE', 'False': 'True', 'false': 'true'}
            value = convert_bool[value]
        return value
