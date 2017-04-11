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
import java.math.*;
class Action
{
    static String expFix(String f)
    {
        ArrayList<String> ops = new ArrayList<String>();
        ops.add("+");
        ops.add("-");
        ops.add("*");
        ops.add("/");
        ops.add("^");
        ops.add(",");
        String[] F = f.split("");
        String h,g;
        h="";
        g="";//If there is an easier way of doing this feel free to let me know, as this is very ugly.
        int n = 0;
        for(int i=f.length()-1; i>0; i=i-1)
        {
            if (F[i].contentEquals(")")){n++;}
            else if (F[i].contentEquals("(")){n--;}
            else if(F[i].contentEquals("^") && n==0)
            {
                
                for(int j=i-1; j>=0;j--)
                {
                    if(ops.contains((String)F[j]) && n==0)
                    {
                        g=f.substring(j+1, i);
                        for(int k=i+1; k<=f.length()-1;k++)
                        {
                            if(ops.contains((String)F[k]) && n==0)
                            {
                                h = f.substring(i+1, k);
                                break;
                            }
                            else if(k==f.length()-1)
                            {
                                h = f.substring(i+1,k);
                                if (h.contentEquals("")){h=(String)F[k];}
                                break;
                            }
                            else if (F[k].contentEquals(")")){n++;}
                            else if (F[k].contentEquals("(")){n--;}
                        }
                        f=f.replace(g+"^"+h,"Math.pow("+g+","+h+")");
                        break;
                    }
                    else if(j==0)
                    {
                        g=f.substring(0, i);
                        for(int k=i+1; k<=f.length()-1;k++)
                        {
                            if(ops.contains((String)F[k]) && n==0)
                            {
                                h = f.substring(i+1, k);
                                break;
                            }
                            else if(k==f.length()-1)
                            {
                                h = f.substring(i+1,k);
                                if (h.contentEquals("")){h=(String)F[k];}
                                break;
                            }
                            else if (F[k].contentEquals(")")){n++;}
                            else if (F[k].contentEquals("(")){n--;}
                        }
                        f=f.replace(g+"^"+h,"Math.pow("+g+","+h+")");
                        break;
                    }
                    else if (F[j].contentEquals(")")){n--;}
                    else if (F[j].contentEquals("(")){n++;}
                }
            break;
            }
        }      
        return f;
    }
    static String replaceMath(String f)
    {
        f=f.replace("cosh","Math.cosh");
        f=f.replace("sinh","Math.sinh");
        f=f.replace("tanh","Math.tanh");
        f=f.replace("cos","Math.cos");
        f=f.replace("sin","Math.sin");
        f=f.replace("tan","Math.tan");
        while(f.contains("^"))// For some reason if this loop is inside the method it never escapes.
        {
            f = expFix(f);
            f=f.replace("()","");
        }
        try{f=f.replace("/",".0/");}
        catch(Exception ex){}
        return f;
    }
}
class Equation
{
    static ScriptEngineManager mgr = new ScriptEngineManager();
    static ScriptEngine engine = mgr.getEngineByName("JavaScript");

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

        double yk = y3+4.0*h/3.0*(2*Yp2-Yp1+2*Yp);

        String Fyk = f.replace("x", "("+Double.toString(x)+")");
        Fyk = Fyk.replace("y", "("+Double.toString(yk)+")");
        double YpK=0;
        try {YpK=(double)(engine.eval(Fyk));}
        catch(Exception ex) {System.out.println(ex);}

        yk = y1+h/3*(Yp1+4*Yp+YpK);
        return yk;
    }
    public static void main(String[] args)
    {
        double x = 0;
        double y = 1;
        String f= "x+y+y^2";
        f=Action.replaceMath(f);

        System.out.println(f);
        double h = .1;
        double yt;
        Stack<Double> st = new Stack<Double>();//Stack for keeping order along with fixed number of values.
        for(int i=0; i<11; i++)
        {
            if(st.size()<4)
            {
                try{y = RungeKutta(f,y,x,h);}//potential infinity value.
                catch(Exception ex){System.out.println("Function error.");break;}
                x=x+h;
                Push4(st,y);
                System.out.println(st);
                System.out.println();
            }
            else if(st.size()==4)
            {
                System.out.println(st);
                yt = RungeKutta(f,y,x,h);
                y = Milne(f, st.get(0), st.get(1), st.get(2), st.get(3), h, x);
                System.out.println("Runge-kutta --> " + Double.toString(yt));
                System.out.println("Milne --> " + Double.toString(y));
                System.out.println();
                x=x+h;
                Push4(st,y);
            }
            else{System.out.println("Stack error.");break;}
        }
    }
}
class Project //Here begins the work for a system of ODEs
{
    static ScriptEngineManager mgr = new ScriptEngineManager();
    static ScriptEngine engine = mgr.getEngineByName("JavaScript");

