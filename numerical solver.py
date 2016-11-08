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
        try: #Fixes Divide by Zero errors
            y = eval(F)
            y = Point(-d, y)
            y.setFill('cyan2')
            y.draw(win)
        except:
            pass
        
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
    lim1.setText('1.145')
    lim2.setText('1.837')

    while True:
        p = win.getMouse()
        
        if button.isClicked(p):
            win.close()
            break
        else:
            pass

    return eval(lim1.getText()), eval(lim2.getText())

def evaluateAt():
    win = GraphWin('Evaluation Point')
    win.setCoords(-5, -5, 5, 5)

    title = Text(Point(0, 3.5), "Put in what point you \n want to evaluate the \n derivative at")
    title.draw(win)

    point=Entry(Point(0, 0), 15)
    point.setText('1.145')
    point.draw(win)

    end=Button(Point(-2,-2),Point(2,-3.5), 'Done')
    end.draw(win)

    while True:
        p=win.getMouse()

        if end.isClicked(p):
            win.close()
            break
        else:
            pass

    return eval(point.getText())


def derivative(f, LEP,REP):
    x=evaluateAt()
    d = abs(REP-LEP)
    win = plot(f, LEP, REP)
    h=0.0078125
    xM3h=str(x-3*h)
    xM2h=str(x-2*h)
    xMh=str(x-h)
    xPh=str(x+h)
    xP2h=str(x+2*h)
    xP3h=str(x+3*h)

    #Using derivative of 6th degree collocation polynomial
    #Could do extrapolation but after testing it shows to be less acurate
    #6th degree collocation polynomial has average accuracy of 14 digits of accuracy

    FxM3h=f.replace('x',xM3h)
    FxM2h=f.replace('x',xM2h)
    FxMh=f.replace('x',xMh)
    FxPh=f.replace('x',xPh)
    FxP2h=f.replace('x',xP2h)
    FxP3h=f.replace('x',xP3h)

    m = (-eval(FxM3h)+9*eval(FxM2h)-45*eval(FxMh)+45*eval(FxPh)-9*eval(FxP2h)+eval(FxP3h))/(60*h)

    print(m)
    g='m*(X-x)+f(x)'
    y=eval(f.replace('x',str(x)))
    g=g.replace('f(x)', str(y))
    g=g.replace('x', str(x))
    

    for i in range(d*1000):
        i = LEP+i*.001
        d = abs(REP-i) 
        i = str(i)
        G = g.replace('X', i)
        y = eval(G)
        y = Point(-d, y)
        y.setFill('red')
        y.draw(win)

    return m

    
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
            y.setFill('red')
            y.draw(win)
        else:
            pass



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
        try:
            y = w*eval(F)       #itterations.
            total = total + y
        except:
            pass
    area = total*abs(b-a)

    return area


def roots(f, LEP, REP):
    
    d = abs(REP-LEP)
    win = plot(f, LEP, REP)
    roots=[]

    for i in range(100):
        x1=((i+1)*d)/100-d/100+LEP
        x2=((i+1)*d)/100+d/100+LEP
        for k in range(100): #Added try statements because of some values overflowing/too large
            try:
                X1=str(x1)
                X2=str(x2)
                F1=f.replace('x', X1)
                F2=f.replace('x', X2)
            
            
                if eval(F1)==0:
                    x3=x1
                    break
                if eval(F1)-(eval(F2))==0:
                    break
            
                x3=x1-eval(F1)*(x1-x2)/(eval(F1)-(eval(F2)))
            except:
                break
            x1,x2=x2,x3

        try: #Fixes Divide by Zero errors
            X3=str(x3)
            try:
                v=eval(f.replace('x', X3))
                if -(10**(-10))<=v<=10**(-10): #10^-16 was a bit too small to catch the zeroes of trig functions
                    
                    x3=round(x3,8)
                    if LEP<=x3<=REP:
                    
                        if x3 in roots:
                            pass
                        else:
                            roots.append(x3)
            except:
                pass
        except:
            pass


    roots.sort()
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

        
    return roots
        

def main():
    win = GraphWin('Numerical Solver Pro', 400, 400)
    win.setCoords(-150, -100, 150, 100)

    title = Text(Point(0, 90), "Type in your function of x:")
    title.draw(win)

    entry = Entry(Point(0, 70), 30)
    entry.draw(win)
    entry.setText('sin(exp(x))/x^2')

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
    LEP.setText('0')
    REP = Entry(Point(30, -40), 5)
    REP.draw(win)
    REP.setText('2')



    answer = Entry(Point(0, -85), 40)
    SolLabel = Text(Point(0, -70),'')

    while True:
        p = win.getMouse()

        
        
        if button1.isClicked(p):
                 #undraw things from different labels and answer boxes
            SolLabel.undraw()
            answer.undraw()
                

            
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            sol = integral(f, Lep, Rep)
            SolLabel.setText('The area under the curve within the limits is')
            
            SolLabel.draw(win)
            
            answer.setText(sol)
            answer.draw(win)
        elif button2.isClicked(p):
            SolLabel.undraw()
            answer.undraw()
            
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            Roots=roots(f,Lep,Rep)
            
            SolLabel.setText('The roots of this function are')
            SolLabel.draw(win)

            answer.setText(Roots)
            answer.draw(win)
            
        elif button3.isClicked(p):
            SolLabel.undraw()
            answer.undraw()
            
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            
            m = derivative(f,Lep,Rep)
            
            SolLabel.setText('The derivative at the given point is')
            SolLabel.draw(win)

            answer.setText(str(m))
            answer.draw(win)

        else:
            pass


main()

if __name__ == "__main__":
    main()
