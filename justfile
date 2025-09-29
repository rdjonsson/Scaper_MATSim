homedir := '/home/danjo/'
tmpdir := homedir + 'tmp/'

scenariodir := homedir + 'scenarios/ume/'
matsimconfig := scenariodir + 'matsim/matsim-config-sbb.xml'

scaperdir := homedir + 'projects/Scaper2/source/Scaper'

build:
    mvn compile
    mvn package

run-matsim:
    java -jar scaper-matsim-0.1.jar org.matsim.RunMatsim {{matsimconfig}}