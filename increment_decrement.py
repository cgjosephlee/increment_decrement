import sublime
import sublime_plugin
import re

class IncrementDecrementCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return len(self.view.sel()) > 0

    def run(self, edit, plus):
        selection = self.view.sel()
        for region in selection:
            try:
                region, value, guess_type = self.select_region(region)
                selection.add(region)
                self.view.replace(edit, region, self.op(value, guess_type, plus))
                # print(value, str(self.op(value, guess_type)), guess_type)
            except ValueError:
                pass

    def select_region(self, region):
        # Try to operate on around the cursor if nothing is selected
        if region.empty():
            begin = end = region.begin()
            guess_type = 'int'
            if self.view.substr(begin - 1).isdigit() or self.view.substr(begin - 1) == '.':
                while begin >= 0:
                    if not self.view.substr(begin - 1).isdigit():
                        # integer
                        if self.view.substr(begin - 1) == '-':
                            # guess_type = 'int'
                            begin -= 1
                            break
                        # binary
                        elif self.view.substr(begin - 1) == 'b':
                            begin -= 2
                            guess_type = 'bin'
                            break
                        # hexadecimal
                        elif self.view.substr(begin - 1) == 'x':
                            begin -= 2
                            guess_type = 'hex'
                            break
                        # decimal
                        elif self.view.substr(begin - 1) == '.':
                            if guess_type == 'dec':  # meet second time, maybe version or IP?
                                break
                            guess_type = 'dec'
                            begin -= 1
                            continue
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
                # boolean
                if self.view.substr(region) in self._boolean_matches():
                    guess_type = 'bool'
                # binary
                elif re.match(r'0b[01]', self.view.substr(region)):
                    guess_type = 'bin'
                # hexadecimal
                elif re.match(r'0x[0-9a-fA-F]', self.view.substr(region)):
                    guess_type = 'hex'
                # roman numeral
                elif re.match(r'([IVXLC]+|[ivxlc]+)$', self.view.substr(region)):
                    guess_type = 'roman'
                else:
                    raise ValueError
            value = self.view.substr(region)
        # User selected region
        else:
            value = self.view.substr(region)
            if value in self._boolean_matches():
                guess_type = 'bool'
            elif re.match(r'([IVXLC]+|[ivxlc]+)$', self.view.substr(region)):
                guess_type = 'roman'
            elif re.match(r'[-]?\d+$', value):
                guess_type = 'int'
            elif re.match(r'[-]?(\d+\.\d+|\.\d+|\d+\.)$', value):
                guess_type = 'dec'
            elif re.match(r'0b[01]', self.view.substr(region)):
                guess_type = 'bin'
            elif re.match(r'0x[0-9a-fA-F]', self.view.substr(region)):
                guess_type = 'hex'
            else:
                raise ValueError
        return region, value, guess_type

    def op(self, value, guess_type, plus):
        if guess_type == 'int':
            value = self.integer(value, plus)
        elif guess_type == 'dec':
            value = self.decimal(value, plus)
        elif guess_type == 'bool':
            value = self.boolean(value)
        elif guess_type == 'roman':
            value = self.roman(value, plus)
        elif guess_type == 'bin':
            value = self.binary(value, plus)
        elif guess_type == 'hex':
            value = self.hexadecimal(value, plus)
        return str(value)

    def integer(self, value, plus):
        digits = None
        if value.startswith('0'):
            digits = len(value)
        value = int(value)
        if plus:
            value += 1
        else:
            value -= 1
        if digits and value >= 0:
            value = str(value).zfill(digits)
        return value

    def decimal(self, value, plus):
        int_part = len(value.split('.')[0])
        dec_part = len(value.split('.')[1])
        # maybe bullet points
        if dec_part == 0:
            value = value.rstrip('.')
            value = self.integer(value, plus)
            value = str(value) + '.'
        else:
            if plus:
                value = '{:.{dec}f}'.format(float(value) + (10 ** -dec_part), dec=dec_part)
            else:
                value = '{:.{dec}f}'.format(float(value) - (10 ** -dec_part), dec=dec_part)
            # .3, valid decimals in programming language
            if int_part == 0:
                value = value.lstrip('0')
        return value

    def _boolean_avail_values(self):
        # upper case only, case is handled automatically
        # two converse values in an item
        return [['TRUE', 'FALSE'], ['YES', 'NO']]

    def _boolean_matches(self):
        flatten = []
        for i in self._boolean_avail_values():
            for j in i:
                flatten.extend((j.upper(), j.lower(), j.capitalize()))
        return flatten

    def _boolean_dict(self):
        convert_dict = {}
        for i in self._boolean_avail_values():
            convert_dict[i[0].upper()] = i[1].upper()
            convert_dict[i[0].lower()] = i[1].lower()
            convert_dict[i[0].capitalize()] = i[1].capitalize()
            convert_dict[i[1].upper()] = i[0].upper()
            convert_dict[i[1].lower()] = i[0].lower()
            convert_dict[i[1].capitalize()] = i[0].capitalize()
        return convert_dict

    def boolean(self, value):
        # ValueError is raised if key is not valid
        return self._boolean_dict()[value]

    def roman(self, RomanNum, plus):
        decimalDens = [100, 90, 50, 40, 10, 9, 5, 4, 1]
        romanDens = ["C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        case_is = 'upper'
        if RomanNum.islower():
            case_is = 'lower'
            RomanNum = RomanNum.upper()
        # convert to decimal
        decimalSum = 0
        currentLen = 0
        while currentLen < len(RomanNum):
            for R in romanDens:
                if re.match(R, RomanNum[currentLen:]):
                    currentLen += len(R)
                    decimalSum += decimalDens[romanDens.index(R)]
        # currently not support > 100
        if decimalSum > 100:
            raise ValueError
        # plus or minus
        if plus and decimalSum < 100:
                decimalSum += 1
        elif not plus and decimalSum > 1:
                decimalSum -= 1
        else:
            raise ValueError
        # convert to roman
        NewRomanNum = ''
        while decimalSum > 0:
            for N in decimalDens:
                if decimalSum >= N:
                    decimalSum -= N
                    NewRomanNum += romanDens[decimalDens.index(N)]
                    break
        if case_is == 'lower':
            NewRomanNum = NewRomanNum.lower()
        return NewRomanNum

    def binary(self, val, plus):
        val = int(val, 2)
        if plus:
            val += 1
        else:
            if val != 0:
                val -= 1
        return str(bin(val))

    def hexadecimal(self, val, plus):
        val = int(val, 16)
        if plus:
            val += 1
        else:
            if val != 0:
                val -= 1
        return str(hex(val))
