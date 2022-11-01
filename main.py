import pytesseract
from PIL import Image, ImageGrab, ImageOps, ImageEnhance
from itertools import permutations
import tkinter as tk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cool_combo_4 = [('AoE', 'Slow'), ('Caster', 'Slow'), ('DP-Recovery', 'Healing'),
                ('DPS', 'Slow'), ('Guard', 'Slow'), ('Healing', 'Support'),
                ('Melle', 'Slow'), ('Ranged', 'Survival'), ('Vanguard', 'Healing'),
                ('AoE', 'Debuff'), ('Caster', 'Debuff'), ('Sniper', 'Debuff')]

cool_combo_5 = [('DPS', 'Healing'), ('Healing', 'Slow'), ('Fast-Redeploy', 'Debuff'),
                ('DP-Recovery', 'Support'), ('DPS', 'Shift'), ('Defender', 'Shift'), ('Defender', 'DPS'),
                ('Defender', 'Survival'), ('Defense', 'DPS'), ('Defense', 'Shift'), ('Defence', 'Survival'),
                ('Melee', 'Debuff'), ('Shift', 'Slow'), ('Specialist', 'Slow'), ('Survival', 'Specialist'),
                ('Supporter', 'DPS'), ('Supporter', 'Debuff'), ('Vanguard', 'Support')]


def calculate_tags():
    txt_edit.delete("1.0", tk.END)

    try:
        image_in_buffer = ImageGrab.grabclipboard()
        image_in_buffer.save('1.png', 'PNG')
        image_to_invert = Image.open('1.png')
        image_to_invert = image_to_invert.convert('L')
        inverted_image = ImageOps.invert(image_to_invert)
        #image_to_invert = image_to_invert.convert('1')
        inverted_image.save('1.png', 'PNG')
        image_to_con = Image.open('1.png')
        enhancer = ImageEnhance.Contrast(image_to_con)
        image_out = enhancer.enhance(2)
        image_out.save('1.png', 'PNG')
    except AttributeError:
        pass

    tag_list = pytesseract.pytesseract.image_to_string(Image.open('1.png'), config='--psm 12')
    # tag_list = 'Debuff Supporter Caster Defense Slow'
    txt_edit.insert(tk.END, f'{tag_list.split()}\n')
    perm_tags = list(permutations(tag_list, 2))

    flag = False

    for i in perm_tags:
        if i in cool_combo_5:
            txt_edit.insert(tk.END, f'5 star {i}\n')
            flag = True
        elif i in cool_combo_4:
            txt_edit.insert(tk.END, f'4 star {i}\n')
            flag = True
    else:
        if not flag:
            txt_edit.insert(tk.END, '\nno cool tags')


window = tk.Tk()
window.title('Arknights Tag Calculator')
window.geometry('550x150+300+500')
window.rowconfigure(0, minsize=100, weight=1)
window.columnconfigure(1, minsize=100, weight=1)
window.resizable(width=False, height=False)

frame_buttons = tk.Frame(window, bd=2)

txt_edit = tk.Text(window)
txt_edit.grid(row=0, column=1, sticky='wn')

btn_calc = tk.Button(frame_buttons, text='Calculate Tags', command=calculate_tags)
btn_calc.grid(row=0, column=0, sticky='we', padx=0, pady=5)
frame_buttons.grid(row=0, column=0, sticky='ns')
window.mainloop()
