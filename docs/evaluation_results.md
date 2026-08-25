# Evaluation Results


<div id="loading" style="padding: 1rem; background: #f0f4f8; border-radius: 4px;">
  Loading and querying <a href="https://duckdb.org/docs/lts/clients/wasm/overview">DuckDB</a>.
</div>

<div id="duckdb-content" hidden>
<p>Evaluation last run at <span id="session-finished"></span> (ID: <span id="session-id"></span>), with <span id="no-of-runs">X</span> runs.</p>

  <div class="chart-box">
    <div id="db-menu"></div>
    <div id="method-menu"></div>
    <div id="subset-menu"></div>
    <div id="graph-menu"></div>
    <h3>Per-graph metrics</h3>
    <a id="download-csv-per-graph">Download as CSV</a>
    <div id="per-graph-metric-plot"></div>

    <h3>Per-dependency metrics</h3>
    <a id="download-csv-per-dep">Download as CSV</a>
    <div id="per-dep-metric-plot"></div>
    
    <h3>Query performance metrics</h3>
    <a href="https://github.com/dmki-tuwien/lpg-normalization/raw/refs/heads/master/out/query_aggregated_classified.csv">Download as CSV<a/>
  </div>

  <p style="font-size: small">
The visualization utilizes <a href="https://idl.uw.edu/mosaic/vgplot/?lang=js">Mosaic vgplot</a>
and <a href="https://duckdb.org/docs/lts/clients/wasm/overview">DuckDB</a>. 
The data the visualizations are based on are available in the form of a DuckDB on <a href="https://github.com/dmki-tuwien/lpg-normalization/blob/master/out/eval_results.duckdb">GitHub</a>.
</p>
</div>

  <script type="module">
