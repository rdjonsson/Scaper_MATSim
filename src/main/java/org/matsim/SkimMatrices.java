/* *********************************************************************** *
 * project: org.matsim.*												   *
 *                                                                         *
 * *********************************************************************** *
 *                                                                         *
 * copyright       : (C) 2008 by the members listed in the COPYING,        *
 *                   LICENSE and WARRANTY file.                            *
 * email           : info at matsim dot org                                *
 *                                                                         *
 * *********************************************************************** *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *   See also COPYING, LICENSE and WARRANTY file                           *
 *                                                                         *
 * *********************************************************************** */
package org.matsim;


import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;


import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Network;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.network.NetworkUtils;
import org.matsim.core.network.io.MatsimNetworkReader;
import org.matsim.utils.gis.matsim2esri.network.Links2ESRIShape;

import org.yaml.snakeyaml.*;

import ch.sbb.matsim.analysis.skims.CalculateSkimMatrices;

public class SkimMatrices {

    public static void Run(String configYaml)  throws IOException {

        Yaml yaml = new Yaml();
        InputStream inputStream = Files.newInputStream(Paths.get(configYaml));
        
        Map<String, Object> conf = yaml.load(inputStream);
        System.out.println(conf);

        String zonesShapeFilename = (String)conf.get("zonesShapeFilename");
        String zonesIdAttributeName = (String)conf.get("zonesIdAttributeName");
        String outputDirectory = (String)conf.get("outputDirectory");
        int numberOfThreads = (int)conf.get("numberOfThreads");

        String networkFilename = (String)conf.get("networkFilename");
        String cleanedNetwork =  (String)conf.get("cleanedNetwork");
        int numberOfPointsPerZone = 5;
        Random r = new Random();

        String transitScheduleFilename = (String)conf.get("transitScheduleFilename");
        String transitNetworkFilename =  (String)conf.get("transitNetworkFilename");
        Config config = ConfigUtils.createConfig();

        double[] mpeak = new double[2];
        mpeak[0] = 27000;
        mpeak[1] = 32400;

        double[] midday = new double[2];   
        midday[0] = 37800;
        midday[1] = 43200;

        final Scenario scenario = ScenarioUtils.createScenario(ConfigUtils.createConfig());
        final Network network = scenario.getNetwork();
        new MatsimNetworkReader(scenario.getNetwork()).readFile(networkFilename);
        Set<String> modes = NetworkUtils.getModes(network);
        NetworkUtils.cleanNetwork(network, modes);
        NetworkUtils.writeNetwork(network, cleanedNetwork);
        
        
        CalculateSkimMatrices skims = new CalculateSkimMatrices(outputDirectory, numberOfThreads);
        //skims.calculateSamplingPointsPerZoneFromFacilities(facilitiesFilename, numberOfPointsPerZone, r, facility -> 1.0);
        // alternative if you don't have facilities:
        skims.calculateSamplingPointsPerZoneFromNetwork(cleanedNetwork, numberOfPointsPerZone,zonesShapeFilename,zonesIdAttributeName, r);
        
        
        // Morning peak
        skims.calculateAndWriteNetworkMatrices(cleanedNetwork, null, mpeak, config, "mpeak_", l -> true);
        skims.calculateAndWritePTMatrices(transitNetworkFilename, transitScheduleFilename, mpeak[0], mpeak[1], config, "mpeak_", (line, route) -> route.getTransportMode().equals("train"));

        // Midday
        skims.calculateAndWriteNetworkMatrices(cleanedNetwork, null, midday, config, "midday_", l -> true);
        skims.calculateAndWritePTMatrices(transitNetworkFilename, transitScheduleFilename, midday[0], midday[1], config, "midday_", (line, route) -> route.getTransportMode().equals("train"));
        
        skims.calculateAndWriteBeelineMatrix();

        final Scenario scenario2 = ScenarioUtils.createScenario(ConfigUtils.createConfig());
        final Network transitnet = scenario2.getNetwork();
        new MatsimNetworkReader(scenario2.getNetwork()).readFile(transitNetworkFilename);

        new Links2ESRIShape(transitnet, "/home/danjo/scenarios/ume/matsim/transitNetwork.shp", "EPSG:3006").write();
    }
}