    static void PopLast(Stack<ArrayList<Double>> st)
    {
        Collections.reverse(st);
        st.pop();
        Collections.reverse(st);
    }
    static void Push4(Stack<ArrayList<Double>> st, ArrayList<Double> a)
    {
        if(st.size()<4){st.push(a);}
        else if(st.size()==4){PopLast(st); st.push(a);}
    }
    static ArrayList<Double> RungeKutta(String f, String g, double x, double y, double t, double h)
    {//Systems really make these equations look bad.
        

        String Fq1 = f.replace("x", "("+Double.toString(x)+")");
        Fq1 = Fq1.replace("y", "("+Double.toString(y)+")");
        Fq1 = Fq1.replace("T", "("+Double.toString(t)+")");
        double q1f=0;
        try {q1f = h * (double)(engine.eval(Fq1));}
        catch(Exception ex) {System.out.println(ex);}

        String Gq1 = g.replace("x", "("+Double.toString(x)+")");
        Gq1 = Gq1.replace("y", "("+Double.toString(y)+")");
        Gq1 = Gq1.replace("T", "("+Double.toString(t)+")");
        double q1g=0;
        try {q1g = h * (double)(engine.eval(Gq1));}
        catch(Exception ex) {System.out.println(ex);}
        
        String Fq2 = f.replace("x", "("+Double.toString(x+q1f/2)+")");
        Fq2 = Fq2.replace("y", "("+Double.toString(y+q1f/2)+")");
        Fq2 = Fq2.replace("T", "("+Double.toString(t+h/2)+")");
        double q2f=0;
        try{q2f = h * (double)(engine.eval(Fq2));}
        catch(Exception ex){System.out.println(ex);}

        String Gq2 = g.replace("x", "("+Double.toString(x+q1g/2)+")");
        Gq2 = Gq2.replace("y", "("+Double.toString(y+q1g/2)+")");
        Gq2 = Gq2.replace("T", "("+Double.toString(t+h/2)+")");
        double q2g=0;
        try {q2g = h * (double)(engine.eval(Gq2));}
        catch(Exception ex) {System.out.println(ex);}

        String Fq3 = f.replace("x", "("+Double.toString(x+q2f/2)+")");
        Fq3 = Fq3.replace("y", "("+Double.toString(y+q2f/2)+")");
        Fq3 = Fq3.replace("T", "("+Double.toString(t+h/2)+")");
        double q3f=0;
        try{q3f = h * (double)(engine.eval(Fq3));}
        catch(Exception ex){System.out.println(ex);}

        String Gq3 = g.replace("x", "("+Double.toString(x+q2g/2)+")");
        Gq3 = Gq3.replace("y", "("+Double.toString(y+q2g/2)+")");
        Gq3 = Gq3.replace("T", "("+Double.toString(t+h/2)+")");
        double q3g=0;
        try {q3g = h * (double)(engine.eval(Gq3));}
        catch(Exception ex) {System.out.println(ex);}
        
        String Fq4 = f.replace("x", "("+Double.toString(x+q3f)+")");
        Fq4 = Fq4.replace("y", "("+Double.toString(y+q3f)+")");
        Fq4 = Fq4.replace("T", "("+Double.toString(t+h)+")");
        double q4f=0;
        try{q4f = h * (double)(engine.eval(Fq4));}
        catch(Exception ex){System.out.println(ex);}

        String Gq4 = g.replace("x", "("+Double.toString(x+q3g)+")");
        Gq4 = Gq4.replace("y", "("+Double.toString(y+q3g)+")");
        Gq4 = Gq4.replace("T", "("+Double.toString(t+h)+")");
        double q4g=0;
        try {q4g = h * (double)(engine.eval(Gq3));}
        catch(Exception ex) {System.out.println(ex);}

        double x1 = y+(1.0/6.0)*(q1f+2*q2f+2*q3f+q4f);
        double y1 = x+(1.0/6.0)*(q1g+2*q2g+2*q3g+q4g);
        ArrayList<Double> XY = new ArrayList<Double>();
        XY.add(y1);
        XY.add(x1);
        return XY;
        
    }
    static ArrayList<Double> Milne(String f, String g, double x3, double x2, double x1, double x, double y3, double y2, double y1, double y, double t, double h)
    {
        String Fy2 = f.replace("x", "("+Double.toString(x2)+")");
        Fy2 = Fy2.replace("y", "("+Double.toString(y2)+")");
        Fy2 = Fy2.replace("T", "("+Double.toString(t)+")");
        double Vp2f=0;
        try {Vp2f=(double)(engine.eval(Fy2));}
        catch(Exception ex) {System.out.println(ex);}

        String Gy2 = g.replace("x", "("+Double.toString(x2)+")");
        Gy2 = Gy2.replace("y", "("+Double.toString(y2)+")");
        Gy2 = Gy2.replace("T", "("+Double.toString(t)+")");
        double Vp2g=0;
        try {Vp2g=(double)(engine.eval(Gy2));}
        catch(Exception ex) {System.out.println(ex);}

        String Fy1 = f.replace("x", "("+Double.toString(x1)+")");
        Fy1 = Fy1.replace("y", "("+Double.toString(y1)+")");
        Fy1 = Fy1.replace("T", "("+Double.toString(t)+")");
        double Vp1f=0;
        try {Vp1f=(double)(engine.eval(Fy1));}
        catch(Exception ex) {System.out.println(ex);}

        String Gy1 = g.replace("x", "("+Double.toString(x1)+")");
        Gy1 = Gy1.replace("y", "("+Double.toString(y1)+")");
        Gy1 = Gy1.replace("T", "("+Double.toString(t)+")");
        double Vp1g=0;
        try {Vp1g=(double)(engine.eval(Gy1));}
        catch(Exception ex) {System.out.println(ex);}

        String Fy = f.replace("x", "("+Double.toString(x)+")");
        Fy = Fy.replace("y", "("+Double.toString(y)+")");
        Fy = Fy.replace("T", "("+Double.toString(t)+")");
        double Vpf=0;
        try {Vpf=(double)(engine.eval(Fy));}
        catch(Exception ex) {System.out.println(ex);}
        
        String Gy = g.replace("x", "("+Double.toString(x)+")");
        Gy = Gy.replace("y", "("+Double.toString(y)+")");
        Gy = Gy.replace("T", "("+Double.toString(t)+")");
        double Vpg=0;
        try {Vpg=(double)(engine.eval(Gy));}
        catch(Exception ex) {System.out.println(ex);}

        double yk = y3+4.0*h/3.0*(2*Vp2f-Vp1f+2*Vpf);
        double xk = x3+4.0*h/3.0*(2*Vp2g-Vp1g+2*Vpg);

        String Fyk = f.replace("x", "("+Double.toString(xk)+")");
        Fyk = Fyk.replace("y", "("+Double.toString(yk)+")");
        Fyk = Fyk.replace("T", "("+Double.toString(t)+")");
        double VpKf=0;
        try {VpKf=(double)(engine.eval(Fyk));}
        catch(Exception ex) {System.out.println(ex);}

        String Gyk = g.replace("x", "("+Double.toString(xk)+")");
        Gyk = Gyk.replace("y", "("+Double.toString(yk)+")");
        Gyk = Gyk.replace("T", "("+Double.toString(t)+")");
        double VpKg=0;
        try {VpKg=(double)(engine.eval(Gyk));}
        catch(Exception ex) {System.out.println(ex);}

        yk = y1+h/3*(Vp1f+4*Vpf+VpKf);
        xk = x1+h/3*(Vp1g+4*Vpg+VpKg);
        ArrayList<Double> XY = new ArrayList<Double>();
        XY.add(yk);
        XY.add(xk);
        return XY;
    }
    
