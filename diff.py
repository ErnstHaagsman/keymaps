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
               self.key == other.key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.ctrl, self.alt, self.shift, self.key))

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


if __name__ == '__main__':
    # Define PyCharm set
    pycharm_hotkeys = set()
    webstorm_hotkeys = set()

    ## Parse the keymaps

    # The keymaps both start with an 'editing' section
    section = 'Editing'
    with open('pycharm-current.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            # If we're at a section header, only the first element of the array will have contents
            # So let's assume that if the second element is empty, it's a section header
            if len(item[1]) == 0:
                section = item[0]
                continue

            # Define the key to add
            to_add = Hotkey()

            # Split the hotkey's elements
            keys = [key.lower() for key in item[0].split(" + ")]

            # Modifiers
            if 'ctrl' in keys:
                to_add.ctrl = True
            if 'alt' in keys:
                to_add.alt = True
            if 'shift' in keys:
                to_add.shift = True

            # Now the only key that remains is the last key (hopefully)
            to_add.key = keys[-1]

            to_add.action = item[1]

            pycharm_hotkeys.add(to_add)
