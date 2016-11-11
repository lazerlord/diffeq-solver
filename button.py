from graphics import *
class Button:
    def __init__(self, p1, p2, label):
        self.rect = Rectangle(p1,p2)
        self.text = Text(Point((p1.getX()+p2.getX())/2 , (p1.getY()+p2.getY())/2), label)
        self.p1 = Point(min(p1.getX(),p2.getX()), min(p1.getY(),p2.getY()))
        self.p2 = Point(max(p1.getX(),p2.getX()), max(p1.getY(),p2.getY()))

    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)
        self.win = win

    def isClicked(self, p):
        if self.p1.getX()<p.getX()<self.p2.getX() and self.p1.getY()<p.getY()<self.p2.getY():
            return True
        else:
            return False

if __name__ == "__main__":
    win = GraphWin('button test', 200,200)
    button = Button(Point(150,50),Point(50,150),'click me')
    button.draw(win)
    while True:
        p = win.getMouse()
        if button.isClicked(p):
            break

    win.close()
