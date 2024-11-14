from tkinter import *
import math
size=600
root=Tk() #окно
canvas= Canvas(root, width=size, height=size) #холст
canvas.pack()
speed=5
direct=1 # 1- по часовой / -1 - против
angle=0
def move():
    global angle
    canvas.delete('all') #удаление всего
    canvas.create_oval(300-200, 300-200, 300+200, 300+200, outline="green", fill="white", width=2) #круг в точке (300;300) с рад 200
    canvas.create_oval(300+200*math.cos(math.radians(angle))-5, 300+200*math.sin(math.radians(angle))-5,
                      300+200*math.cos(math.radians(angle))+5, 300+200*math.sin(math.radians(angle))+5, fill='red')
    #Формула для расчета координат точки на окружности выглядит следующим образом:
    #x = center_x + radius * cos(angle)
    #y = center_y + radius * sin(angle)
    # +5 и -5 для создания точки диаметром 10
    angle+=speed*direct #обновление угла на основе скорости и направления
    root.after(16, move) #вызов функции move повторно через 16 милисекунд для анимации движения точки
move()
root.mainloop()