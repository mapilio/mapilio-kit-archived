from simple_term_menu import TerminalMenu
import logging

LOG = logging.getLogger(__name__)

LOG.warning(f"Select Image Quality ")


def main():
    options = ["480", "720", "1080"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    return int(options[menu_entry_index])


QUALITY = main()
