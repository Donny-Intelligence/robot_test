import webbrowser
main_speech ='Good morning'
user_name = 'Don'
news = f'Hello {user_name}'
html_content0 = f"<html> " \
                   f"<head> " \
                   f"<title>Page Title</title>" \
                   f"<meta http-equiv='refresh' content= '2' >" \
                   f"</head> <font size='+2''>{main_speech} </font>" \
                   f"<h1> <br><br> <img src='images/adam_talk.png'/> Adam: {news}</h1> " \
                   f"<body> </body> " \
                   f"<html>"


with open("index.html", "w") as html_file1:
    html_file1.write(html_content0)
    print("html content renew")

# textfile_h = open(f'display_history.txt', 'w')
# textfile_h.close()
# textfile_u = open(f'user_speech.txt', 'w')
# textfile_u.close()


def renew_display(new_sentence, num_adam_history, role):
    #  open the buffer txt
    # =====================
    with open(f'display_history.txt') as f:
        history = f.readlines()
    with open(f'user_speech.txt') as f:
        user_speech = f.readlines()
    if not history:
        history = [f'Hello {user_name} I am listening']
    if not user_speech:
        user_speech = ['(Your speech will display in here)']
    # initial variable
    history_display = ''
    adam_sentence = 'I am listening'
    user_sentence = '(Your speech will display in here)'
    num = len(history)
    # =====================
    # =====================
    # renew the html information
    if role == 'robot':
        adam_sentence = new_sentence
        user_sentence = user_speech[0]

        i = 0
        if num < num_adam_history:
            num_adam_history = num
        while True:
            if i == num_adam_history:
                break
            else:
                history_display = f"{history_display}{history[num - num_adam_history + i]}<br>"
                i = i + 1
        # renew the buffer file
        textfile_h = open(f'display_history.txt', 'a')
        textfile_h.write(f'\n {new_sentence}')
        textfile_h.close()

    elif role == "user":
        user_sentence = new_sentence
        adam_sentence = history[num-1]
        # renew the buffer file
        textfile_h = open(f'user_speech.txt', 'w')
        textfile_h.write(new_sentence)
        textfile_h.close()

        i = 0
        if num < num_adam_history:
            num_adam_history = num
        while True:
            if i == num_adam_history:
                break
            else:
                history_display = f"{history_display}{history[num - num_adam_history + i]}<br>"
                i = i + 1
                print(history_display)

    # =====================
    html_content = f"<html> " \
                   f"<head> " \
                   f"<title>Page Title</title>" \
                   f"<meta http-equiv='refresh' content= '1' >" \
                   f"</head>" \
                   f"<body>" \
                   f"<h1 style = 'color:black; font-size:2vw; text-align: center'/> Chat history<br></h1>" \
                   f"<p style = 'color:black; font-size:2vw; text-align: center'/>{history_display} </p>" \
                   f"<hr>"\
                   f"<h2 style = 'color:green; font-size:3vw'> Adam's speech</h2> " \
                   f"<img src='images/adam_talk.png'; style ='height: 10%; width: 10%; object-fit: contain; float:left'/>" \
                   f"<h3 style = 'color:green; font-size:3vw'> :{adam_sentence} </h3> " \
                   f"<hr>"\
                   f"<h5 style = 'color:blue; font-size:2vw; text-align: right'/>" \
                   f"{user_name}: {user_sentence} " \
                   f"</h5> " \
                   f"<hr>" \
                   f"<p style = 'color:black; font-size:2vw; text-align: center'/> " \
                   f"<br> Hint 1: {user_name} demo hint1 here" \
                   f"<br> Hint 2: {user_name} demo hint2 here" \
                   f"<img src='images/adam_happy.png'; style ='height: 20%; width: 10%; display: block; margin-left: auto; margin-right: auto; float:up'/>" \
                   f"</p> " \
                   f"<hr>" \
                   f"</body> " \
                   f"<html>"

    with open("index.html", "w") as html_file:
        html_file.write(html_content)
        print("html content renew")


if __name__ == '__main__':
    renew_display('9int robot', 2, 'robot')
    renew_display('9int user', 2, 'user')

    webbrowser.open("index.html", new=0)
