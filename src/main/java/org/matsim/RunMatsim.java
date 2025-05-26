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


import java.net.URL;
import java.nio.file.*;

import org.matsim.api.core.v01.Scenario;
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

import ch.sbb.matsim.mobsim.qsim.SBBTransitModule;
import ch.sbb.matsim.mobsim.qsim.pt.SBBTransitEngineQSimModule;
import ch.sbb.matsim.routing.pt.raptor.SwissRailRaptorModule;


public class RunMatsim {

    public static void main(String[] args) {

        Config config;
        if (args == null || args.length == 0 || args[0] == null) {
            System.out.println("Proper Usage is: java [options, jar file] org.matsim.RunMatsim /path/to/config.xml");
            System.exit(0);
        } else {
            config = ConfigUtils.loadConfig(args);

            config.controller().setOverwriteFileSetting((OutputDirectoryHierarchy.OverwriteFileSetting.deleteDirectoryIfExists));

            var configDir = Paths.get(args[0]).getParent();
            
            var cordonFile = Paths.get(configDir.toString(), "cordonToll.xml");

            System.out.println("Cordon file: " + cordonFile.toString());

            var runRoadPricing = Files.exists(cordonFile);

            //load config into scenario
            final Scenario scenario = ScenarioUtils.loadScenario(config);
            Controler controler = new Controler(scenario);

            if(runRoadPricing)
            {
                //add RoadPricing ConfigGroup
                RoadPricingConfigGroup rpConfig = ConfigUtils.addOrGetModule(config, RoadPricingConfigGroup.class);
                rpConfig.setTollLinksFile("cordonToll.xml");


                // define the toll factor as an anonymous class.  If more flexibility is needed, convert to "full" class.
                TollFactor tollFactor = (personId, vehicleId, linkId, time) -> {
                    if(scenario.getVehicles().getVehicles().get(vehicleId) == null){
                        return 0;
                        } else if (scenario.getVehicles().getVehicles().get(vehicleId).getType().getNetworkMode().equals("car")) {
                            return 1;
                        } else {
                            return 0;
                        }
                    };

                // instantiate the road pricing scheme, with the toll factor inserted:
                URL roadpricingUrl;
                roadpricingUrl = IOUtils.extendUrl(config.getContext(), rpConfig.getTollLinksFile());
                RoadPricingSchemeUsingTollFactor stuff = RoadPricingSchemeUsingTollFactor.createAndRegisterRoadPricingSchemeUsingTollFactor(roadpricingUrl, tollFactor, scenario);
                controler.addOverridingModule( new RoadPricingModule( stuff ) );
            }
            // To use the deterministic pt simulation (Part 1 of 2):
            controler.addOverridingModule(new SwissRailRaptorModule());

//           	controler.getConfig().transit().setUseTransit(true);
//		    controler.getConfig().transit().setUsingTransitInMobsim(true);
            
            controler.run();
        }
    }
}
