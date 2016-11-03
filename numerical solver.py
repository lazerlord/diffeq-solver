# This program will give the option of either finding roots, finding
# the derivative at a point, or finding the area under the
# curve in a given interval.

from graphics import *
from math import *
from button import *


def plot(f, LEP, REP):
    d = abs(REP-LEP)
    win = GraphWin('Graph', 400, 400)
    win.setCoords(-d, -d, 0, d)

    xAxis = Line(Point(-d, 0), Point(0, 0))
    xAxis.draw(win)

    yAxis = Line(Point(-abs(REP), -d), Point(-abs(REP), d))
    yAxis.draw(win)
    for i in range(d*1000):
        i = LEP+i*.001
        d = abs(REP-i) # cannot have number - string, TypeError.
        i = str(i)
        F = f.replace('x', i)
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

    button = Button(Point(-2, 0), Point(2, -3), 'Done')
    button.draw(win)
    lim1.setText('-.8')
    lim2.setText('-.3')

    while True:
        p = win.getMouse()
        
        if button.isClicked(p):
            win.close()
            break
        else:
            pass

    return eval(lim1.getText()), eval(lim2.getText())


def integral(f, LEP, REP):
    a, b = limits()
    d = abs(REP-LEP)
    win = plot(f, LEP, REP)
    A = str(a) # a<i<b will not work if a and b are strings, TypeError.
    B = str(b)

    for i in range(d*1000):
        i = LEP+i*.001
        if a < i < b:
            d = abs(REP-i)
            i = str(i)
            F = f.replace('x', i) #keep original function intact
            y = eval(F)
            y = Line(Point(-d, y), Point(-d, 0))
            y.setFill('cyan2')
            y.draw(win)
        else:
            pass

    # should the following two if statements be indented

    # What this does is print the location of the left and right limits. 
    # The if statements are to make sure they are inside the graphed region.


    if a < REP:
        aPoint = Text(Point(-abs(REP-a), -d/8), A)
        aPoint.setStyle('bold')
        aPoint.draw(win)
    else:
        pass

    if b > LEP:
        bPoint = Text(Point(-abs(REP-b), -d/8), B)
        bPoint.setStyle('bold')
        bPoint.draw(win)
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
        F = f.replace('x', x) # Must keep original function intact for multiple
        y = w*eval(F)       #itterations.
        total = total + y
    area = total*abs(b-a)

    return area


def roots(f, LEP, REP):
    
    d = abs(REP-LEP)
    win = plot(f, LEP, REP)
    roots=[]

    for i in range(100):
        x1=((i+1)*d)/100-d/100+LEP
        x2=((i+1)*d)/100+d/100+LEP
        for k in range(100):
            X1=str(x1)
            X2=str(x2)
            F1=f.replace('x', X1)
            F2=f.replace('x', X2)
            if eval(F1)==0:
                x3=x1
                break
            if 1-(eval(F2)/eval(F1))==0:
                break
            x3=x1-(x1-x2)/(1-(eval(F2)/eval(F1)))
            x1,x2=x2,x3

        X3=str(x3)
        v=eval(f.replace('x', X3))
        if -(10**(-20))<=v<=10**(-20):
            
            x3=round(x3,8)
            if LEP<=x3<=REP:
            
                if x3 in roots:
                    pass
                else:
                    roots.append(x3)

            
            


    
    for i in range(100):
        if i<=len(roots)-1:
            p=-abs(REP-roots[i])
            point=Circle(Point(p,0),d/80)
            point.setOutline('red')
            point.setFill('red')
            point.draw(win)
            text=Text(Point(p, -d/8), str(roots[i]))
            text.draw(win)
        else:
            break
        

def main():
    win = GraphWin('Numerical Solver Pro', 400, 400)
    win.setCoords(-150, -100, 150, 100)

    title = Text(Point(0, 90), "Type in your function of x:")
    title.draw(win)

    entry = Entry(Point(0, 70), 30)
    entry.draw(win)
    entry.setText('(x-.5)^2*(x+.5)*(x-1)')

    button1 = Button(Point(-130, 30), Point(-70, 0),'Integrate')
    button1.draw(win)

    button2 = Button(Point(-30, 30), Point(30, 0),'Solve for \n roots')
    button2.draw(win)

    button3 = Button(Point(130, 30), Point(70, 0), 'Find \n derivative \n at a point')
    button3.draw(win)

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

        # Dr. Kubota made the graphics file so idk if we are allowed to
        # go in and change it
        
        if button1.isClicked(p):
            # try:
                # undraw things from different labels and answer boxes
                
                # does not seem to work
                
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
        elif button2.isClicked(p):
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            roots(f,Lep,Rep)
        elif button3.isClicked(p):
            pass  # not done yet
        else:
            pass


main()

if __name__ == "__main__":
    main()
