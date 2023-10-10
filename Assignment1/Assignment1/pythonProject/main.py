import re
import tkinter as tk
from tkinter.messagebox import showinfo
import windnd
from PIL import ImageTk, Image
import base64

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

Movenumber = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]  # the sheft number of sub keys
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,  # IP box
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]
IP_1 = [40, 8, 48, 16, 56, 24, 64, 32, 39,  # IP-1 box
        7, 47, 15, 55, 23, 63, 31, 38, 6,
        46, 14, 54, 22, 62, 30, 37, 5, 45,
        13, 53, 21, 61, 29, 36, 4, 44, 12,
        52, 20, 60, 28, 35, 3, 43, 11, 51,
        19, 59, 27, 34, 2, 42, 10, 50, 18,
        58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
E = [32, 1, 2, 3, 4, 5, 4, 5,  # E-box
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1]
P = [16, 7, 20, 21, 29, 12, 28, 17,  # P-box
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]
S = [  # S-box  the value of the list is a list whose value is also a list
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],

]


def cryption(text, key, type):  # the method of decryption or encryption
    BoralText = ''  # initialize binary text
    for c in text:  # Iterate over every letter or symbol in the source text
        l = bin(ord(c))[2:]  # Convert to binary by ASCII code
        length = len(l)  # if the length of the code is less than 8, add 0s in the front of the code
        for j in range(0, 8 - length):
            l = '0' + l
        BoralText = BoralText + l
    BoralKey = ''.join([bin(ord(c)).replace('0b', '') for c in
                        key])  # Because the key does not need to be converted back to a string, zero padding is not
    # required
    if type == 'decryption':  # When decrypted, the binary text is equal to the source text because the output
        # ciphertext is binary
        BoralText = text
    textlon = len(BoralText)
    keylon = len(BoralKey)
    if textlon % 64 != 0:              # when one part is less than 64, add 0s
        for i in range(64 - textlon % 64):
            BoralText = BoralText + "0"
    if keylon % 64 != 0:
        for i in range(64 - keylon % 64):
            BoralKey = BoralKey + "0"
    key = BoralKey[
          :64]  # When k is bigger than 64, the rest of k is useless, because extra bits are meaningless for Xor
    # calculation
    textlist = re.findall(r'.{64}', BoralText)  # Encrypt every 64-bit binary code
    keys = []  # the sub-keys list
    KeyPlus = ""  # the value of K+
    for j in PC1:  # PC - 1 replacement
        KeyPlus = KeyPlus + key[j - 1]
    C0 = KeyPlus[:28]
    D0 = KeyPlus[28:]
    for k in range(16):       # CnDn loop
        FrontC0 = C0[:Movenumber[k]]   # shift to the left of C0
        FC1 = FrontC0[::-1]
        AfterC0 = C0[Movenumber[k]:]
        AC1 = AfterC0[::-1]
        ReverseC1 = FC1 + AC1
        C1 = ReverseC1[::-1]
        C0 = C1
        FrontD0 = D0[:Movenumber[k]]     # shift to the left of D0
        FD1 = FrontD0[::-1]
        AfterD0 = D0[Movenumber[k]:]
        AD1 = AfterD0[::-1]
        ReverseD1 = FD1 + AD1
        D1 = ReverseD1[::-1]
        D0 = D1
        CDN = C0 + D0
        Kn = ""            # Kn Initialization
        for m in PC2:        # PC-2 replacement
            Kn = Kn + CDN[m - 1]
        keys.append(Kn)         # get sub-key list
    allresults = ''
    for i in textlist:    # Start looping every 64 bits of text
        Mip = ""         # IP replacement
        for j in IP:
            Mip = Mip + i[j - 1]
        L0 = Mip[:32]
        R0 = Mip[32:]
        for k in range(16):
            ER0 = ""       # E replacement
            for m in E:
                ER0 = ER0 + R0[m - 1]
            ER0k1 = ""           # Xor
            for m in range(48):
                if type == 'encryption':  # when encryption , Xor with kn
                    if ER0[m] == keys[k][m]:
                        ER0k1 = ER0k1 + "0"
                    else:
                        ER0k1 = ER0k1 + "1"
                else:
                    if ER0[m] == keys[15 - k][m]:   # when decryption, Xor with kn in adverse
                        ER0k1 = ER0k1 + "0"
                    else:
                        ER0k1 = ER0k1 + "1"
            Elist = re.findall(r'.{6}', ER0k1)    # S-box replacement
            i = 0
            Sresult = ""
            for m in Elist:
                Birow = m[:1] + m[5:]    # the first and the last number
                row = int(Birow, 2)
                Biline = m[1:5]     # the mid four number
                line = int(Biline, 2)
                TenS = S[i][row][line]
                i = i + 1
                Ss = ""
                for n in range(4):         # Decimal to binary
                    if TenS != 0:
                        Ss = Ss + str(TenS % 2)
                        TenS = int(TenS / 2)
                    else:
                        Ss = Ss + "0"
                Ss = Ss[::-1]
                Sresult = Sresult + Ss
            presult = ''
            for m in P:           # P box replacement
                presult = presult + Sresult[m - 1]
            XorResult = ""        # Xor
            for m in range(32):
                if presult[m] == L0[m]:
                    XorResult = XorResult + "0"
                else:
                    XorResult = XorResult + "1"
            L0 = R0          # this L0 means Ln
            R0 = XorResult     # this R0 means Rn
        final = R0 + L0    #R16L16
        result = ''
        for k in IP_1:      # IP-1 box replacement
            result = result + final[k - 1]
        allresults = result + allresults
    resultunits = re.findall(r'.{8}', allresults)  # Every eight bits of binary code can be converted to one character
    finalresult = allresults
    if type == "decryption":            # When decrypting, the resulting binary code needs to be converted to a string
        finalresult = ''.join([chr(i) for i in [int(b, 2) for b in resultunits]])
    paths = path.get()              # get the name of output file, the des text of + origin name
    names = paths.split("\\")
    name = names[len(names) - 1]
    if type == 'encryption':           # when encryption, the name of output file is the des text of + origin name
        title = 'The des text of ' + name +'.txt'
    else:                     # when decryption, the name of out put file is the origin text of + the origin name
        na = name.split(" ")
        name = ''
        for n in range(4,len(na)-1):
            name = name +  na[n] + " "
        last = na[len(na)-1]                  # change the type of the file to the origin type
        l = str(last).split('.')
        name = name + l[0]
        for n in range(1,len(l)-1):
            name = name + "." + l[n]
        title = 'The origin text of ' + name
    if type == 'encryption':
        f = open(title, 'w', encoding='utf-8')    # write the output file
        f.write(finalresult)
        f.close()
    else:
        try:
            con = bytes(finalresult,encoding='utf-8')           # decode the bytes, and write it
            f2 = base64.b64decode(con)
            f8 = open(title,'wb')
            f8.write(f2)
            f8.close()
        except BaseException:
            showinfo(title=None, message='key is wrong')

