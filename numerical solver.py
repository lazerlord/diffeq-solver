# This program will give the option of either finding roots, finding
# the derivative at a point, or finding the area under the
# curve in a given interval. Also added Fourier Transform within
# the plotted region.

from graphics import *
from math import *
from button import *


def cbrt(x):
    return copysign(pow(abs(x), 1.0/3.0), x)

def plotWin(d, num):
    win = GraphWin('Graph '+num, 400, 400)
    win.setCoords(-d, -d, 0, d)
    return win
def plot(f, LEP, REP, win, color):
    d = abs(REP-LEP)

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
            y.setFill(color)
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
    lim1.setText('0')
    lim2.setText('1.145')

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
    point.setText('1.5')
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



def derivative(f, LEP, REP, num):
    x=evaluateAt()
    d = abs(REP-LEP)
    win = plotWin(d, num)
    plot(f, LEP, REP, win, 'cyan2')
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

    g='m*(X-x)+f(x)'
    y=eval(f.replace('x',str(x)))
    g=g.replace('f(x)', str(y))
    g=g.replace('x', str(x))

    Rep=str(REP)
    Lep=str(LEP)
    
    G = g.replace('X', Lep)
    y1=eval(G)
    G = g.replace('X', Rep)
    y2 = eval(G)
    y = Line(Point(-d, y1),Point(0,y2))
    y.setFill('red')
    y.setWidth(2)
    y.draw(win)

    return m
    
def integral(f, a, b):
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
        F = f.replace('x', x) # Must keep original function
                            #intact for multiple iterations.
        try:
            y = w*eval(F)       
            total = total + y
        except:
            pass
    area = total*abs(b-a)
    return area


def integralPlot(f, LEP, REP, num):
    a, b = limits()
    d = abs(REP-LEP)
    win = plotWin(d, num)
    plot(f, LEP, REP, win, 'cyan2')
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



    return integral(f, a, b)


def roots(f, LEP, REP, num):
    
    d = abs(REP-LEP)
    win = plotWin(d, num)
    plot(f, LEP, REP, win, 'cyan2')
    roots=[]

    for i in range(200):
        x1=((i)*d)/200-d/200+LEP
        x2=((i)*d)/200+d/200+LEP
        for k in range(100): #Added try statements because of
                            #some values overflowing/too large
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
                if -(10**(-10))<=v<=10**(-10): #10^-16 was a bit too small
                                    #to catch the zeroes of trig functions
                    
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
    v=eval(f.replace('x', str(0)))
    if -(10**(-10))<=v<=10**(-10):
        
            if LEP<=x3<=REP:
                 
                if 0 in roots:
                    pass
                else:
                    roots.append(0)

    roots.sort()
    for i in range(200):
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
        

