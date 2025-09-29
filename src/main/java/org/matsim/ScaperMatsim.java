package org.matsim;

import java.io.IOException;

public class ScaperMatsim {

    public static void main(String[] args) throws IOException {

        if (args == null || args.length != 2 || args[0] == null) {
            System.out.println("Proper Usage is: java [options, jar file] org.matsim.ScaperMatsim [run | skim] /path/to/config.[xml|yaml]");
            System.out.println(args.length);
            System.exit(0);
        } else 
        {
            if(args[0].equals("run"))
            {
                RunMatsim.Simulate(args[1]);
            } 
            else if(args[0].equals("skim"))
            {
                SkimMatrices.Run(args[1]);
            }
            else{
                System.out.println(args[0]);
                System.out.println(args[1]);
                System.out.println("Proper Usage is: java [options, jar file] org.matsim.ScaperMatsim [run | skim] /path/to/config.[xml|yaml]");
                System.exit(0);
            }
        }
    }
}