def button1():         # the method of encryption button on the main interface
    interface.withdraw()     # hide the old window
    newinterface = tk.Toplevel()       # get a new interface
    newinterface.resizable(0, 0)
    bg = ImageTk.PhotoImage(image)    # the background picture
    w = bg.width()
    h = bg.height()
    newinterface.geometry('%dx%d+500+300' % (w, h - 60))   # the size of the window
    newinterface.title('encryption')
    bgL = tk.Label(newinterface, image=bg)
    bgL.place(x=-2, y=-60)
    lb = tk.Label(newinterface, text='Please drag your file in this interface', bg='#87CEFA',
                  font=('Times New Roman', 14))    # hint of drag txt file
    lb.place(x=95, y=50)
    lb2 = tk.Label(newinterface, text='Please enter your key below', bg='#87CEFA',
                   font=('Times New Roman', 14))          # hint of entering key
    lb2.place(x=120, y=100)
    entry = tk.Entry(newinterface)     # the enter box
    entry.place(x=160, y=130)
    windnd.hook_dropfiles(newinterface, func=drag)     # the drag document function
    b = tk.Button(newinterface, text='encryption', command=lambda: button3(entry.get(), newinterface), bg='#87CEFA',
                  font=('Times New Roman', 14))       # encryption button
    b.place(x=180, y=180)
    back = tk.Button(newinterface, text='Back', command=lambda: button5(newinterface), bg='#87CEFA',
                     font=('Times New Roman', 12))    # back button
    back.place(x=380, y=220)
    newinterface.focus_force()   # focus on the new window
    newinterface.mainloop()


def button5(newinterface):   # the method of back function
    newinterface.destroy()      # destroy the top interface
    path.set('')           # clean the drag document
    interface.update()      # show the old interface
    interface.deiconify()


def drag(files):          # the method of drag document
    msg2 = '\n'.join((item.decode('gbk') for item in files))
    showinfo('your documents', msg2)          # the hint of drag successfully
    path.set(msg2)      # get the paths


