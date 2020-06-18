=======
RoadMap
=======

- Backup facilities for measurement database
- Importing and exporting configuration
- Importing and exporting measurements (csv, xml, json)
- Distinquish between different types of measurements

  - Continuous / incident measurements, measure each
    detection event separately optionally with its
    energy.
  - Aggregated measurements, such as CPM or uSv/h.

- Support different units for measurements

  - CPM / CPS
  - Becquerel (Activity)
  - Coulumb per kilogram (Exposure)
  - Gray (Absorbed dose)
  - Sievert (Equivalent dose)

Some units will make less sense or no sense to record. For instance for a
device put in place to measure background radiation it won't make sense to
measure DPS (Becquerel) as the distance from the source as well as the type of
source are unknown. Other devices such as a CPAM will very likely require much
more complicated database types for storing data.

- Allow to identify between types of devices

  - Geiger counter
  - Proportional counter
  - Ionization chamber
  - CPAM
  - Dosimeter
  - Scintillation counter
