#coding=utf-8
from Tkinter import * 
def printkey(event):
	tmpRe = myProcess(u1.get())
	outPut = ''
	for tmp in tmpRe
		outPut=outPut+tmp[0]
	u2.set(outPut);
	
top = Tk()
#绑定对象到Entry
u1 = StringVar()
u2 = StringVar()
sample1  = Entry(top,textvariable = u1)
sample2 = Label(top,textvariable = u2)
sample1.bind('<Key-Return>', printkey)
sample1.pack()           
sample2.pack()
top.mainloop()