    public static void main(String[] args)
    {
        ArrayList<Double> XY = new ArrayList<Double>();
        double x=0;
        double y=1;
        XY.add(y);
        XY.add(x);
        double t = 0;

        String f= "(1+cos(x))^2";
        String g= "(1+sin(y))^2";//if using time, must enter with T not t (look in Runge-kutta)
        f=Action.replaceMath(f);
        g=Action.replaceMath(g);
        
        System.out.println(f);
        System.out.println(g);
        double h = .001;
        Stack<ArrayList<Double>> st = new Stack<ArrayList<Double>>();
        Push4(st,XY);
        System.out.println(st);
        ArrayList<Double> XYt = new ArrayList<Double>();
        for(int i=0; i<0; i++)
        {
            if(st.size()<4)
            {
                try{XY = RungeKutta(f,g,XY.get(0),XY.get(1),t,h);}
                catch(Exception ex){System.out.println("Function error.");break;}
                t=t+h;
                Push4(st,XY);
                System.out.println(st);
                System.out.println();
            }
            else if(st.size()==4)
            {
                System.out.println(st);
                XYt = RungeKutta(f,g,XY.get(0),XY.get(1),t,h);
                XY = Milne(f, g, st.get(0).get(1), st.get(1).get(1), st.get(2).get(1), st.get(3).get(1), st.get(0).get(0), st.get(1).get(0), st.get(2).get(0), st.get(3).get(0), t, h);
                System.out.println("Runge-kutta --> "+XYt);
                System.out.println("Milne --> "+XY);
                System.out.println();
                t=t+h;
                Push4(st,XY);
            }
            else{System.out.println("Stack error.");break;}
        }
    }
}
