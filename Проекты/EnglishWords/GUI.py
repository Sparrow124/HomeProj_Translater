from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re

our_dict = {}  # dict with {key(english_word):value(russian_words)}
index_key = 0  # index for iteration global key
index_value = 0  # index for iteration global value
true_answers = 0  # quantity of correct answers
incorrect_answers = 0  # quantity of incorrect answers
index_for_field_text = 1.0  # index for Text field, as one of args


def start_prog():
    """reading file and create dict like {'eng_word':'rus_words'}"""
    with open('Words.txt', 'r', encoding='utf-8') as file_with_words:
        for line in file_with_words:
            try:
                key, value = line.split(' - ')  # splitting every line as 'eng' - 'rus'
                our_dict[key] = value
            except ValueError:
                messagebox.showinfo('File Error',
                                    "Your file contains incorrectly entered words\nFix it because application can slow down")


def start_work():
    """func for start_button, printing first key to field with rus words"""
    start_prog()
    first = list(our_dict.values())[0]
    rus_word.delete(0, END)
    rus_word.insert(0, first)
    field_for_end.delete(0.0, END)


def answer_button(event=None):
    """func for add_button: add new word in field with rus_word, sort what we entered in eng_field, and sorts everything into fields, depending on the correctness of the answer"""
    try:
        k = list(our_dict.keys())  # created list with keys
        v = list(our_dict.values())  # created list with values

        text_for_label_1, text_for_label_2, color_cool, color_not_cool = 'CORRECT', 'WRONG', 'green', 'red'  # values for change_color_func
        text_for_empty_list = 'Your list with words is empty! \nRestart the application if you want to repeat'  # just for set as arguments in func

        global index_value, index_key, true_answers, incorrect_answers, index_for_field_text  # get global variables for count

        if len(rus_word.get()) == 0:  # error if we click answer button before start
            messagebox.showinfo('Error', 'You Need Start Firstly')

        else:
            introduced = eng_word.get()  # get what we printed in field
            introduced.lower()  # bring it to lower case

            if introduced == k[index_key]:  # if our answer is correct
                try:  # for check non-empty list with words
                    index_value += 1
                    index_key += 1
                    true_answers += 1
                    rus_word.delete(0, END)  # delete word from field
                    rus_word.insert(0, v[index_value])  # add next word

                    add_number_to_correct_field(true_answers)
                    change_label_with_color(text_for_label_1, color_cool)  # change label's color if we answered correct
                    clear_english_field()

                except IndexError:  # list is empty
                    rus_word.delete(0, END)
                    rus_word.insert(0, 'List with your words is EMPTY!')

                    add_number_to_correct_field(true_answers)
                    change_label_with_color(text_for_label_1,
                                            color_cool)  # change label's color if we answered correct, and our list is empty

                    messagebox.showerror('THE END', text_for_empty_list)  # show error if empty

            else:  # if our asnwer is incorrect
                try:
                    index_value += 1
                    index_key += 1
                    incorrect_answers += 1
                    index_for_field_text += 1.0
                    rus_word.delete(0, END)  # delete word from field
                    rus_word.insert(0, v[index_value])  # add next word

                    add_number_to_wrong_field(incorrect_answers)
                    add_words_to_text(index_for_field_text, k[index_key - 1])

                    change_label_with_color(text_for_label_2,
                                            color_not_cool)  # change label's color if we answered incorrect
                    clear_english_field()

                except IndexError:  # if list is empty

                    rus_word.delete(0, END)
                    rus_word.insert(0, 'List with your words is EMPTY!')

                    add_number_to_wrong_field(incorrect_answers)
                    add_words_to_text(index_for_field_text, k[index_key - 1])

                    change_label_with_color(text_for_label_2,
                                            color_not_cool)  # change label's color if we answered incorrect, and our list is empty

                    messagebox.showerror('THE END', text_for_empty_list)  # show error if empty
    except IndexError:
        messagebox.showerror('Error', 'You Need Start Firstly')


