import java.lang.Thread;
import java.util.*;
import javax.swing.*;
import javax.swing.event.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import javax.imageio.*;
import javax.script.ScriptEngineManager;
import javax.script.ScriptEngine;

class Project
{
    static ScriptEngineManager mgr = new ScriptEngineManager();
    static ScriptEngine engine = mgr.getEngineByName("JavaScript");
    static double RungeKutta(String f, double y, double x, double h)
    {
        

        String Fq1 = f.replace("x", "("+Double.toString(x)+")");
        Fq1 = Fq1.replace("y", "("+Double.toString(y)+")");
        double q1=0;
        try {q1 = h * (double)(engine.eval(Fq1));}
        catch(Exception ex) {System.out.println(ex);}
        
        String Fq2 = f.replace("x", "("+Double.toString(x+h/2)+")");
        Fq2 = Fq2.replace("y", "("+Double.toString(y+q1/2)+")");
        double q2=0;
        try{q2 = h * (double)(engine.eval(Fq2));}
        catch(Exception ex){System.out.println(ex);}

        String Fq3 = f.replace("x", "("+Double.toString(x+h/2)+")");
        Fq3 = Fq3.replace("y", "("+Double.toString(y+q2/2)+")");
        double q3=0;
        try{q3 = h * (double)(engine.eval(Fq3));}
        catch(Exception ex){System.out.println(ex);}
        
        String Fq4 = f.replace("x", "("+Double.toString(x+h)+")");
        Fq4 = Fq4.replace("y", "("+Double.toString(y+q3)+")");
        double q4=0;
        try{q4 = h * (double)(engine.eval(Fq4));}
        catch(Exception ex){System.out.println(ex);}

        double y1 = y+(1.0/6.0)*(q1+2*q2+2*q3+q4);

        return y1;
    }
    static double Milne(String f, double y3, double y2, double y1, double y, double h, double x)
    {
        String Fy2 = f.replace("x", "("+Double.toString(x)+")");
        Fy2 = Fy2.replace("y", "("+Double.toString(y2)+")");
        double Yp2=0;
        try {Yp2=(double)(engine.eval(Fy2));}
        catch(Exception ex) {System.out.println(ex);}

        String Fy1 = f.replace("x", "("+Double.toString(x)+")");
        Fy1 = Fy1.replace("y", "("+Double.toString(y1)+")");
        double Yp1=0;
        try {Yp1=(double)(engine.eval(Fy1));}
        catch(Exception ex) {System.out.println(ex);}

        String Fy = f.replace("x", "("+Double.toString(x)+")");
        Fy = Fy.replace("y", "("+Double.toString(y)+")");
        double Yp=0;
        try {Yp=(double)(engine.eval(Fy));}
        catch(Exception ex) {System.out.println(ex);}

        double yk = y3+4*h/3.0*(2*Yp2-Yp1+2*Yp);

        String Fyk = f.replace("x", "("+Double.toString(x)+")");
        Fyk = Fyk.replace("y", "("+Double.toString(yk)+")");
        double YpK=0;
        try {YpK=(double)(engine.eval(Fyk));}
        catch(Exception ex) {System.out.println(ex);}

        yk = y1+h/3*(Yp1+4*Yp+YpK);
        return yk;
    }
    static void PopLast(Stack<Double> st)
    {
        Collections.reverse(st);
        st.pop();
        Collections.reverse(st);
    }
    static void Push4(Stack<Double> st, double a)
    {
        if(st.size()<4){st.push(a);}
        else if(st.size()==4){PopLast(st); st.push(a);}
    }

    public static void main(String[] args)
    {
        double x = 1;
        double y = 1;
        String f= "y*x";
        double h = .1;
        double yt;
        try{f=f.replace("/",".0/");}//also something wrong with squaring with ^
        catch(Exception ex){}//looking for a solution for next time
        Stack<Double> st = new Stack<Double>();
        for(int i=0; i<10; i++)
        {
            if(st.size()<4)
            {
                System.out.println(st);
                y = RungeKutta(f,y,x,h);
                x=x+h;
                Push4(st,y);
            }
            else if(st.size()==4)
            {
                System.out.println(st);
                y = Milne(f, st.get(3), st.get(2), st.get(1), st.get(0), h, x);
                yt = RungeKutta(f,y,x,h);
                System.out.println("Runge-kutta --> " + Double.toString(yt));
                System.out.println("Milne --> " + Double.toString(y));
                Push4(st,y);//not sure why the two numbers are so different
            }
        }
    }
}
