// Cristofear Santillan

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.math.BigInteger;
import java.util.Scanner;
import java.io.File;
import java.io.PrintWriter;
import java.io.FileNotFoundException;

public class Main {

  public static int readData( ArrayList<BigInteger> ms ){

    int x = 0;

    try{

      File inputFile = new File("input.txt");

      Scanner readFile = new Scanner(inputFile);

      x = readFile.nextInt();

      while ( readFile.hasNextBigInteger() ) {

        ms.add(readFile.nextBigInteger());

      }

      readFile.close();

    } catch (FileNotFoundException e) {

      e.printStackTrace();

    }

    return x;

  }

  public static void xgcd(BigInteger a, BigInteger b, ArrayList<BigInteger> coefficients){

    BigInteger q, r, holder, c1 = BigInteger.ONE, c2 = BigInteger.ZERO, x = BigInteger.ZERO, y = BigInteger.ONE;

    while ( !(b.equals(BigInteger.ZERO)) ){

      q = a.divide(b);
      r = a.mod(b);

      a = b;
      b = r;

      holder = x;
      x = c1.subtract(q.multiply(x));
      c1 = holder;

      holder = y;
      y = c2.subtract(q.multiply(y));
      c2 = holder;

    }

    coefficients.add(c1);
    coefficients.add(c2);

  }

  public static ArrayList<BigInteger> findMeasurements( ArrayList<BigInteger> ms ){

    ArrayList<BigInteger> measurements = new ArrayList<BigInteger>();

    LinkedHashMap<String, BigInteger> storage = new LinkedHashMap<String, BigInteger>();

    BigInteger gcd;

    int start1 = 0, start2 = 1, level = 1, tempSize = ms.size();

    while ( measurements.size() == 0 ){

      ArrayList<String> keys = new ArrayList<String>(storage.keySet());

      for(int i = start1; i < tempSize ;i++){

        for(int j = start2; j < ms.size() ;j++){

          if(level == 1){

            gcd = ms.get(i).gcd(ms.get(j));
            storage.put(String.format("%d.%d",i,j),gcd);

            if( gcd.equals(BigInteger.ONE) ){

              measurements.add(ms.get(i));
              measurements.add(ms.get(j));
              return measurements;

            }

          }else{

            gcd = storage.get(keys.get(i)).gcd(ms.get(j));
            storage.put(String.format("%s.%d",keys.get(i),j),gcd);
            start1 = tempSize;

            if( gcd.equals(BigInteger.ONE) ){

              for(String key: keys.get(i).split("\\.")){ measurements.add(ms.get(Integer.parseInt(key))); }
              measurements.add(ms.get(j));
              return measurements;

            }

          }

        }

        start2++;

      }

      tempSize = storage.size();

      start2 = ++level;

    }

    return measurements;

  }

  public static ArrayList<BigInteger> findCoefficients( int n, ArrayList<BigInteger> measurements ){

    ArrayList<BigInteger> coefficients = new ArrayList<BigInteger>();

    xgcd(measurements.get(0), measurements.get(1), coefficients);
    BigInteger gcd = measurements.get(0).gcd(measurements.get(1));

    int index = 2;

    for(int i = 2; i < measurements.size(); i++){

      xgcd(gcd, measurements.get(i), coefficients);

      for(int j = 0; j < index; j++){ coefficients.set(j,coefficients.get(j).multiply(coefficients.get(index))); }

      coefficients.remove(index);

      gcd = gcd.gcd(measurements.get(i));

      index++;

    }

    for(int i = 0; i < coefficients.size(); i++){ coefficients.set(i,coefficients.get(i).multiply(BigInteger.valueOf(n))); }

    return coefficients;

  }

  public static void outputData( LinkedHashMap<BigInteger, BigInteger> combination ){

    try{

      PrintWriter outFile = new PrintWriter(new File("output.txt"));

      for ( Map.Entry<BigInteger, BigInteger> e : combination.entrySet() ) {

        outFile.println(e.getKey() + " " + e.getValue());

      }

      outFile.close();

    } catch(FileNotFoundException e){

      e.printStackTrace();

    }

  }

  public static void main(String[] args) {
    
    ArrayList<BigInteger> ms = new ArrayList<BigInteger>();

    int x = readData(ms);

    ArrayList<BigInteger> measurements = findMeasurements(ms);

    ArrayList<BigInteger> coefficients = findCoefficients(x,measurements);

    LinkedHashMap<BigInteger, BigInteger> combination = new LinkedHashMap<BigInteger, BigInteger>();

    for(int i = 0; i < measurements.size(); i++){combination.put(measurements.get(i), coefficients.get(i));}

    outputData(combination);

  }

}
