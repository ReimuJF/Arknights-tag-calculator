import pytesseract
from PIL import Image, ImageGrab, ImageOps, ImageEnhance
from itertools import permutations
import tkinter as tk

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# if you have tesseract error

cool_combo_4 = {('AoE', 'Slow'), ('Caster', 'Slow'), ('DP-Recovery', 'Healing'),
                ('DPS', 'Slow'), ('Guard', 'Slow'), ('Healing', 'Support'),
                ('Melee', 'Slow'), ('Ranged', 'Survival'), ('Vanguard', 'Healing'),
                ('AoE', 'Debuff'), ('Caster', 'Debuff'), ('Sniper', 'Debuff'), ('DPS', 'Support'),
                ('Sniper', 'Survival'), ('Sniper', 'Slow'), ('Debuff', 'Ranged')}

cool_combo_5 = {('DPS', 'Healing'), ('Healing', 'Slow'), ('Fast-Redeploy', 'Debuff'),
                ('DP-Recovery', 'Support'), ('DPS', 'Shift'), ('Defender', 'Shift'), ('Defender', 'DPS'),
                ('Defender', 'Survival'), ('Defense', 'DPS'), ('Defense', 'Shift'), ('Defense', 'Survival'),
                ('Melee', 'Debuff'), ('Shift', 'Slow'), ('Specialist', 'Slow'), ('Survival', 'Specialist'),
                ('Supporter', 'DPS'), ('Supporter', 'Debuff'), ('Vanguard', 'Support'),
                ('Caster', 'Healing'), ('Defense', 'Guard'), ('AoE', 'Debuff'),
                ('Nuker', 'Sniper'), ('Nuker', 'Ranged'), ('Specialist', 'DPS')}

guaranteed = {'Top', 'Nuker', 'Specialist', 'Summon', 'Support',
              'Debuff', 'Crowd-Control', 'Senior', 'Shift', 'Fast-Redeploy'}

def get_image():
    txt_edit.delete("1.0", tk.END)
    try:
        image_in_buffer = ImageGrab.grabclipboard()
        image_in_buffer.save('1.png', 'PNG')
        image_to_invert = Image.open('1.png')
        image_to_invert = image_to_invert.convert('L')
        inverted_image = ImageOps.invert(image_to_invert)
        inverted_image.save('1.png', 'PNG')
        image_to_con = Image.open('1.png')
        enhancer = ImageEnhance.Contrast(image_to_con)
        image_out = enhancer.enhance(3)
        image_out.save('1.png', 'PNG')
        return image_out
        #image_out.save('1.png', 'PNG')
    except AttributeError:
        pass

def read_image() -> list:
    #tag_list = (pytesseract.pytesseract.image_to_string(Image.open('1.png'), config='--psm 12')).replace(',','')
    image = get_image()
    o_image = image if image else Image.open('1.png')
    tag_list = (pytesseract.pytesseract.image_to_string(o_image, config='--psm 12')).replace(',', '')
    # tag_list = 'Debuff Supporter Caster Defense Slow'
    return tag_list.split()
  
def get_combinations():
    tag_list = read_image()
    txt_edit.insert(tk.END, f'{tag_list}\n')
    flag = False
    for i in tag_list:
        if i == 'Top':
            txt_edit.insert(tk.END, f'WOW! {i} Operator! You get free 6 star!\n')
            flag = True
        elif i in guaranteed:
            txt_edit.insert(tk.END, f'Solo tag {i}. 5 or 4 star.\n')
            flag = True
    perm_tags = list(permutations(tag_list, 2))


    for i in perm_tags:
        if i in cool_combo_5:
            txt_edit.insert(tk.END, f'5 star {i}\n')
            flag = True
        elif i in cool_combo_4:
            txt_edit.insert(tk.END, f'4 star {i}\n')
            flag = True
    if not flag:
        txt_edit.insert(tk.END, '\nno cool tags')

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Arknights Tag Calculator')
    window.geometry('550x150+300+500')
    window.rowconfigure(0, minsize=100, weight=1)
    window.columnconfigure(1, minsize=100, weight=1)
    window.resizable(width=False, height=False)

    window.iconbitmap('icon.ico')

    frame_buttons = tk.Frame(window, bd=2)

    txt_edit = tk.Text(window)
    txt_edit.grid(row=0, column=1, sticky='wn')

    btn_calc = tk.Button(frame_buttons, text='Calculate Tags', command=get_combinations)
    btn_calc.grid(row=0, column=0, sticky='we', padx=0, pady=5)
    frame_buttons.grid(row=0, column=0, sticky='ns')
    window.mainloop()