def change_label_with_color(text, color):
    """func for change color label(label_right_or_not)"""
    if text == 'correct':
        label_right_or_not['text'] = text
        label_right_or_not['fg'] = color
    else:
        label_right_or_not['text'] = text
        label_right_or_not['fg'] = color


def add_words_to_text(number, word):
    """add all wrong words in text field"""
    field_for_end.insert(number, word + '\n')


def clear_english_field():
    """clearing field function"""
    eng_word.delete(0, END)


def hint_button():
    """function for new window with hint"""
    if len(rus_word.get()) == 0:  # error if we click hint button before start or if our field is empty
        messagebox.showinfo('Error', 'You need start firstly')
    else:
        a = list(our_dict.keys())
        messagebox.showinfo('Hint', a[index_key])


def add_number_to_correct_field(number):
    """+1 in field where we count our correct answers"""
    entry_correct.delete(0.0, END)
    entry_correct.insert(1.0, 'Correct:' + '\n' + str(number))


def add_number_to_wrong_field(number):
    """-1 in field where we count our correct answers"""
    entry_wrong.delete(0.0, END)
    entry_wrong.insert(0.0, 'Wrong:' + '\n' + str(number))


def button_add_delete_new_word():
    """create new window for add/delete words from our file"""

    def clear_button():
        """clear fields"""
        field_for_eng.delete(0, END)
        field_for_translate.delete(0, END)

    def add_word_button():
        """function for button wich adding new word in file"""
        from_eng_field = field_for_eng.get().lower()
        from_transl_field = field_for_translate.get().lower()
        with open('Words.txt', 'a', encoding='utf-8') as file_with_words:
            file_with_words.write(
                from_eng_field + ' - ' + from_transl_field + '\n')  # first '\n' to avoid writing at line where already words
            field_for_eng.delete(0, END)
            field_for_translate.delete(0, END)
            messagebox.showinfo('Saved', 'Saved')

    def delete_word_button():
        """delete from file, find all matches in file, for example u can enter only: sun, and it offer you for delete all lines with 'sun'(sun/sunny etc, if you forgot full word)"""
        from_eng_field = field_for_eng.get().lower()
        from_transl_field = field_for_translate.get().lower()

        if len(from_eng_field) == 0:
            messagebox.showinfo('Error', 'Enter the whole or part of the word in English field')
        else:
            index = 0  # index for check line
            list_with_matches = []  # list with indexes of matches line

            with open('Words.txt', 'r', encoding='utf-8') as file_with_words:
                list_with_lines = file_with_words.readlines()
                for line in list_with_lines:
                    index += 1
                    if re.search(from_eng_field, line):  # get index of matches
                        list_with_matches.append(index)  # append index of match

                if len(list_with_matches) != 0:  # if we catch some matches
                    list_with_matches.reverse()  # for delete from end
                    for value in list_with_matches:
                        question = messagebox.askyesno('Confirm', 'Are you want delete: ' + '{}'.format(
                            list_with_lines[value - 1]).upper())
                        if question == True:  # asking about matches, this word or not user want delete
                            del list_with_lines[value - 1]  # delete
                            messagebox.showinfo('Deleted', 'Successful')
                            field_for_eng.delete(0, END)
                        else:
                            messagebox.showinfo('Canceled', 'Canceled')  # if user did not want delete this word
                    with open('Words.txt', 'w', encoding='utf-8') as file_with_words:
                        file_with_words.writelines(list_with_lines)
                else:
                    messagebox.showinfo('Empty', 'No Matches')

    add_window = Toplevel(bg='black')  # create new window for add/delete
    add_window.title('Add/Delete Window')
    add_window.geometry('360x71')  # resolution of window
    add_window.resizable(width=False, height=False)  # block change resolution

    label_english = Label(add_window, text='English', bg='black', fg='white').grid(row=0,
                                                                                   column=0)  # Field for english Word
    label_translate = Label(add_window, text='Translate', bg='black', fg='white').grid(row=1, column=0)  # Field for

    field_for_eng = Entry(add_window, width=50, bg='black', fg='white')
    field_for_translate = Entry(add_window, width=50, bg='black', fg='white')

    clear_fields = Button(add_window, text='Clear', bg='black', fg='white', command=clear_button).grid(row=2, column=1,
                                                                                                       sticky=W)
    add_new_word = Button(add_window, text='Add', bg='black', fg='white', command=add_word_button).grid(row=2, column=2)
    delete_word = Button(add_window, text='Delete', bg='black', fg='white', command=delete_word_button).grid(row=2,
                                                                                                             column=3,
                                                                                                             sticky=E)

    field_for_eng.grid(row=0, column=1, columnspan=3, sticky=W + E)  # grid on another line because we will take values
    field_for_translate.grid(row=1, column=1, columnspan=3)  # same as for eng


