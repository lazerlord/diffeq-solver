from graphics import *


def midpoint(p1, p2):  # takes two Point objects as parameters
    x1 = p1.getX()
    x2 = p2.getX()
    y1 = p1.getY()
    y2 = p2.getY()

    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    return Point(x, y)  # returns the midpoint as a Point object


def squareButton_push(topLeftPoint, bottomRightPoint, win):
    # takes 2 points and GraphWin as parameters
    m = win.getMouse()

    if(m.getX() >= topLeftPoint.getX() and
       m.getX() <= bottomRightPoint.getX() and
       m.getY() >= topLeftPoint.getY() and
       m.getY() <= bottomRightPoint.getY()):
        return True
        # returns True if a square 'button' is clicked in a particular GraphWin


def button(tfPoint, brPoint, text, win):
    # takes top-left, bottom-right Point objects,
    #   String, and GraphWin as parameters

    shape = Rectangle(tfPoint, brPoint)
    mid = midpoint(tfPoint, brPoint)
    button_text = Text(mid, text)  # text displayed in center of button
    shape.draw(win)
    button_text.draw(win)


def main():  # example usage
    w = 500
    win = GraphWin("Title", w, w)
    p1 = Point(50, 50)
    p2 = Point(100, 100)
    button(p1, p2, "stuff", win)

    while(True):
        if(squareButton_push(p1, p2, win)):
            print("lol")  # printed only if button clicked

if __name__ == "__main__":
    main()
