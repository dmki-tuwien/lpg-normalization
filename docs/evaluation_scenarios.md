# Evaluation Scenarios

We defined [12 scenarios](#scenarios) on [6 graphs](#graphs) for the evaluation the [graph-native approach to LPG normalization](https://github.com/dmki-tuwien/lpg-normalization/blob/master/paper/extended_version.pdf)

## Graphs
* **London Public Transport**<br> The _London Public Transport_ graph's sources are available on [Zenodo](https://zenodo.org/records/18479732).
  Adapted from [^2], it models the public transport network of London.

* **Northwind**<br>
  The _Northwind_ graph is used in [^1] and is available on [GitHub](https://github.com/neo4j-graph-examples/northwind). It contains the "Northwind Traders" retail data set.

* **No Socks**<br>
  The _No Socks_ graph originates from the motivating example of [^1].

* **Offshore**<br>
  The _Offshore_ graph is used in [^1] and is available on [GitHub](https://github.com/neo4j-graph-examples/northwind). It contains the "The Offshore Leaks Database and guide from the International Consortium of Investigative Journalists (ICIJ)".

* **University**<br>
  The _University_ graph originate from Figure 1a of the
  [graph-native LPG normalization paper](https://github.com/dmki-tuwien/lpg-normalization/blob/master/paper/extended_version.pdf).

* **Train Services**<br>
  The _Train Services_ graph is based on data from [Rijden de Treinen](https://www.rijdendetreinen.nl) and
  models train services performed by different operators that stop at train stations. It is available on [Zenodo](https://zenodo.org/records/18478422).

## Scenarios
Evaluation scenarios combine [graphs](#graphs) with dependency sets. In the following we list the minimal covers (i.e., minimal dependency sets) used for each graph.
The dependencies use an ASCII syntax (see [Grammar](gofd.md#grammar)) for expressing GO-FDs.

###  $S_\text{Lon}$
**Graph:** London Public Transport

**Minimal cover of dependencies:**

*  `(s:Station:zone&zoneOriginal)::s.zoneOriginal=>s.zone`
*  `(s:Station:latitude&longitude)::s.latitude,s.longitude=>s`
*  `(s:Station)-[c:CONNECTED_THROUGH:line&color&type]->()::c.line=>c.color,c.type`

###  $S_\text{Nw}$
**Graph:** Northwind

**Minimal cover of dependencies:**

*  `(o:Order:orderID)::o.orderID=>o`
*  `(o:Order:orderID&orderDate&customerID&shipCity&shipPostalCode&shipCountry&shipAddress&shipRegion)::o.customerID=>o.shipCity,o.shipPostalCode,o.shipCountry,o.shipAddress,o.shipRegion`
    
###  $S_\text{No-1}$
**Graph:** No Socks

**Minimal cover of dependencies:**

*  `(e:Event:company&name&time&venue)::e.company,e.time=>e`
*  `(e:Event:company&name&time&venue)::e.name=>e.company`
*  `(e:Event:company&name&time&venue)::e.name,e.time=>e.venue`
*  `(e:Event:company&name&time&venue)::e.time,e.venue=>e.name`
    
###  $S_\text{No-2}$
**Graph:** No Socks

**Minimal cover of dependencies:**

*  `(e:Event:company&name&time&venue)::e.company,e.time=>e.venue`
*  `(e:Event:company&name&time&venue)::e.name=>e.company`
*  `(e:Event:company&name&time&venue)::e.name,e.time=>e.venue`
*  `(e:Event:company&name&time&venue)::e.time,e.venue=>e.name`
    
###  $S_\text{No-3}$
**Graph:** No Socks

**Minimal cover of dependencies:**

*  `(e:Event&Confirmed:company&name&time&venue)::e.company,e.time=>e`
*  `(e:Event&Confirmed:company&name&time&venue)::e.name=>e.company`
*  `(e:Event&Confirmed:company&name&time&venue)::e.name,e.time=>e.venue`
*  `(e:Event&Confirmed:company&name&time&venue)::e.time,e.venue=>e.name`
*  `(e:Event&Confirmed:company&name&time&venue)::e.name,e.company=>e.time`
    
###  $S_\text{Off-1}$
**Graph:** Offshore

**Minimal cover of dependencies:**

*  `(e:Entity:jurisdiction_description&countries&service_provider&country_codes):: e.countries=>e.country_codes`
*  `(e:Entity:jurisdiction_description&countries&service_provider&country_codes):: e.country_codes=>e.countries`
    
###  $S_\text{Off-2}$
**Graph:** Offshore

**Minimal cover of dependencies:**

*  `(e:Entity:jurisdiction_description&valid_until&countries&sourceID&country_codes):: e.countries,e.jurisdiction_description=>e.country_codes`
*  `(e:Entity:jurisdiction_description&valid_until&countries&sourceID&country_codes):: e.countries,e.sourceID=>e.country_codes`
*  `(e:Entity:jurisdiction_description&valid_until&countries&sourceID&country_codes):: e.countries,e.valid_until=>e.country_codes`
*  `(e:Entity:jurisdiction_description&valid_until&countries&sourceID&country_codes):: e.country_codes,e.sourceID=>e.countries`
*  `(e:Entity:jurisdiction_description&valid_until&countries&sourceID&country_codes):: e.country_codes,e.valid_until=>e.countries`

###  $S_\text{Off-3}$
**Graph:** Offshore

**Minimal cover of dependencies:**

*  `(e:Entity:countries&service_provider&country_codes&jurisdiction_description&sourceID&valid_until):: e.countries=>e.country_codes`
*  `(e:Entity:countries&service_provider&country_codes&jurisdiction_description&sourceID&valid_until):: e.country_codes=>e.countries`
*  `(e:Entity:countries&service_provider&country_codes&jurisdiction_description&sourceID&valid_until):: e.service_provider=>e.sourceID`
*  `(e:Entity:countries&service_provider&country_codes&jurisdiction_description&sourceID&valid_until):: e.sourceID=>e.valid_until`
*  `(e:Entity:countries&service_provider&country_codes&jurisdiction_description&sourceID&valid_until):: e.valid_until=>e.sourceID`
    
###  $S_\text{Ts-1}$
**Graph:** Train Services

**Minimal cover of dependencies:**

*  `()-[t:STOPS_AT:code]->(s:Station:name)::s.name=>t.code`
*  `(ts:TrainService:date&number&type)::ts.number,ts.date=>ts.type`
*  `(ts:TrainService:date&number&operator)-[:STOPS_AT]->()::ts.number,ts.date=>ts.operator`
*  `(ts:TrainService:serviceid)-[:STOPS_AT]->()::ts.serviceid=>ts`
*  `()-[t:STOPS_AT:stopid]->()::t.stopid=>t`
*  `()-[t:STOPS_AT:departure&stopid]->(s)::t.stopid=>s`
    
###  $S_\text{Ts-2}$
**Graph:** Train Services

**Minimal cover of dependencies:**

*  `()-[t:STOPS_AT:code]->(s:Station:name)::s.name=>t.code`
*  `()-[t:STOPS_AT:code]->(s:Station:name)::t.code=>s.name`
*  `(ts:TrainService:date&number&type)::ts.number,ts.date=>ts.type`
*  `(ts:TrainService:date&number&operator)-[:STOPS_AT]->()::ts.number,ts.date=>ts.operator`
*  `(ts:TrainService:serviceid)-[:STOPS_AT]->()::ts.serviceid=>ts`
*  `()-[t:STOPS_AT:stopid]->()::t.stopid=>t`
*  `()-[t:STOPS_AT:departure&stopid]->(s)::t.stopid=>s`
    
###  $S_\text{Uni-1}$
**Graph:** University

**Minimal cover of dependencies:**

*  `(c:Course)<-[t:TEACHES:usingBook]-()::c=>t.usingBook`
    
###  $S_\text{Uni-2}$
**Graph:** University

**Minimal cover of dependencies:**

*  `(c:Course:title)<-[t:TEACHES:usingBook]-()::c.title=>t.usingBook`
    

## Queries

In our query experiment we run in total 17 queries before and after normalization on 4 [scenarios](#scenarios). 
For several queries we used different variants after normalization.


###$S_\text{Lon}$

??? "Query 1"
    #####  Original query

      * `PROFILE MATCH ()-[c:CONNECTED_THROUGH]->() RETURN DISTINCT c.line, c.color`
  
    ##### After normalization

      * `PROFILE MATCH (c:Ccolorclinectype) RETURN DISTINCT c.Cline, c.Ccolor`
      * `PROFILE MATCH ()-[]-(d:CONNECTED_THROUGH)-[]-(), (d)-[]-(c:Ccolorclinectype) RETURN DISTINCT c.Cline, c.Ccolor`

??? "Query 2"
    ##### Original query

      * `PROFILE MATCH (s:Station)-[c:CONNECTED_THROUGH]-() WHERE s.name = "Piccadilly Circus" RETURN DISTINCT c.line`

    ##### After normalization

      * `PROFILE MATCH (s:Station)-[]-(:CONNECTED_THROUGH)-[:CCOLORCLINECTYPE]-(c:Ccolorclinectype) WHERE s.name = "Piccadilly Circus" RETURN DISTINCT c.Cline`

??? "Query 3"
    ##### Original query

    * `PROFILE MATCH (s:Station) WHERE s.zoneOriginal IS NOT NULL RETURN DISTINCT s.zone, s.zoneOriginal`

    ##### After normalization

    * `PROFILE MATCH (s:SzoneszoneOriginal) WHERE s.SzoneOriginal IS NOT NULL RETURN DISTINCT s.Szone, s.SzoneOriginal`
    * `PROFILE MATCH (s:Station)-[]-(s:SzoneszoneOriginal) WHERE s.SzoneOriginal IS NOT NULL RETURN DISTINCT s.Szone, s.SzoneOriginal`

??? "Query 4"
    ##### Original query

    * `PROFILE MATCH (s:Station)-[c:CONNECTED_THROUGH]-(:Station) WHERE s.zone = "6" RETURN DISTINCT c.line`

    ##### After normalization

    * `PROFILE MATCH (s:Station)-[]-(c:CONNECTED_THROUGH)-[]-(:Station), (s)-[]-(z:SzoneszoneOriginal), (c)-[]-(d:Ccolorclinectype) WHERE z.Szone = "6" RETURN DISTINCT d.Cline`

??? "Query 5"
    ##### Original query

    * `PROFILE MATCH (s:Station)-[c:CONNECTED_THROUGH]->(t:Station) WHERE s.name = "Piccadilly Circus" AND c.line = "Bakerloo" RETURN DISTINCT s.name, t.name`

    ##### After normalization

    * `PROFILE MATCH (s:Station)-[]->(c:CONNECTED_THROUGH)-[]->(t:Station), (c)-[]-(d:Ccolorclinectype) WHERE s.name = "Piccadilly Circus" and d.Cline ="Bakerloo" RETURN t.name`

??? "Query 6"
    ##### Original query

    * `PROFILE MATCH ()-[c:CONNECTED_THROUGH]->() WHERE c.line = "Bakerloo" SET c.color = "Rainbow"`

    ##### After normalization

    * `PROFILE MATCH (c:Ccolorclinectype) WHERE c.Cline = "Bakerloo" SET c.Ccolor = "Rainbow"`
    * `PROFILE MATCH (:CONNECTED_THROUGH)-->(c:Ccolorclinectype) WHERE c.Cline = "Bakerloo" SET c.Ccolor = "Rainbow"`
    * `PROFILE MATCH (:CONNECTED_THROUGH)-->(c:Ccolorclinectype) WHERE c.Cline = "Bakerloo" WITH DISTINCT c SET c.Ccolor = "Rainbow"`

###$S_\text{Nw}$

??? "Query 1"
    ##### Original query

    * `PROFILE MATCH (o:Order) RETURN DISTINCT o.orderID, o.customerID`

    ##### After normalization

    * `PROFILE MATCH (o:Order)-[]-(c:OcustomerIDoshipAddressoshipCityoshipCountryoshipPostalCodeoshipRegion) RETURN DISTINCT o.orderID, c.OcustomerID`

??? "Query 2"
    ##### Original query

    * `PROFILE MATCH (o:Order) WHERE o.customerID IS NOT NULL AND o.shipCity IS NOT NULL AND o.shipPostalCode IS NOT NULL AND o.shipCountry IS NOT NULL AND o.shipAddress IS NOT NULL AND o.shipRegion IS NOT NULL RETURN DISTINCT o.customerID`

    ##### After normalization

    * `PROFILE MATCH (o:OcustomerIDoshipAddressoshipCityoshipCountryoshipPostalCodeoshipRegion) WHERE o.OcustomerID IS NOT NULL AND o.OshipCity IS NOT NULL AND o.OshipPostalCode IS NOT NULL AND o.OshipCountry IS NOT NULL AND o.OshipAddress IS NOT NULL AND o.OshipRegion IS NOT NULL RETURN DISTINCT o.OcustomerID`
    * `PROFILE MATCH (:Order)-->(o:OcustomerIDoshipAddressoshipCityoshipCountryoshipPostalCodeoshipRegion) WHERE o.OcustomerID IS NOT NULL AND o.OshipCity IS NOT NULL AND o.OshipPostalCode IS NOT NULL AND o.OshipCountry IS NOT NULL AND o.OshipAddress IS NOT NULL AND o.OshipRegion IS NOT NULL RETURN DISTINCT o.OcustomerID`

??? "Query 3"
    ##### Original query

    * `PROFILE MATCH (o:Order) WHERE o.customerID = "FOLKO" SET o.shipCountry = "Rainbow"`
 
    ##### After normalization

    * `PROFILE MATCH (o:Order)-[]-(c:OcustomerIDoshipAddressoshipCityoshipCountryoshipPostalCodeoshipRegion) WHERE c.OcustomerID = "FOLKO" SET c.OshipCountry = "Rainbow"`
    * `PROFILE MATCH (o:Order)-[]-(c:OcustomerIDoshipAddressoshipCityoshipCountryoshipPostalCodeoshipRegion) WHERE c.OcustomerID = "FOLKO" WITH DISTINCT c SET c.OshipCountry = "Rainbow"`
    * `PROFILE MATCH (c:OcustomerIDoshipAddressoshipCityoshipCountryoshipPostalCodeoshipRegion) WHERE c.OcustomerID = "FOLKO" SET c.OshipCountry = "Rainbow"`




###$S_\text{Off-1}$

??? "Query 1"
        ##### Original query

        * `PROFILE MATCH (e:Entity) WHERE e.countries IS NOT NULL AND e.jurisdiction_description IS NOT NULL AND e.country_codes IS NOT NULL RETURN DISTINCT e.countries, e.country_codes`
        ##### After normalization

        * `PROFILE MATCH (c:EcountriesecountryCodes) WHERE c.Ecountries IS NOT NULL AND c.EcountryCodes IS NOT NULL RETURN DISTINCT c.Ecountries, c.EcountryCodes`
        * `PROFILE MATCH (:Entity)-[]->(c:EcountriesecountryCodes) WHERE c.Ecountries IS NOT NULL AND c.EcountryCodes IS NOT NULL RETURN DISTINCT c.Ecountries, c.EcountryCodes`


??? "Query 2"
    ##### Original query

    * `PROFILE MATCH (e:Entity) WHERE e.countries IS NOT NULL AND e.service_provider IS NOT NULL AND e.country_codes IS NOT NULL RETURN DISTINCT e.countries,e.service_provider, e.country_codes`
    ##### After normalization

    * `PROFILE MATCH (e:Entity)-[]-(c:EcountriesecountryCodes) WHERE c.Ecountries IS NOT NULL AND c.EcountryCodes IS NOT NULL RETURN DISTINCT c.Ecountries, c.EcountryCodes, e.service_provider`

??? "Query 3"
    ##### Original query

    * `PROFILE MATCH (e:Entity) WHERE e.countries IS NOT NULL AND e.jurisdiction_description IS NOT NULL AND e.country_codes IS NOT NULL AND e.countries = "Singapore" SET e.country_codes = "Sp"`
    ##### After normalization

    * `PROFILE MATCH (c:EcountriesecountryCodes) WHERE c.Ecountries IS NOT NULL AND c.EcountryCodes IS NOT NULL AND c.Ecountries = "Singapore" SET c.EcountryCodes = "Sp"`
    * `PROFILE MATCH (:Entity)-[]->(c:EcountriesecountryCodes) WHERE c.Ecountries IS NOT NULL AND c.EcountryCodes IS NOT NULL AND c.Ecountries = "Singapore" SET c.EcountryCodes = "Sp"`
    * `PROFILE MATCH (:Entity)-[]->(c:EcountriesecountryCodes) WHERE c.Ecountries IS NOT NULL AND c.EcountryCodes IS NOT NULL AND c.Ecountries = "Singapore" WITH DISTINCT c SET c.EcountryCodes = "Sp"`





###$S_\text{Ts-2}$

??? "Query 1"
    ##### Original query

    * `PROFILE MATCH ()-[t:STOPS_AT]->(s:Station) WHERE s.name IS NOT NULL AND t.code IS NOT NULL RETURN DISTINCT t.code, s.name`
    ##### After normalization

    * `PROFILE MATCH (n:Snametcode) RETURN DISTINCT n.Sname, n.Tcode`
    * `PROFILE MATCH (s:Station)-->(n:Snametcode), (t:STOPS_AT)-->(n), (t)-->(s) RETURN DISTINCT n.Sname, n.Tcode`

??? "Query 2"
    ##### Original query

    * `PROFILE MATCH (ts:TrainService)-[t:STOPS_AT]->(s:Station) WHERE ts.type CONTAINS "Nightjet" RETURN DISTINCT ts.number, ts.type, t.code`
    ##### After normalization

    * `PROFILE MATCH (ts:TrainService)-->(t:STOPS_AT)-->(s:Station), (ts)-->(d:Tsdatetsnumbertstype), (s)-->(n:Snametcode), (t)-->(n) WHERE d.Tstype CONTAINS "Nightjet" RETURN DISTINCT d.Tsnumber, d.Tstype, n.Tcode`

??? "Query 3"
    ##### Original query

    * `PROFILE MATCH (ts:TrainService) WHERE ts.type CONTAINS "Nightjet" RETURN DISTINCT ts.number, ts.completely_cancelled`
    ##### After normalization

    * `PROFILE MATCH (ts:TrainService)-->(d:Tsdatetsnumbertstype) WHERE d.Tstype CONTAINS "Nightjet" RETURN DISTINCT d.Tsnumber, ts.completely_cancelled`

??? "Query 4"
    ##### Original query

    * `PROFILE MATCH (ts:TrainService) WHERE ts.type CONTAINS "Sprinter" RETURN DISTINCT ts.number, ts.operator`
    ##### After normalization

    * `PROFILE MATCH (ts:TrainService)-->(d:Tsdatetsnumbertstype), (ts)-->(e:Tsdatetsnumbertsoperator) WHERE d.Tstype CONTAINS "Sprinter" RETURN DISTINCT d.Tsnumber, e.Tsoperator`
    * `PROFILE MATCH (ts:TrainService)-->(d:Tsdatetsnumbertstype), (ts)-->(e:Tsdatetsnumbertsoperator) WHERE d.Tstype CONTAINS "Sprinter" RETURN DISTINCT d.Tsnumber, e.Tsoperator`

??? "Query 5"
    ##### Original query

    * `PROFILE MATCH ()-[t:STOPS_AT]->(s:Station) WHERE s.name IS NOT NULL AND t.code IS NOT NULL AND s.name = "Innsbruck Hbf" SET t.code = "Rainbow"`
    ##### After normalization

    * `PROFILE MATCH (n:Snametcode) WHERE n.Sname = "Innsbruck Hbf" SET n.Tcode = "Rainbow"`
    * `PROFILE MATCH (s:Station)-->(n:Snametcode), (t:STOPS_AT)-->(n), (t)-->(s) WHERE n.Sname = "Innsbruck Hbf" SET n.Tcode = "Rainbow"`
    * `PROFILE MATCH (s:Station)-->(n:Snametcode), (t:STOPS_AT)-->(n), (t)-->(s) WHERE n.Sname = "Innsbruck Hbf" WITH DISTINCT n  SET n.Tcode = "Rainbow"`
    

[^1]: Philipp Skavantzos and Sebastian Link. 2025. Third and Boyce-Codd normal
form for property graphs. VLDB J. 34, 2 (2025), 23.

[^2]: <https://github.com/neo4j-partners/neo4j-transport-for-london>