def close_app():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


"""GUI"""
root = Tk()

windowWidth = root.winfo_reqwidth()  # get width in pixels
windowHeight = root.winfo_reqheight()  # get height in pixels
positionRight, positionDown = int(root.winfo_screenwidth() / 2 - windowWidth / 2), int(
    root.winfo_screenheight() / 5 - windowHeight / 5)  # create position on monitor
root.geometry("484x700+{}+{}".format(positionRight, positionDown))  # size window
root.resizable(width=False, height=False)  # block change resolution
root.title('Translater')

photo = ImageTk.PhotoImage(Image.open('img.jpg').resize((484, 700)))  # background image
Image_background = Label(root, image=photo)  # Label as background with image
Image_background.place(x=0, y=0, relwidth=1, relheight=1)  # set resolution for our image

photo_2 = ImageTk.PhotoImage(Image.open('img2.jpg').resize((100, 100)))  # image for buttons

rus_word = Entry(width=40, bg='black', fg='white', font=('Verdana', 10))  # field with rus word
eng_word = Entry(width=19, bg='black', fg='white', font=('Verdana', 10))  # field with eng word

button_hint = Button(text='Hint', bg='black', fg='white', width=100, height=40, image=photo_2, compound=CENTER,
                     command=hint_button)  # hint button
button_answer = Button(text='Answer', bg='black', fg='white', width=100, height=40, image=photo_2, compound=CENTER,
                       command=answer_button)  # answer button

label_right_or_not = Label(text='CORRECT/WRONG', width=105, height=40, bg='black', fg='white', image=photo_2,
                           compound=CENTER)  # label for correct/incorrect answers

field_for_end = Text(width=30, height=15, bg='black', fg='white', wrap=NONE)  # field for incorrect answer, for yours

rus_word.grid(row=0, column=0, padx=1)  # field with rus word
eng_word.grid(row=0, column=5, padx=1)  # field with eng word
eng_word.bind('<Return>', answer_button)  # now can click Return in english field instead of button Answer

button_hint.grid(row=1, column=0, sticky=W, padx=1)  # hint button
button_answer.grid(row=1, column=5, sticky=E, padx=1)  # answer button

label_right_or_not.grid(row=2, column=0, columnspan=6, sticky=N)  # correct/incorrect label
root.grid_rowconfigure(3, minsize=300)  # change size of 3rd row, for invisible step for our widgets below
field_for_end.grid(row=4, column=0, columnspan=4, sticky=W + E)  # text field

button_add_delete = Button(text='Add/delete word', bg='black', fg='white', width=100, height=38, image=photo_2,
                           compound=CENTER, command=button_add_delete_new_word)  # add button
button_add_delete.grid(row=5, column=0, sticky=N + S + W)

button_start = Button(text='START', bg='black', fg='white', width=100, height=38, image=photo_2, compound=CENTER,
                      command=start_work)  # start button
button_start.grid(row=5, column=5, sticky=N + S + E)

entry_correct = Text(width=9, height=2, bg='black', fg='white',
                     font=('Verdana', 10))  # text-field for count-correct answers
entry_wrong = Text(width=9, height=2, bg='black', fg='white',
                   font=('Verdana', 10))  # text-field for count-incorrect answers

entry_wrong.grid(row=4, column=5, sticky=N + E)
entry_correct.grid(row=4, column=5, sticky=N + W)

root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()

if __name__ == '__main__':
    start_work()