import * as vg from 'https://cdn.jsdelivr.net/npm/@uwdata/vgplot@0.10/+esm';
import * as duckdb from 'https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm/+esm';

    async function buildDashboard() {
      const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();
      const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);
      const worker = await duckdb.createWorker(bundle.mainWorker);
      const logger = new duckdb.ConsoleLogger();
      const db = new duckdb.AsyncDuckDB(logger, worker);
      await db.instantiate(bundle.mainModule);

      // Fetch and register your .duckdb database file
      const dbUrl = 'https://raw.githubusercontent.com/dmki-tuwien/lpg-normalization/refs/heads/master/out/eval_results.duckdb';
      const response = await fetch(dbUrl);
      const buffer = new Uint8Array(await response.arrayBuffer());
      await db.registerFileBuffer('eval_results.duckdb', buffer);

      const conn = await db.connect();
      await conn.query(`ATTACH 'eval_results.duckdb' AS eval_db; USE eval_db;`);

      await conn.query(`
        CREATE VIEW current_per_graph_metric AS SELECT *  FROM per_graph_metric WHERE session_id = ( SELECT DISTINCT session_id FROM per_graph_metric WHERE  timestamp = (SELECT max(timestamp) FROM per_graph_metric));
        CREATE VIEW current_per_dep_metric AS SELECT *  FROM per_dep_metric WHERE session_id = ( SELECT DISTINCT session_id FROM per_dep_metric WHERE  timestamp = (SELECT max(timestamp) FROM per_dep_metric));
      `);

      const connector = vg.wasmConnector({ 
        duckdb,          
        connection: conn 
      });
      
      const sessionInfoResult = await conn.query(`SELECT DISTINCT session_id, MAX(timestamp) as t, COUNT(distinct run_id) as runs FROM per_graph_metric WHERE session_id = ( SELECT DISTINCT session_id FROM per_dep_metric WHERE  timestamp = (SELECT max(timestamp) FROM per_dep_metric)) GROUP BY session_id`);
      const sessionFinished = document.getElementById('session-finished');
      const sessionId = document.getElementById('session-id');
      const sessionData = sessionInfoResult.toArray().map(row => row.toJSON());
      sessionFinished.innerHTML = new Date(sessionData[0].t).toLocaleString();
      const currentSession = sessionData[0].session_id;
      sessionId.innerHTML = currentSession;
      document.getElementById("no-of-runs").innerHTML = sessionData[0].runs;

      // Set the connector using databaseConnector (NOT databaseClient)
      const coordinator = vg.coordinator();
      coordinator.databaseConnector(connector);


      // Create a Selection state for interactive filtering
      const $filter = vg.Selection.crossfilter();


      const dbResult = await conn.query(`SELECT DISTINCT database FROM current_per_graph_metric`);
      const methodResult = await conn.query(`SELECT DISTINCT normalization_method FROM current_per_graph_metric`);
      const subsetResult = await conn.query(`SELECT DISTINCT subset FROM current_per_graph_metric ORDER BY subset`);

      const dbOptions = dbResult.toArray().map(row => row.database);
      const methodOptions = methodResult.toArray().map(row => row.normalization_method);
      const subsetOptions = subsetResult.toArray().map(row => row.subset);

      
      // Build the menus 
      const dbDropdown = vg.menu({
        label: 'Database: ',
        column: 'database',
        options: dbOptions, 
        as: $filter,
        value: dbOptions[0] 
      });
      
      const methodDropdown = vg.menu({
        label: 'Method: ',
        column: 'normalization_method',
        options: methodOptions, 
        as: $filter,
        value: methodOptions[0] 
      });

      const subsetDropdown = vg.menu({
        label: 'Subset of dependencies: ',
        column: 'subset',
        options: subsetOptions, 
        as: $filter,
        value: subsetOptions[0] 
      });

      const graphDropdown = vg.menu({
        label: 'Scenario: ',
        from: 'current_per_graph_metric',
        column: 'graph',
        as: $filter
      });

      const per_graph_metric_plot = vg.plot(
        vg.barY(
          vg.from('current_per_graph_metric', { filterBy: $filter }), 
          { x: 'metric', y: vg.avg('value'), fx: 'graph', fill: "#009485" , tip: true}
        ),
        vg.yScale('symlog'),
        vg.marginLeft(60), 
        vg.marginBottom(100), 
        vg.marginTop(50),
        vg.yTicks([0, 1, 10, 100, 1000, 10000, 100000, 1000000]),
        vg.xTickRotate(-45),
        vg.width(768),
        vg.height(350)
      );

      const per_dep_metric_plot = vg.plot(
        vg.barY(
          vg.from('current_per_dep_metric', { filterBy: $filter }), 
          { x: 'metric', y: vg.avg('value'), fx: 'graph', fill: "#009485" , tip: true}
        ),
        vg.yScale('symlog'),
        vg.marginLeft(60), 
        vg.marginBottom(100), 
        vg.marginTop(50),
        vg.yTicks([0, 1, 10, 100, 1000, 10000, 100000, 1000000]),
        vg.xTickRotate(-45),
        vg.width(768),
        vg.height(350)
      );

      // Mount elements to DOM
      document.getElementById('db-menu').appendChild(dbDropdown);
      document.getElementById('method-menu').appendChild(methodDropdown);
      document.getElementById('subset-menu').appendChild(subsetDropdown);

      document.getElementById('graph-menu').appendChild(graphDropdown);

      document.getElementById('per-graph-metric-plot').appendChild(per_graph_metric_plot);
      document.getElementById('per-dep-metric-plot').appendChild(per_dep_metric_plot);

      
      document.getElementById('download-csv-per-graph').addEventListener('click', async () => {
        const selectedDb = dbDropdown.querySelector('select').value;
        const selectedMethod = methodDropdown.querySelector('select').value;
        
        const virtualFileName = 'filtered_export.csv';
      
        await conn.query(`
          COPY (
            SELECT * FROM current_per_graph_metric 
            WHERE database = '${selectedDb}' 
              AND normalization_method = '${selectedMethod}'
          ) TO '${virtualFileName}' (HEADER, FORMAT CSV);
        `);
      
        const buffer = await db.copyFileToBuffer(virtualFileName);
      
        // Create a Blob and trigger a download
        const blob = new Blob([buffer], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        // Dynamically name the file based on the filters!
        link.download = `per_graph_metrics_${selectedDb}_${selectedMethod}.csv`; 
        
        document.body.appendChild(link);
        link.click();
        
        // Cleanup the DOM and memory
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      });


      document.getElementById('download-csv-per-dep').addEventListener('click', async () => {
        const selectedDb = dbDropdown.querySelector('select').value;
        const selectedMethod = methodDropdown.querySelector('select').value;
        
        const virtualFileName = 'filtered_export.csv';
      
        await conn.query(`
          COPY (
            SELECT * FROM current_per_dep_metric 
            WHERE database = '${selectedDb}' 
              AND normalization_method = '${selectedMethod}'
          ) TO '${virtualFileName}' (HEADER, FORMAT CSV);
        `);
      
        // Extract the file from WASM memory into a standard JavaScript buffer
        const buffer = await db.copyFileToBuffer(virtualFileName);
      
        // Create a Blob and trigger a download
        const blob = new Blob([buffer], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        // Dynamically name the file based on the filters!
        link.download = `per_dependency_metrics_${selectedDb}_${selectedMethod}.csv`; 
        
        document.body.appendChild(link);
        link.click();
        
        // Cleanup the DOM and memory
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      });
      document.getElementById('duckdb-content').hidden = false;
      document.getElementById('loading').hidden = true;
    }

    buildDashboard();
  </script>


