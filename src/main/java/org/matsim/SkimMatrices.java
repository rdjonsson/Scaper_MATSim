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
import java.net.URL;
import java.util.Random;
import java.util.function.BiPredicate;
import java.util.function.Predicate;

import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Link;
import org.matsim.contrib.roadpricing.RoadPricingConfigGroup;
import org.matsim.contrib.roadpricing.RoadPricingModule;
import org.matsim.contrib.roadpricing.RoadPricingSchemeUsingTollFactor;
import org.matsim.contrib.roadpricing.TollFactor;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.controler.Controler;
import org.matsim.core.controler.OutputDirectoryHierarchy;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.utils.io.IOUtils;


import org.matsim.pt.transitSchedule.api.TransitLine;
import org.matsim.pt.transitSchedule.api.TransitRoute;
import org.matsim.pt.transitSchedule.api.TransitScheduleReader;

import ch.sbb.matsim.analysis.skims.CalculateSkimMatrices;

public class SkimMatrices {

    public static void main(String[] args)  throws IOException {

        String zonesShapeFilename = "/home/danjo/scenarios/sthlm/deso_sthlm.shp";
        String zonesIdAttributeName = "ID";
        String outputDirectory = "/home/danjo/scenarios/sthlm/matsim/deso_osm/";
        int numberOfThreads = 5;

        String networkFilename = "/home/danjo/scenarios/sthlm/matsim/matsim-network.xml.gz";
        int numberOfPointsPerZone = 3;
        Random r = new Random();

        String transitScheduleFilename = "/home/danjo/scenarios/sthlm/matsim/transitSchedule.xml.gz";
        String transitNetworkFilename =  "/home/danjo/scenarios/sthlm/matsim/transitNetwork.xml.gz";
        Config config = ConfigUtils.createConfig();

        double[] mpeak = new double[2];
        mpeak[0] = 28800;
        mpeak[1] = 32400;

        double[] midday = new double[2];   
        midday[0] = 39600;
        midday[1] = 43200;

        CalculateSkimMatrices skims = new CalculateSkimMatrices(outputDirectory, numberOfThreads);
        //skims.calculateSamplingPointsPerZoneFromFacilities(facilitiesFilename, numberOfPointsPerZone, r, facility -> 1.0);
        // alternative if you don't have facilities:
        skims.calculateSamplingPointsPerZoneFromNetwork(networkFilename, numberOfPointsPerZone,zonesShapeFilename,zonesIdAttributeName, r);
        
        
        // Morning peak
        skims.calculateAndWriteNetworkMatrices(networkFilename, null, mpeak, config, "mpeak_", l -> true);
        skims.calculateAndWritePTMatrices(transitNetworkFilename, transitScheduleFilename, mpeak[0], mpeak[1], config, "mpeak_", (line, route) -> route.getTransportMode().equals("train"));

        // Midday
        skims.calculateAndWriteNetworkMatrices(networkFilename, null, midday, config, "midday_", l -> true);
        skims.calculateAndWritePTMatrices(transitNetworkFilename, transitScheduleFilename, midday[0], midday[1], config, "midday_", (line, route) -> route.getTransportMode().equals("train"));
        
        skims.calculateAndWriteBeelineMatrix();


    }
}