def fourier(f, a, b, num):
    d = abs(b-a)
    win = plotWin(d, num)
    plot(f, a, b, win, 'cyan2')
    a0=1/(2*pi)*integral(f,a,b)
    Fa1= 'cos(x)*('+f+')'
    a1=1/pi*integral(Fa1,a,b)
    Fa2='cos(2*x)*('+f+')'
    a2=1/pi*integral(Fa2,a,b)
    Fa3='cos(3*x)*('+f+')'
    a3=1/pi*integral(Fa3,a,b)
    Fa4='cos(4*x)*('+f+')'
    a4=1/pi*integral(Fa4,a,b)
    Fa5='cos(5*x)*('+f+')'
    a5=1/pi*integral(Fa5,a,b)
    Fa6='cos(6*x)*('+f+')'
    a6=1/pi*integral(Fa6,a,b)
    Fa7='cos(7*x)*('+f+')'
    a7=1/pi*integral(Fa7,a,b)
    Fb1='sin(x)*('+f+')'
    b1=1/pi*integral(Fb1,a,b)
    Fb2='sin(2*x)*('+f+')'
    b2=1/pi*integral(Fb2,a,b)
    Fb3='sin(3*x)*('+f+')'
    b3=1/pi*integral(Fb3,a,b)
    Fb4='sin(4*x)*('+f+')'
    b4=1/pi*integral(Fb4,a,b)
    Fb5='sin(5*x)*('+f+')'
    b5=1/pi*integral(Fb5,a,b)
    Fb6='sin(6*x)*('+f+')'
    b6=1/pi*integral(Fb6,a,b)
    Fb7='sin(7*x)*('+f+')'
    b7=1/pi*integral(Fb7,a,b)
    

    g=str(a0)+'+'+str(a1)+'*cos(x)+'+str(a2)+'*cos(2*x)+'+\
       str(a3)+'*cos(3*x)+'+str(a4)+'*cos(4*x)+'+str(a5)+\
       '*cos(5*x)+'+str(a6)+'*cos(6*x)+'+str(a7)+'*cos(7*x)+'+\
       str(b1)+'*sin(x)+'+str(b2)+'*sin(2*x)+'+str(b3)+\
       '*sin(3*x)+'+str(b4)+'*sin(4*x)+'+str(b5)+'*sin(5*x)+'+\
       str(b6)+'*sin(6*x)+'+str(b7)+'*sin(7*x)'

    
    plot(g, a, b, win, 'red')
    

def main():
    win = GraphWin('Numerical Solver Pro', 400, 400)
    win.setCoords(-150, -100, 150, 100)

    title = Text(Point(0, 90), "Type in your function of x:")
    title.draw(win)

    entry = Entry(Point(0, 70), 30)
    entry.draw(win)
    entry.setText('sin(exp(x))*cbrt(x)')

    button1 = Button(Point(-140, 30), Point(-80, 0),'Integrate')
    button1.draw(win)

    button2 = Button(Point(-70, 30), Point(-10, 0),'Solve for \n roots')
    button2.draw(win)

    button3 = Button(Point(70, 30), Point(10, 0), 'Find \n derivative \n at a point')
    button3.draw(win)

    button4 = Button(Point(80, 30), Point(140, 0), 'Fourier \n Transform')
    button4.draw(win)

    lft = Text(Point(-40, -20), "   Plot from x =")
    lft.draw(win)
    rte = Text(Point(-40, -40), "                to x=")
    rte.draw(win)

    LEP = Entry(Point(30, -20), 5)
    LEP.draw(win)
    LEP.setText('-1')
    REP = Entry(Point(30, -40), 5)
    REP.draw(win)
    REP.setText('2')



    answer = Entry(Point(0, -85), 40)
    SolLabel = Text(Point(0, -70),'')

    i=1

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
            sol = integralPlot(f, Lep, Rep, str(i))
            SolLabel.setText('The area under the curve within the limits is')
            
            SolLabel.draw(win)
            
            answer.setText(sol)
            answer.draw(win)
            i+=1
        elif button2.isClicked(p):
            SolLabel.undraw()
            answer.undraw()
            
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            Roots=roots(f, Lep, Rep, str(i))
            
            SolLabel.setText('The roots of this function are')
            SolLabel.draw(win)

            answer.setText(Roots)
            answer.draw(win)
            i+=1
            
        elif button3.isClicked(p):
            SolLabel.undraw()
            answer.undraw()
            
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))
            
            m = derivative(f, Lep, Rep, str(i))
            
            SolLabel.setText('The derivative at the given point is')
            SolLabel.draw(win)

            answer.setText(str(m))
            answer.draw(win)
            i+=1

        elif button4.isClicked(p):
            SolLabel.undraw()
            answer.undraw()
            
            f = entry.getText()
            f = f.replace('^', '**')
            f = f.replace('exp', '2.718281828459045**')
            Lep = floor(eval(LEP.getText()))
            Rep = ceil(eval(REP.getText()))

            fourier(f,Lep,Rep, str(i))
            i+=1
            

        else:
            pass


main()

if __name__ == "__main__":
    main()