def button2():   # the button of decryption button on the main interface, very similar to the encryption button
    interface.withdraw()   # hide the old window
    newinterface = tk.Toplevel()     # get a new window
    newinterface.resizable(0, 0)
    w = bg.width()
    h = bg.height()
    newinterface.geometry('%dx%d+500+300' % (w, h - 60))  # get the size
    newinterface.title('decryption')
    bgL = tk.Label(newinterface, image=bg)     # background label
    bgL.place(x=-2, y=-60)
    lb = tk.Label(newinterface, text='Please drag your des txt document in this interface', bg='#87CEFA',
                  font=('Times New Roman', 14))       # the hint
    lb.place(x=60, y=50)
    lb2 = tk.Label(newinterface, text='Please enter your key below', bg='#87CEFA',
                   font=('Times New Roman', 14))
    lb2.place(x=120, y=100)
    entry = tk.Entry(newinterface)
    entry.place(x=160, y=130)
    windnd.hook_dropfiles(newinterface, func=drag)  # the decryption button
    b = tk.Button(newinterface, text='decryption', command=lambda: button4(entry.get(), newinterface), bg='#87CEFA',
                  font=('Times New Roman', 14))
    b.place(x=180, y=180)
    back = tk.Button(newinterface, text='Back', command=lambda: button5(newinterface), bg='#87CEFA',
                     font=('Times New Roman', 12))       # the back button
    back.place(x=380, y=220)
    newinterface.focus_force()
    newinterface.mainloop()


def button3(yourkey, newinterface):  # the method of encryption button on encryption interface
    pathresult = path.get()
    paths = pathresult.split('\n')      # get paths
    d = 0   # it is used to judge if the file encrypt successfully
    for p in paths:    # get each path of paths
        if yourkey == "":      # judge if the user enter the key
            showinfo(title=None, message='Please enter your key')
        else:
            if p == '':    # judge if the user drag the document
                showinfo(title=None, message='Please drag your document')
                break
            else:
                path.set(p)
                binfile = open(p, 'rb')         # read the binary file, and encode it ,and covert it to string
                context = base64.b64encode(binfile.read())
                c = str(context,encoding='utf-8')
                cryption(c, yourkey, 'encryption')   # encryption the file
                d = 1
    if d == 1:   # when succeed, show the hint information, and destroy the top window, show the main interface
        showinfo(title=None, message='encrypt successfully')
        newinterface.destroy()
        path.set('')
        interface.update()
        interface.deiconify()


def button4(yourkey, newinterface):  # the method of decryption button on decryption window, it is similar to button3
    pathresult = path.get()
    paths = pathresult.split('\n')
    d = 0  # judge if the file decrypt successfully
    for p in paths:
        name = p.split('\\')
        judge = name[len(name) - 1].split(" ")
        j = 0
        if judge[0] == 'The' and judge[1] == 'des' and judge[2] == 'text':
            # judge if the file is a encrypted txt file according to the spacial name
            j = 1
        type = name[len(name) - 1].split('.')
        if type[len(type) - 1] != 'txt':    # if  a txt
            showinfo(title=None, message='Please drag a txt document')
        else:
            if j == 1:
                if yourkey == "":  # if the user enter a key
                    showinfo(title=None, message='Please enter your key')
                else:
                    if p == '':      # if the user drag a file
                        showinfo(title=None, message='Please drag your document')
                        break
                    else:
                        f = open(p, encoding='utf-8')
                        text = f.read()
                        path.set(p)            # decrypt the file
                        cryption(text, yourkey, 'decryption')
                        d = 1
            else:
                showinfo(title=None, message='Please drag a des txt document， the name is The des text of ...')
    if d == 1:     # when decryption successfully
        showinfo('congratulation!', 'decryption successfully!')
        newinterface.destroy()
        path.set('')
        interface.update()
        interface.deiconify()


def openMain(interface):   # the method of main interface
    interface.title('DES encryption and decryption')
    interface.resizable(0, 0)
    bgL = tk.Label(interface, image=bg, text='DES encryption', font=('Times New Roman', 25), compound='center')
    bgL.place(x=-2, y=-60)    # the background picture
    w = bg.width()
    h = bg.height()
    b1 = tk.Button(interface, text='encryption', command=button1, bg='#87CEFA', font=('Times New Roman', 14))
    b1.place(x=100, y=150)       # the encryption button
    b2 = tk.Button(interface, text='decryption', command=button2, bg='#87CEFA', font=('Times New Roman', 14))
    b2.place(x=280, y=150)    # the decryption button
    interface.geometry('%dx%d+500+300' % (w, h - 60))    # the size of the window
    interface.mainloop()


if __name__ == '__main__':
    interface = tk.Tk()   # get the main interface
    path = tk.StringVar()     # store the paths
    image = Image.open(r'bg.jpg')    # get the bg image
    bg = ImageTk.PhotoImage(image)
    openMain(interface)   # open the main interface

