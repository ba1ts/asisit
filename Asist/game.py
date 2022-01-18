import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
 
 
class Cons:
 
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27
 
 
class Board(Canvas):
 
    def __init__(self):
        super().__init__(
            width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
            background="blue", highlightthickness=0
        )
 
        self.initGame()
        self.pack()
 
    def initGame(self):
        """
        Инициализация игры.
        """
 
        self.inGame = True
        self.dots = 3
        self.score = 0
 
        # Переменные для передвижения замеи.
        self.moveX = Cons.DOT_SIZE
        self.moveY = 0
 
        # Изначальные стартовые координаты яблоки.
        self.appleX = 100
        self.appleY = 190
 
        self.loadImages()
 
        self.createObjects()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Cons.DELAY, self.onTimer)
 
    def loadImages(self):
        """
        Подгружаем нужные изображения для игры.
        """
 
        try:
            self.idot = Image.open("dot.png")
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open("head.png")
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open("apple.png")
            self.apple = ImageTk.PhotoImage(self.iapple)
 
        except IOError as e:
            print(e)
            sys.exit(1)
 
    def createObjects(self):
        """
        Создание объектов на холсте.
        """
 
        self.create_text(
            30, 10, text="Счет: {0}".format(self.score),
            tag="score", fill="white"
        )
 
        self.create_image(
            self.appleX, self.appleY, image=self.apple,
            anchor=NW, tag="apple"
        )
 
        self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
        self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
        self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")
 
    def checkAppleCollision(self):
        """
        Проверяем, не столкнулась ли голова змеи с яблоком.
        """
 
        apple = self.find_withtag("apple")
        head = self.find_withtag("head")
 
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
 
        for ovr in overlap:
 
            if apple[0] == ovr:
 
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
                self.locateApple()
 
    def moveSnake(self):
        """
        Меняем положение змеи на холсте.
        """
 
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
 
        items = dots + head
 
        z = 0
        while z < len(items)-1:
 
            c1 = self.coords(items[z])
            c2 = self.coords(items[z+1])
            self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
            z += 1
 
        self.move(head, self.moveX, self.moveY)
 
    def checkCollisions(self):
        """
        Проверка на столкновение змеи с другими объектами.
        """
 
        dots = self.find_withtag("dot")
        head = self.find_withtag("head")
 
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
 
        for dot in dots:
            for over in overlap:
                if over == dot:
                  self.inGame = False
 
        if x1 < 0:
            self.inGame = False
 
        if x1 > Cons.BOARD_WIDTH - Cons.DOT_SIZE:
            self.inGame = False
 
        if y1 < 0:
            self.inGame = False
 
        if y1 > Cons.BOARD_HEIGHT - Cons.DOT_SIZE:
            self.inGame = False
 
    def locateApple(self):
        """
        Распределяем яблоки по холсту (canvas).
        """
 
        apple = self.find_withtag("apple")
        self.delete(apple[0])
 
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleY = r * Cons.DOT_SIZE
 
        self.create_image(
            self.appleX, self.appleY, anchor=NW,
            image=self.apple, tag="apple"
        )
 
    def onKeyPressed(self, e):
        """
        Управляем змеей через стрелки клавиатуры.
        """
 
        key = e.keysym
 
        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            self.moveX = -Cons.DOT_SIZE
            self.moveY = 0
 
        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = Cons.DOT_SIZE
            self.moveY = 0
 
        RIGHT_CURSOR_KEY = "Up"
        if key == RIGHT_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = -Cons.DOT_SIZE
 
        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = Cons.DOT_SIZE
 
    def onTimer(self):
        """
        Создает игровой цикл для каждого события таймера
        """
 
        self.drawScore()
        self.checkCollisions()
 
        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(Cons.DELAY, self.onTimer)
        else:
            self.gameOver()
 
    def drawScore(self):
        """
        Рисуем счет игры
        """
 
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Счет: {0}".format(self.score))
 
    def gameOver(self):
        """
        Удаляем все объекты и выводим сообщение об окончании игры.
        """
 
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height()/2,
            text="Игра закончилась со счетом {0}".format(self.score), fill="white")
 
 
class Snake(Frame):
 
    def __init__(self):
        super().__init__()
        self.master.title('Змейка')
        self.board = Board()
        self.pack()
 
 
def main():
    root = Tk()
    nib = Snake()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()
self.createObjects()
self.locateApple()
self.bind_all("<Key>", self.onKeyPressed)
try:
    self.idot = Image.open("dot.png")
    self.dot = ImageTk.PhotoImage(self.idot)
    self.ihead = Image.open("head.png")
    self.head = ImageTk.PhotoImage(self.ihead)
    self.iapple = Image.open("apple.png")
    self.apple = ImageTk.PhotoImage(self.iapple)
 
except IOError as e:
    print(e)
    sys.exit(1)
def createObjects(self):
    """
    Создание объектов на холсте.
    """
 
    self.create_text(
        30, 10, text="Счет: {0}".format(self.score),
        tag="score", fill="white"
    )
 
    self.create_image(
        self.appleX, self.appleY, image=self.apple,
        anchor=NW, tag="apple"
    )
 
    self.create_image(50, 50, image=self.head, anchor=NW, tag="head")
    self.create_image(30, 50, image=self.dot, anchor=NW, tag="dot")
    self.create_image(40, 50, image=self.dot, anchor=NW, tag="dot")
apple = self.find_withtag("apple")
head = self.find_withtag("head")
x1, y1, x2, y2 = self.bbox(head)
overlap = self.find_overlapping(x1, y1, x2, y2)
for ovr in overlap:
  
    if apple[0] == ovr:
        x, y = self.coords(apple)
        self.create_image(x, y, image=self.dot, anchor=NW, tag="dot")
        self.locateApple()
z = 0
while z < len(items)-1:
    c1 = self.coords(items[z])
    c2 = self.coords(items[z+1])
    self.move(items[z], c2[0]-c1[0], c2[1]-c1[1])
    z += 1
self.move(head, self.moveX, self.moveY)
x1, y1, x2, y2 = self.bbox(head)
overlap = self.find_overlapping(x1, y1, x2, y2)
 
for dot in dots:
    for over in overlap:
        if over == dot:
          self.inGame = False
if y1 > HEIGHT - DOT_SIZE:
    self.inGame = False
apple = self.find_withtag("apple")
self.delete(apple[0])
r = random.randint(0, Cons.MAX_RAND_POS)
Python
self.appleX = r * Cons.DOT_SIZE
...
self.appleY = r * Cons.DOT_SIZE



	
self.appleX = r * Cons.DOT_SIZE
self.appleY = r * Cons.DOT_SIZE

	
LEFT_CURSOR_KEY = "Left"
 
if key == LEFT_CURSOR_KEY and self.moveX <= 0:
    self.moveX = -Cons.DOT_SIZE
    self.moveY = 0
def onTimer(self):
    """
    Создает игровой цикл для каждого события таймера
    """
 
    self.drawScore()
    self.checkCollisions()
 
    if self.inGame:
        self.checkAppleCollision()
        self.moveSnake()
        self.after(Cons.DELAY, self.onTimer)
    else:
        self.gameOver()
def drawScore(self):
    """
    Рисуем счет игры
    """
 
    score = self.find_withtag("score")
    self.itemconfigure(score, text="Счет: {0}".format(self.score))
def gameOver(self):
    """
    Удаляем все объекты и выводим сообщение об окончании игры.
    """
 
    self.delete(ALL)
    self.create_text(self.winfo_width() / 2, self.winfo_height()/2,
        text="Игра закончилась со счетом {0}".format(self.score), fill="white")
