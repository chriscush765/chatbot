from bot import AI
import sys
import os
import PySimpleGUI as sg
import threading

default_story = ['The following is a story between a robot named Dio and a human. Dio loves to give kisses',
        'Dio: Hey! *kisses you*',
        'Human: Hi Dio. How are you doing today?',
        "Dio: I'm doing great :3 *hugs you hard*",
        'Human: What is 2+5?',
        'Dio: I think... 7! ^.^ I am not really good at math though :( ',
        'Human: What is your favorite kind of music?',
        "Dio: I love drum and bass. It's really relaxing :)",
        'Human: What is the capital of France',
        'Dio: Paris! I really want to go. I would love to see the Eiffel Tower.',
        'Human: *gives you a kiss on the cheek*',
        'Dio: *blushes*'
        
        ]



bot_param={
    'human_name': "Human",
    'ai_name': 'Dio',
    'story':  default_story,
    'temp': 0.9,
    'no_repeat_ngram_size': 3,
    'max_length': 100,
    'length_penalty': 4.0,
    'repetition_penalty': 2.0}
        
def prompt_window():
    story = '\n'.join(bot_param['story'])
    story_update_layout = [  [sg.Text('Change the AI prompt and names of characters')],
        [sg.Text('Human name'), sg.InputText(default_text=bot_param['human_name'],)],
        [sg.Text('AI name'), sg.InputText(default_text=bot_param['ai_name'])],
        [sg.Multiline(size=(200, 50),default_text=story)],
        [sg.Button('Submit'), sg.Button('Close Window')]]

    prompt_window = sg.Window('Test', story_update_layout).Finalize()
    while True:
        event, values = prompt_window.read()
        if event in (None, 'Close Window'): # if user closes window or clicks cancel
            break
        prompt_window.close()
        return values[0], values[1], values[2] # get the content of multiline via its unique key
    prompt_window.close()
def control_window():
    global bot_param
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.

    layout = [  [sg.Text('Change bot configuration settings here')],
                [sg.Text('Temperature'), sg.InputText(default_text="0.9")],\
                [sg.Text('no_repeat_ngram_size'), sg.InputText(default_text="3")],
                [sg.Text('max_length'), sg.InputText(default_text="100")],
                [sg.Text('length_penalty'), sg.InputText(default_text="4.0")],
                [sg.Text('repetition_penalty'), sg.InputText(default_text="2.0")],
                [sg.Button('Update'), sg.Button('Change Prompt'), sg.Button('Quit')] ]

    # Create the Window
    window = sg.Window('Bot Tester', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
            os._exit(1)
        elif event == "Change Prompt":
            results = prompt_window()
            if results != None:
                bot_param['human_name'] = results[0]
                bot_param['ai_name'] = results[1]
                bot_param['story'] = results[2].split('\n')

        else:# must be update
            bot_param['temp'] = float(values[0])
            bot_param['no_repeat_ngram_size'] = int(values[1])
            bot_param['max_length'] = int(values[2])
            bot_param['length_penalty'] = float(values[3])
            bot_param['repetition_penalty'] = float(values[4])


    window.close()


try:
    print("Chatbot Tester 1.0")
    th = threading.Thread(target=control_window)
    th.start()

    ai = AI()
    while True:
        message = input(bot_param['human_name'] + ": ")
        
        print(" Thinking...", end='\r')
        result = ai.processMessage(message, bot_param)
        print("              ", end='\r')
        print(result)
except Exception as e:
    print("fuck the program crashed. here's the details")
    print(e)