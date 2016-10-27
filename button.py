from graphics import *


def midpoint(p1, p2):
    x1 = p1.getX()
    x2 = p2.getX()
    y1 = p1.getY()
    y2 = p2.getY()

    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    return Point(x, y)


def squareButton_push(tfPoint, brPoint):
    m = win.getMouse()

    if(m.getX() >= tfPoint.getX() and m.getX() <= brPoint.getX() and
       m.getY() >= tfPoint.getY() and m.getY() <= brPoint.getY()):
        return True


def button(tfPoint, brPoint, text, win):
    shape = Rectangle(tfPoint, brPoint)
    mid = midpoint(tfPoint, brPoint)
    button_text = Text(mid, text)
    shape.draw(win)
    button_text.draw(win)



w = 500
win = GraphWin("Title", w, w)
p1 = Point(50, 50)
p2 = Point(100, 100)
button(p1, p2, "stuff", win)

while(True):
    if(squareButton_push(p1, p2)):
        print("lol")
