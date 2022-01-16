import logging
import os
import re
import sys
from typing import Any, Dict

import PySimpleGUI as sg  # type: ignore
from PySimpleGUI.PySimpleGUI import Column  # type: ignore

from .utils.encryption import encrypt_password, generate_key

logger = logging.getLogger(__name__)


def login_gui() -> Dict[str, Any]:
    sg.theme('DarkTeal12')

    def collapse(layout: list, key: str, visible: bool) -> Column:
        """
        Helper function to hide and un-hide layouts
        """

        return sg.pin(sg.Column(layout, key=key, visible=visible))

    def main() -> Dict[str, Any]:
        """
        Main GUI function
        """
        new_user_section = [
            [sg.Text('Username'), sg.Input(key='_USERNAME_', tooltip='What is your myASNB account username?')],
            [sg.Text('Password'), sg.Input(key='_PASSWORD_', password_char="*", tooltip='What is your myASNB account password?')],
            [sg.Text('Investment Amount (RM)'), sg.Input(key='_INVESTMENT_AMOUNT_', tooltip='How much do you want to invest?', change_submits=True, do_not_clear=True)],
        ]

        layout = [
            [sg.Text('myASNB Unit Holder Login', font='Helvetica 20', justification='center')],
            [sg.Checkbox('Login as new user', enable_events=True, key='_CHECKBOX_KEY_', tooltip='Tick to login.')],
            [collapse(new_user_section, '_SECTION_KEY_', False)],
            [sg.OK('Start', tooltip='Start the bot (Press: ENTER)', size=(10, 1), bind_return_key=True, focus=True), sg.Cancel('Quit', tooltip='Goodbye.', size=(5, 1))],
        ]

        window = sg.Window(
            'Six Percent',
            layout,
            auto_size_text=False,
            default_element_size=(25, 1),
            text_justification='l',
            return_keyboard_events=True,
            grab_anywhere=False,
        )

        user_credentials_template = dict(username='', password='', investment_amount='')
        user_credentials = user_credentials_template.copy()
        section_toggle = False

        while True:
            event, values = window.read()

            if event == '_CHECKBOX_KEY_':
                section_toggle = not section_toggle
                window['_SECTION_KEY_'].update(visible=section_toggle)

            elif event == '_INVESTMENT_AMOUNT_':
                window.FindElement(event).Update(re.sub("[^0-9]", "", values[event]))

            user_credentials = {
                **user_credentials,
                'username': values['_USERNAME_'],
                'password': values['_PASSWORD_'],
                'investment_amount': values['_INVESTMENT_AMOUNT_'],
            }

            if event in (sg.WIN_CLOSED, 'Quit'):
                logger.info('Exiting program gracefully')
                window.close()
                sys.exit()

            elif event == 'Start':
                break

        window.close()

        if not os.path.isfile('secret.key'):
            generate_key()

        # Encrypts user password before storing it
        if user_credentials['password']:
            user_credentials['password'] = encrypt_password(user_credentials['password'])

        return dict() if user_credentials == user_credentials_template else user_credentials

    user_info = main()
    return user_info


if __name__ == '__main__':
    logger.info(login_gui())
