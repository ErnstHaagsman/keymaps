import csv


class Hotkey:
    def __init__(self, ctrl = False, alt = False, shift = False, key = False, action = '', section = ''):
        self.ctrl = ctrl
        self.alt = alt
        self.shift = shift
        self.key = key
        self.action = action
        self.section = section

    def __eq__(self, other):
        if not isinstance(other, Hotkey):
            return False

        return self.ctrl == other.ctrl and \
               self.alt == other.alt and \
               self.shift == other.shift and \
               self.key.lower() == other.key.lower()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.ctrl, self.alt, self.shift, self.key.lower()))

    def __repr__(self):
        key_parts = []
        if self.ctrl:
            key_parts.append('Ctrl')
        if self.alt:
            key_parts.append('Alt')
        if self.shift:
            key_parts.append('Shift')
        key_parts.append(self.key.capitalize())
        return "<{}> {}".format(" + ".join(key_parts), self.action)


def main():
    # Read the hotkeys from the CSV files
    pycharm_hotkeys = parse_csv('pycharm-current.csv', ' + ')
    webstorm_hotkeys = parse_csv('webstorm-current.csv', '-')

    print('PyCharm: {} keys found'.format(len(pycharm_hotkeys)))
    print('WebStorm: {} keys found'.format(len(webstorm_hotkeys)))

    print ('WebStorm, but not PyCharm')
    webstorm = webstorm_hotkeys.difference(pycharm_hotkeys)
    for key in webstorm:
        print("{}: {}".format(key.section, key))

    print('PyCharm, but not WebStorm')
    difference = pycharm_hotkeys.difference(webstorm_hotkeys)
    for key in difference:
        print("{}: {}".format(key.section, key))


def parse_csv(csv_file_name, sep):
    # The keymaps both start with an 'editing' section
    section = 'Editing'
    current_set = set()
    with open(csv_file_name, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            # If we're at a section header, only the first element of the array will have contents
            # So let's assume that if the second element is empty, it's a section header
            if len(item[1]) == 0:
                section = item[0]
                continue

            to_add = parse_hotkey(item[0], item[1], section, sep)

            current_set.update(to_add)

    return current_set


modifiers = {'ctrl', 'alt', 'shift'}

def parse_hotkey(keystroke, action, section, sep):
    # Closure to parse the keystroke
    def get_key(keystroke, to_add):
        to_add.section = section

        # Split the hotkey's elements
        keys = [key.strip().lower() for key in keystroke.split(sep)]
        # Modifiers
        if 'ctrl' in keys:
            to_add.ctrl = True
        if 'alt' in keys:
            to_add.alt = True
        if 'shift' in keys:
            to_add.shift = True

        # Now the only key that remains is the last key (hopefully)
        key = keys[-1]

        # Special case for WebStorm keymap
        if len(keys) > 1 and keys[-2].lower() == 'numpad' and sep == '-':
            key = 'Numpad-'

        to_add.key = key


    # Define the key to add
    hotkeys = []
    keystrokes = []

    comma_index = keystroke.find(',')
    slash_index = keystroke.find('/')
    if comma_index > -1:
        # With a comma, we have alternate keystrokes for the same action
        keystrokes = keystroke.split(',')
    elif slash_index > -1 and slash_index != len(keystroke) - 1:
        # If we have a slash in the middle of a keystroke, we have multiple keystrokes on a single line
        # This is harder, we have to find out if there's a modifier right of the slash
        # If there is, we need to split on the slash, if there isn't we need to duplicate the modifiers
        parts = [part.strip() for part in keystroke.split('/')]
        if not any([part.lower() in modifiers for part in parts[1].split(sep)]):
            # duplicate modifiers
            for part in parts[0].split(sep):
                if part.lower() in modifiers:
                    parts[1] = part + sep + parts[1]

        keystrokes = parts
    else:
        keystrokes = [keystroke]

    for stroke in keystrokes:
        to_add = Hotkey()
        get_key(stroke, to_add)
        to_add.action = action

        hotkeys.append(to_add)

    return hotkeys


if __name__ == '__main__':
    main()
