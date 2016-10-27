# This program will give the option of either finding roots, finding
# the derivative at a point, or finding the area under the
# curve in a given interval.

from graphics import *
from math import *


def plot(f, LEP, REP):
    d = abs(REP-LEP)
    win = GraphWin('Graph', 400, 400)
    win.setCoords(-d, -d, 0, d)

    xAxis = Line(Point(-d, 0), Point(0, 0))
    xAxis.draw(win)

    yAxis = Line(Point(-abs(REP), -d), Point(-abs(REP), d))
    yAxis.draw(win)
    for i in range(d*1000):
        i = str(LEP+i*.001)
        d = abs(REP-i)
        I = str(i) # Must convert number into a string before putting into existing string, else will cause TypeError
        F = f.replace('x', I) # Since the number changes everytime through the loop we cannot replace original string
        y = eval(F)
        y = Point(-d, y)
        y.setFill('cyan2')
        y.draw(win)
    return win


def limits():
    win = GraphWin('limits')
    win.setCoords(-5, -5, 5, 5)

    title = Text(Point(0, 4), "Put in your limits")
    title.draw(win)

    lim1_text = Text(Point(-2, 3), "left limit:")
    lim1 = Entry(Point(1, 3), 5)
    lim1_text.draw(win)
    lim1.draw(win)

    lim2_text = Text(Point(-2, 1), "right limit:")
    lim2 = Entry(Point(1, 1), 5)
    lim2_text.draw(win)
    lim2.draw(win)

    button = Rectangle(Point(-2, 0), Point(2, -3))
    button.draw(win)
    lim1.setText('-.8')
    lim2.setText('-.3')

    done = Text(Point(0, -1.5), 'Done')
    done.draw(win)

    win.getMouse()
    win.close()

    return eval(lim1.getText()), eval(lim2.getText())
    # wtf are you returning here? a tuple??


def integral(f, LEP, REP):
    a, b = limits()
    d = abs(REP-LEP)
    win2 = plot(f, LEP, REP)
    a = str(a)
    a = str(b)

    for i in range(d*1000):
        i = LEP+i*.001
        if a < i < b:
            d = abs(REP-i)
            i = str(i)
            f = f.replace('x', I)
            y = eval(F)
            y = Line(Point(-d, y), Point(-d, 0))
            y.setFill('cyan2')
            y.draw(win2)
        else:
            pass

    # should the following two if statements be indented

    if a < REP:
        aPoint = Text(Point(-abs(REP-a), -d/8), A)
        aPoint.setStyle('bold')
        aPoint.draw(win2)
    else:
        pass

    if b > LEP:
        bPoint = Text(Point(-abs(REP-b), -d/8), B)
        bPoint.setStyle('bold')
        bPoint.draw(win2)
    else:
        pass

    # Gaussian quadrature for n=16, accuracy is high but a bit of a setup
    xi = [0.005299532504175031, 0.0277124884633837, 0.06718439880608407,
          0.12229779582249845, 0.19106187779867811, 0.27099161117138637,
          0.35919822461037054, 0.45249374508118123, 0.5475062549188188,
          0.6408017753896295, 0.7290083888286136, 0.8089381222013219,
          0.8777022041775016, 0.9328156011939159, 0.9722875115366163,
          0.9947004674958250]
    wi = [0.013576229705876844, 0.03112676196932382, 0.04757925584124612,
          0.06231448562776691, 0.07479799440828848, 0.08457825969750153,
          0.09130170752246194, 0.0947253052275344, 0.0947253052275344,
          0.09130170752246194, 0.08457825969750153, 0.07479799440828848,
          0.06231448562776691, 0.04757925584124612, 0.03112676196932382,
          0.013576229705876844]
    # now that those are out of the way we may start integration

    total = 0
    for i in range(16):
        x = xi[i]*abs(b-a)+a
        x = str(x)
        w = wi[i]
        f = f.replace('x', X)
        y = w*eval(F)
        total = total + y
    area = total*abs(b-a)

    return area


def main():
    win = GraphWin('Numerical Solver Pro', 400, 400)
    win.setCoords(-150, -100, 150, 100)

    title = Text(Point(0, 90), "Type in your function of x:")
    title.draw(win)

    entry = Entry(Point(0, 70), 30)
    entry.draw(win)
    entry.setText('(x-.5)^2*(x+.5)*(x-1)')

    button1 = Rectangle(Point(-130, 30), Point(-70, 0))
    button1.draw(win)
    button1Text = Text(Point(-100, 15), 'Integrate')
    button1Text.draw(win)

    button2 = Rectangle(Point(-30, 30), Point(30, 0))
    button2.draw(win)
    button2Text = Text(Point(0, 15), 'Solve of \n roots')
    button2Text.draw(win)

    button3 = Rectangle(Point(130, 30), Point(70, 0))
    button3.draw(win)
    button3Text = Text(Point(100, 15), 'Find \n derivative \n at a point')
    button3Text.draw(win)

    lft = Text(Point(-40, -20), "   Plot from x =")
    lft.draw(win)
    rte = Text(Point(-40, -40), "                to x=")
    rte.draw(win)

    LEP = Entry(Point(30, -20), 5)
    LEP.draw(win)
    LEP.setText('-1')
    REP = Entry(Point(30, -40), 5)
    REP.draw(win)
    REP.setText('1')

    while True:
        p = win.getMouse()
        if -130 <= p.getX() <= -70 and 0 <= p.getY() <= 30:
            # try:
                # undraw things from different labels and answer boxes
                # SolLabel.undraw()
                # answer.undraw()
            # except GraphicsError:
                # pass
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            sol = integral(f, Lep, Rep)
            SolLabel = Text(Point(0, -70),
                            'The area under the curve within the limits is')
            SolLabel.draw(win)
            answer = Entry(Point(0, -85), 20)
            answer.setText(sol)
            answer.draw(win)
        elif -30 <= p.getX() <= 30 and 0 <= p.getY() <= 30:
            pass  # not done yet
        elif 70 <= p.getX() <= 130 and 0 <= p.getY() <= 30:
            pass  # not done yet
        else:
            pass


main()

if __name__ == "__main__":
    main()
