import pytesseract
import pyperclip
import re
import tkinter as tk
import tags5
import tags4
from PIL import Image, ImageGrab, ImageOps, ImageEnhance


# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# if you have tesseract error


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
    except AttributeError:
        pass


def read_image() -> list:
    image = get_image()
    o_image = image if image else Image.open('1.png')
    tag_list = re.sub('[.,_~*;"]', '', pytesseract.pytesseract.image_to_string(o_image, config='--psm 12'))
    # tag_list = 'Survival Ranged Healing Support'
    return tag_list.split()


def get_combinations():
    tag_list = sorted(read_image())
    txt_edit.insert(tk.END, f'{", ".join(tag_list)}\n')
    res = []

    for index, tag in enumerate(tag_list):
        if tag == 'Top':
            res.append(f'WOW! {tag} Operator! You get free 6 star!')
            continue
        elif tag == 'Senior':
            res.append(f'{tag} Operator! You get free 5 star!')
            continue
        elif tag in tags5.tag_combo_5:
            res.append(f'{tag}: {tags5.tag_combo_5[tag]} | 5 star')
        elif tag in tags4.tag_combo_4:
            res.append(f'{tag}: {tags4.tag_combo_4[tag]} | 4 star')
        for second_tag in tag_list[index + 1:]:
            tag_combo = (tag, second_tag)
            if tag_combo in tags5.tag_combo_5:
                res.append(f"{' + '.join(tag_combo)}: {tags5.tag_combo_5[tag_combo]} | 5 star")
            elif (tag, second_tag) in tags4.tag_combo_4:
                res.append(f"{' + '.join(tag_combo)}: {tags4.tag_combo_4[tag_combo]} | 4 star")

    txt_edit.insert(tk.END, '\nNo guaranteed tags' if not res else f'\n'.join(res))


def copy_text(event):
    content = txt_edit.selection_get()
    cleared_content = ''.join(content.split())
    pyperclip.copy(cleared_content)
    return "break"


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
    txt_edit.bind("<Control-c>", copy_text)
    window.mainloop()
