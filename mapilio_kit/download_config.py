import os

if not os.name == 'nt':
    from simple_term_menu import TerminalMenu

import logging

LOG = logging.getLogger(__name__)


def select_quality():
    """

    Returns: image quality

    """
    LOG.info(f"Select Image Quality ")
    options = ["1080", "480", "240"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    return options[menu_entry_index]