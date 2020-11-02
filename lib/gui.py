#!/usr/bin/env python
import logging

import PySimpleGUI as sg


def login_gui():

    sg.theme('DarkAmber')

    def main():

        layout = [
            [sg.Text('myASNB Unit Holder Login', font='Any 21')],
            [sg.Text('Username'), sg.Input(key='asnb_username', tooltip='What is your myASNB account username?')],
            [sg.Text('Password'), sg.Input(key='asnb_password', password_char="*", tooltip='What is your myASNB account password?')],
            [sg.Text('Investment Amount (RM)'), sg.Input(key='investment_amount', tooltip='How much do you want to invest?')],
            [sg.OK(), sg.Cancel()],
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

        user_credentials = dict(username='', password='', investment_amount='0')

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Cancel', 'OK'):
                break
            # end if

            user_credentials = {
                **user_credentials,
                'username': values['asnb_username'],
                'password': values['asnb_password'],
                'investment_amount': values['investment_amount'],
            }
        # end while

        window.close()
        return user_credentials

    user_info = main()
    return user_info
    # end def
# end def


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info(login_gui())
# end if
