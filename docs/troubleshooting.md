# Troubleshooting

* **The evaluation crashes because its unable to connect to Memgraph.**<br>
  When running on Linux it may be necessary to remove all environment variables with the key `TC_HOST` from the file `docker-compose.yml`.
* **The evaluation crashes because the Neo4j container was not responsive after 120 seconds.**<br>
  When the Neo4j container tries to load a graph that is not available it crashes. Please check whether all graphs defined in the file `setup.yaml` are in place in the folder `graphs`.