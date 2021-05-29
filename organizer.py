import PySimpleGUI as sg
from datetime import date
from typing import List, Dict, TextIO

previous_data = []
try:
    with open('WOU - debtors.txt', 'r') as f1:
        for line in f1:
            line_list = "".join([char for char in line if \
                                 (char != '{' or char != '}')])
            previous_data.append(line_list)

except IOError:
    new_file = open('WOU - debtors.txt', 'x')

sg.theme('DarkAmber')
list_box = sg.Listbox(previous_data, size=(90, 10))

layout = [[list_box],
          [sg.Text("What's their name?*"), sg.InputText(key='debt_name')],
          [sg.Text("How much you need back? (in dollars)*    $"),\
           sg.InputText(size=(10, 1), key='debt_amount')],
          [sg.CalendarButton('When do they owe you?', key='date')],
          [sg.Text('Interest increase per day (in dollars)    $'),\
           sg.InputText(size=(10, 1), key='interest')],
          [sg.Submit(), sg.Cancel()],
          [sg.Text("* means you gotta enter the info", font=('Any 7'))]]
window = sg.Window('WhoOwesU?', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        debtor_name, date_due, interest_rate, amount =\
            values['debt_name'], values['date'], '$' + values['interest'],\
            '$' + values['debt_amount']
        if amount == '$' or debtor_name == '$':
            sg.popup('You gotta complete ALL the required information')
        else:
            window.close()
            third_line = ("Get it back by {}!").format(date_due)
            fourth_line = \
                ("If not, you get an extra {}/day!").format(interest_rate)
            if date_due in ('', None):
                third_line =\
                    "There's no deadline for when they have to pay you back"
                date_due = "No due date!"
            if interest_rate == '$':
                fourth_line = \
                    " No interest required!"
                interest_rate = "No interest applied!"
            sg.popup("Newly added: This person owes you. Get your cash back!!",\
                     debtor_name + ' has your money!',\
                     'They owe you ' + amount, third_line, fourth_line)
            with open('WOU - debtors.txt', 'a') as output_file:
                output_file.write(\
                    ("{0} | {1} | {2} | {3}\n").format(\
                    debtor_name, amount, date_due, interest_rate))
            break
window.close()





