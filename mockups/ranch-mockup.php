<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>H-RIP Ranch Mockup</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=Montserrat:wght@500;600&display=swap" rel="stylesheet">
  <script src="../Leaflet/ranches.js"></script>
  <script src="../plotly-2.24.1.min.js"></script>
  <style>
    :root {
      --bg: #f6f5f0;
      --surface: #ffffff;
      --surface-2: #f1f3ee;
      --ink: #1c2420;
      --ink-2: #4f5b54;
      --ink-3: #7c8781;
      --line: #e4e7e0;
      --brand: #1f5b3f;
      --brand-2: #2f7a55;
      --brand-soft: #e3efe7;
      --accent: #c9822f;
      --radius: 16px;
      --shadow: 0 1px 2px rgba(20,30,25,.05), 0 6px 20px rgba(20,30,25,.05);
      --maxw: 1200px;
      /* data colours: strong = observed, soft = monthly average */
      --rain: #2f6fb3; --rain-soft: #cddff1;
      --temp: #c4573a; --temp-soft: #f2d5cb;
      --veg: #2f7a55;  --veg-soft: #cfe5d7;
      --enso-nina: #2f5fa8; --enso-neutral: #9aa19d; --enso-nino: #b8343f;
      --good: #2f7a55; --bad: #b8343f;
    }
    * { box-sizing: border-box; }
    [hidden] { display: none !important; }
    html { scroll-behavior: smooth; scroll-padding-top: 120px; }
    body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 'Lato', sans-serif; -webkit-font-smoothing: antialiased; }
    a { color: var(--brand-2); }
    img { max-width: 100%; display: block; }
    .wrap { max-width: var(--maxw); margin: 0 auto; padding: 0 24px; }
    h1, h2, h3 { font-weight: 700; margin: 0; }
    .num { font-variant-numeric: tabular-nums; }

    /* ---------- Site header ---------- */
    .site-header { position: sticky; top: 0; z-index: 1000; background: rgba(255,255,255,.94); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }
    .nav { display: flex; align-items: center; justify-content: space-between; gap: 12px; height: 60px; }
    .brand { text-decoration: none; color: var(--ink); font-family: 'Montserrat', sans-serif; font-weight: 600; font-size: 15px; line-height: 1.15; }
    .beta { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 99px; border: 1px solid currentColor; opacity: .7; margin-left: 4px; vertical-align: 2px; }
    .nav-links { display: flex; gap: 6px; list-style: none; margin: 0; padding: 0; }
    .nav-links a { color: var(--ink); text-decoration: none; font-size: 14.5px; padding: 8px 14px; border-radius: 99px; }
    .nav-links a:hover { background: var(--surface-2); }
    .nav-links .cta { background: var(--brand); color: #fff; }

    /* ---------- Page title + section nav ---------- */
    .page-title { padding: 28px 0 0; }
    .crumbs { font-size: 13.5px; color: var(--ink-3); }
    .crumbs a { color: var(--ink-2); text-decoration: none; }
    .crumbs a:hover { text-decoration: underline; }
    .title-row { display: flex; align-items: baseline; flex-wrap: wrap; gap: 4px 14px; margin-top: 2px; }
    .title-row h1 { font-size: clamp(30px, 4vw, 40px); letter-spacing: -.01em; }
    .title-row .meta { color: var(--ink-2); font-size: 15px; }
    .subnav { position: sticky; top: 60px; z-index: 900; background: rgba(246,245,240,.95); backdrop-filter: blur(10px); margin-top: 14px; border-bottom: 1px solid var(--line); }
    .subnav ul { display: flex; gap: 22px; list-style: none; margin: 0; padding: 0; overflow-x: auto; scrollbar-width: none; }
    .subnav ul::-webkit-scrollbar { display: none; }
    .subnav a { display: block; white-space: nowrap; text-decoration: none; color: var(--ink-3); font-size: 14px; font-weight: 700; padding: 12px 0 10px; border-bottom: 2px solid transparent; }
    .subnav a:hover { color: var(--ink); }
    .subnav a.active { color: var(--brand); border-bottom-color: var(--brand); }

    /* ---------- Layout ---------- */
    section.block { padding-top: 44px; }
    .section-head { margin-bottom: 16px; }
    .section-head h2 { font-size: clamp(22px, 2.4vw, 28px); }
    .section-head p { margin: 4px 0 0; color: var(--ink-2); font-size: 15px; }
    .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 18px; }
    .stack { display: flex; flex-direction: column; gap: 18px; min-width: 0; }
    .span-4 { grid-column: span 4; } .span-5 { grid-column: span 5; } .span-6 { grid-column: span 6; } .span-7 { grid-column: span 7; } .span-8 { grid-column: span 8; } .span-12 { grid-column: span 12; }
    .card { background: var(--surface); border-radius: var(--radius); box-shadow: var(--shadow); padding: 20px; display: flex; flex-direction: column; min-width: 0; position: relative; }
    .card-head { display: flex; justify-content: space-between; align-items: start; gap: 12px; margin-bottom: 10px; }
    .card h3 { font-size: 16px; }
    .sub { font-size: 13px; color: var(--ink-3); }

    /* ---------- Dashboard: original layout, one panel ---------- */
    .dash { background: var(--surface); border-radius: var(--radius); box-shadow: var(--shadow); }
    .dash-head { padding: 14px 22px; border-bottom: 1px solid var(--line); }
    .dash-head h2 { font-size: 19px; }
    .dash-grid { display: grid; grid-template-columns: repeat(12, 1fr); }
    .cell { position: relative; padding: 20px 22px; min-width: 0; display: flex; flex-direction: column; }
    .c-half { grid-column: span 6; } .c-chart { grid-column: span 8; } .c-side { grid-column: span 4; padding: 0; }
    .c-half:first-child { border-right: 1px solid var(--line); }
    .c-chart { border-top: 1px solid var(--line); border-right: 1px solid var(--line); }
    .c-side { border-top: 1px solid var(--line); }
    .c-side .cell + .cell { border-top: 1px solid var(--line); }
    .mcell { display: grid; grid-template-columns: 132px 1fr; gap: 20px; align-items: center; }
    .m-id { display: flex; flex-direction: column; align-items: center; gap: 10px; text-align: center; }
    .m-id .name { font-weight: 700; font-size: 16px; }
    .m-icon { width: 50px; height: 50px; border-radius: 50%; display: grid; place-items: center; color: #fff; }
    .m-icon svg { width: 26px; height: 26px; }
    .m-body { min-width: 0; padding-right: 30px; }
    .m-date { font-size: 13px; font-weight: 700; color: var(--ink-3); margin-bottom: 8px; }
    .m-vals { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .m-val { background: var(--surface-2); border-radius: 12px; padding: 12px 14px; text-align: center; }
    .m-val .v { font-size: 26px; font-weight: 900; line-height: 1.15; font-variant-numeric: tabular-nums; }
    .m-val .v small { font-size: 15px; font-weight: 700; color: var(--ink-2); margin-left: 2px; }
    .m-val .v .d { font-size: 14px; font-weight: 700; margin-left: 6px; }
    .m-val .k { font-size: 13.5px; color: var(--ink-2); }
    .m-val .s { margin-top: 6px; font-size: 13px; color: var(--ink-2); }
    .cell h3 { font-size: 16px; padding-right: 36px; }
    .seg { display: inline-flex; background: var(--surface-2); padding: 3px; border-radius: 99px; }
    .seg button { font: inherit; font-size: 12.5px; font-weight: 700; border: 0; background: none; color: var(--ink-2); padding: 5px 11px; border-radius: 99px; cursor: pointer; }
    .seg button[aria-pressed="true"] { background: var(--surface); color: var(--ink); box-shadow: 0 1px 2px rgba(0,0,0,.1); }
    .enso-text { text-align: center; font-size: 14px; color: var(--ink-2); margin: 4px 0 12px; line-height: 1.45; }
    .enso-text b { color: var(--ink); font-size: 16px; }
    .up { color: var(--good); } .down { color: var(--bad); } .neutral { color: var(--ink-2); }

    /* Status pills: icon + label, never colour alone */
    .status { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 700; padding: 3px 10px 3px 7px; border-radius: 99px; }
    .status svg { width: 15px; height: 15px; flex: none; }
    .status.good { background: #e3efe7; color: var(--good); }
    .status.warn { background: #fbefd9; color: #8a5a06; }
    .status.bad { background: #f7e1e3; color: var(--bad); }
    .status.big { font-size: 16px; padding: 7px 14px 7px 10px; }
    .status.big svg { width: 18px; height: 18px; }

    /* Info button + popover */
    .info-wrap { position: absolute; top: 16px; right: 16px; z-index: 5; }
    .info { width: 28px; height: 28px; border-radius: 50%; border: 1px solid var(--line); background: var(--surface); color: var(--ink-3); cursor: pointer; font-weight: 700; font-size: 13px; font-family: Georgia, serif; font-style: italic; }
    .info:hover, .info[aria-expanded="true"] { background: var(--brand-soft); color: var(--brand); border-color: var(--brand-soft); }
    .popover { display: none; position: absolute; right: 0; top: calc(100% + 8px); z-index: 50; width: 280px; background: var(--ink); color: #fff; font-size: 13px; line-height: 1.5; padding: 12px 14px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,.18); }
    .popover.open { display: block; }
    .popover p { margin: 0 0 6px; } .popover p:last-child { margin: 0; }
    .popover table { width: 100%; border-collapse: collapse; }
    .popover td { padding: 2px 0; }
    .popover a { color: #9fd8b8; font-weight: 600; }

    /* Drought + ENSO */
    .chart { height: 320px; }
    .chart.sm { height: 260px; }
    .chart.hist { height: 340px; }
    .chart-card.span-7 .chart { flex: 1 1 auto; min-height: 320px; height: auto; }
    .gauge-img { max-width: 220px; margin: 8px auto 0; }
    .phase { text-align: center; margin: 4px 0 12px; }
    .phase-name { display: inline-flex; align-items: center; gap: 8px; font-size: 17px; font-weight: 700; }
    .phase-name i { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .mini-cap { font-size: 12px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--ink-3); margin-bottom: 2px; }
    .mini-table { width: 100%; border-collapse: collapse; font-size: 14px; }
    .mini-table td { padding: 6px 0; border-top: 1px solid var(--line); }
    .mini-table td:last-child { text-align: right; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }

    /* ---------- Climate sections (stat cards + map | chart) ---------- */
    .stat-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
    .stat-card { text-align: center; align-items: center; justify-content: center; gap: 4px; }
    .stat-card .v { font-size: 30px; font-weight: 900; line-height: 1.1; font-variant-numeric: tabular-nums; }
    .stat-card .v small { font-size: 16px; font-weight: 700; color: var(--ink-2); }
    .stat-card .k { font-size: 14px; color: var(--ink-2); }
    .stat-card .d { font-size: 14px; font-weight: 700; }
    .stat-card .when { font-size: 12.5px; color: var(--ink-3); margin-top: 6px; }
    .stat-card .row { display: flex; gap: 18px; justify-content: center; }
    .map-card { padding: 10px; }
    .map-card a { display: block; border-radius: 10px; overflow: hidden; }
    .map-card img { width: 100%; height: auto; }
    .map-card .cap { font-size: 12.5px; color: var(--ink-3); text-align: center; padding-top: 6px; }
    .legend-row { display: flex; flex-wrap: wrap; gap: 4px 16px; font-size: 12.5px; color: var(--ink-2); }
    .legend-row span { display: inline-flex; align-items: center; gap: 6px; }
    .legend-row i { width: 12px; height: 10px; border-radius: 3px; display: inline-block; }
    .legend-row i.ln { height: 3px; border-radius: 2px; }
    .chart-card .card-head { align-items: center; }
    .card-foot { display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 8px; font-size: 13px; }
    .card-foot a { color: var(--ink-2); font-weight: 700; }
    .desc { font-size: 14px; color: var(--ink-2); }
    .desc p { margin: 0; }

    /* Forage tool */
    .tool-form { display: flex; flex-wrap: wrap; gap: 14px; align-items: end; }
    .field { display: grid; gap: 6px; font-size: 13px; font-weight: 700; color: var(--ink-2); }
    .field select { font: inherit; font-size: 15px; font-weight: 400; color: var(--ink); padding: 10px 36px 10px 12px; border: 1px solid var(--line); border-radius: 10px; background: var(--surface) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%237c8781' stroke-width='2'/%3E%3C/svg%3E") right 12px center no-repeat; appearance: none; min-width: 200px; }
    .btn { font: inherit; font-size: 15px; font-weight: 700; border: 0; border-radius: 99px; padding: 11px 22px; background: var(--brand); color: #fff; cursor: pointer; }
    .btn:hover { background: var(--brand-2); }
    #toolResults { margin-top: 18px; overflow-x: auto; }
    #toolResults:empty { display: none; }
    #toolResults table { border-collapse: collapse; width: 100%; font-size: 14px; font-variant-numeric: tabular-nums; }
    #toolResults th, #toolResults td { padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: center; }
    #toolResults .msg { color: var(--ink-2); background: var(--surface-2); padding: 12px 14px; border-radius: 10px; font-size: 14px; }

    /* Footer */
    footer { margin-top: 72px; background: #14231b; color: #c9d3cd; padding: 44px 0 26px; }
    .foot-grid { display: grid; grid-template-columns: 1.2fr 2fr; gap: 48px; }
    footer h4 { color: #fff; font-size: 13px; letter-spacing: .1em; text-transform: uppercase; margin: 0 0 14px; font-weight: 600; }
    footer a { color: #fff; }
    footer p { margin: 0 0 10px; font-size: 14.5px; }
    .partners { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
    .partners div { background: #fff; border-radius: 12px; height: 76px; display: grid; place-items: center; padding: 12px; }
    .partners img { max-height: 52px; width: auto; object-fit: contain; }
    .legal { margin-top: 36px; padding-top: 18px; border-top: 1px solid rgba(255,255,255,.1); font-size: 13px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; color: #8fa097; }

    /* ---------- Responsive ---------- */
    @media (max-width: 1000px) {
      .span-4, .span-5, .span-6, .span-7, .span-8 { grid-column: span 12; }
      .c-half, .c-chart { grid-column: span 12; }
      .c-half:first-child { border-right: 0; } .c-half + .c-half { border-top: 1px solid var(--line); } .c-chart { border-right: 0; }
      .c-side { grid-column: span 12; display: grid; grid-template-columns: 1fr 1fr; }
      .c-side .cell + .cell { border-top: 0; border-left: 1px solid var(--line); }
    }
    @media (max-width: 680px) {
      html { scroll-padding-top: 104px; }
      .wrap { padding: 0 16px; }
      .nav { height: 56px; }
      .subnav { top: 56px; }
      .subnav ul { gap: 18px; }
      .nav-links li:not(:last-child) { display: none; }
      .nav-links a { white-space: nowrap; padding: 8px 12px; font-size: 13.5px; }
      .brand { font-size: 13.5px; }
      .page-title { padding-top: 18px; }
      section.block { padding-top: 34px; }
      .grid, .stack, .stat-pair { gap: 14px; }
      .card { padding: 16px; }
      .dash-head { padding: 14px 16px; }
      .cell { padding: 16px; }
      .mcell { grid-template-columns: 1fr; gap: 12px; }
      .m-id { flex-direction: row; text-align: left; padding-right: 44px; }
      .m-icon { width: 38px; height: 38px; } .m-icon svg { width: 20px; height: 20px; }
      .m-id .seg { margin-left: auto; }
      .m-body { padding-right: 0; }
      .m-val .v { font-size: 22px; }
      .c-side { grid-template-columns: 1fr; }
      .c-side .cell + .cell { border-left: 0; border-top: 1px solid var(--line); }
      .chart { height: 270px; } .chart.hist { height: 300px; } .chart-card.span-7 .chart { min-height: 270px; }
      .stat-card .v { font-size: 26px; }
      .info { width: 36px; height: 36px; font-size: 15px; }
      .info-wrap { top: 12px; right: 12px; }
      .popover { width: min(280px, calc(100vw - 56px)); }
      .field, .field select { width: 100%; }
      .tool-form .btn { width: 100%; }
      .foot-grid { grid-template-columns: 1fr; }
      .partners { grid-template-columns: repeat(2, 1fr); }
    }
  </style>
</head>
<body>

  <header class="site-header">
    <div class="wrap nav">
      <a class="brand" href="home-mockup.html">Hawaiʻi Rangeland Information Portal <span class="beta">BETA</span></a>
      <ul class="nav-links">
        <li><a href="home-mockup.html#conditions">Conditions</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a class="cta" href="home-mockup.html#ranch">Find a ranch</a></li>
      </ul>
    </div>
  </header>

  <div class="wrap page-title">
    <div class="crumbs"><a href="home-mockup.html#ranch">Ranches</a> / <span id="crumbIsle">—</span></div>
    <div class="title-row"><h1 id="ranchId">—</h1><span class="meta" id="titleMeta">Loading…</span></div>
  </div>

  <nav class="subnav" aria-label="Sections">
    <div class="wrap">
      <ul>
        <li><a href="#dashboard" class="active">Dashboard</a></li>
        <li><a href="#outlook">Rainfall Outlook</a></li>
        <li><a href="#tool">Decision Support Tool</a></li>
        <li><a href="#rainfall">Rainfall</a></li>
        <li><a href="#temperature">Temperature</a></li>
        <li><a href="#vegetation">NDVI</a></li>
        <li><a href="#drought">Drought</a></li>
      </ul>
    </div>
  </nav>

  <main class="wrap">

    <!-- ================= Dashboard ================= -->
    <section class="block" id="dashboard" style="padding-top:24px">
      <div class="dash">
        <div class="dash-head"><h2>Dashboard</h2></div>
        <div class="dash-grid">
          <!-- Rainfall -->
          <div class="cell c-half">
            <div class="mcell">
              <div class="m-id"><div class="m-icon" style="background:#3d89f7"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 14a4.5 4.5 0 0 0-1-8.9A6 6 0 0 0 5 7.5 3.5 3.5 0 0 0 6 14.5"/><path d="M8 17l-1 2.5M12 16l-1 3M16 17l-1 2.5"/></svg></div><div class="name">Rainfall</div><div class="seg" role="group" aria-label="Rainfall period"><button aria-pressed="true" data-v="d">Daily</button><button aria-pressed="false" data-v="m">Monthly</button></div></div>
              <div class="m-body" data-v="d">
                <div class="m-date" id="rfDDate">—</div>
                <div class="m-vals">
                  <div class="m-val"><div class="v"><span id="rfD">—</span><small>in</small></div><div class="k">Total Rainfall</div></div>
                  <div class="m-val"><div class="v" id="dryConsec">—</div><div class="k">Consecutive Dry Days</div></div>
                </div>
              </div>
              <div class="m-body" data-v="m" hidden>
                <div class="m-date" id="rfMDate">—</div>
                <div class="m-vals">
                  <div class="m-val"><div class="v"><span id="rfM">—</span><small>in</small><span class="d" id="rfMDelta"></span></div><div class="k">Total Rainfall</div><div class="s" id="rfStatus"></div></div>
                  <div class="m-val"><div class="v" id="dryTotal">—</div><div class="k">Total Dry Days</div></div>
                </div>
              </div>
            </div>
            <div class="info-wrap"><button class="info" type="button" aria-expanded="false" aria-label="About rainfall">i</button><div class="popover"><p><b>Daily rainfall:</b> total accumulated rainfall for yesterday. <b>Consecutive dry days:</b> days in a row with under 0.04 in of rain.</p><p><b>Monthly rainfall:</b> total for last month, and the percent difference from the typical rainfall for that month. <b>Total dry days:</b> days in the month with under 0.04 in.</p></div></div>
          </div>
          <!-- Temperature -->
          <div class="cell c-half">
            <div class="mcell">
              <div class="m-id"><div class="m-icon" style="background:#f03737"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/><path d="M12 9v8"/></svg></div><div class="name">Temperature</div><div class="seg" role="group" aria-label="Temperature period"><button aria-pressed="true" data-v="d">Daily</button><button aria-pressed="false" data-v="m">Monthly</button></div></div>
              <div class="m-body" data-v="d">
                <div class="m-date" id="tDDate">—</div>
                <div class="m-vals">
                  <div class="m-val"><div class="v"><span id="tD">—</span><small>°F</small><span class="d" id="tDDelta"></span></div><div class="k">Daily Temperature</div></div>
                  <div class="m-val"><div class="v" style="font-size:20px">Max <span id="tDMax">—</span></div><div class="v" style="font-size:20px">Min <span id="tDMin">—</span></div></div>
                </div>
              </div>
              <div class="m-body" data-v="m" hidden>
                <div class="m-date" id="tMDate">—</div>
                <div class="m-vals">
                  <div class="m-val"><div class="v"><span id="tM">—</span><small>°F</small><span class="d" id="tMDelta"></span></div><div class="k">Monthly Temperature</div></div>
                  <div class="m-val"><div class="v" style="font-size:20px">Max <span id="tMMax">—</span></div><div class="v" style="font-size:20px">Min <span id="tMMin">—</span></div></div>
                </div>
              </div>
            </div>
            <div class="info-wrap"><button class="info" type="button" aria-expanded="false" aria-label="About temperature">i</button><div class="popover"><p><b>Daily:</b> yesterday's average, minimum and maximum temperature. The difference compares with the average temperature for that month.</p><p><b>Monthly:</b> last month's average, minimum and maximum, compared with the average for that month.</p></div></div>
          </div>
          <!-- 12-Month Drought History -->
          <div class="cell c-chart">
            <h3>12-Month Drought History</h3>
            <div class="sub" id="dMonths">—</div>
            <div class="chart" id="spi12" style="height:300px"></div>
            <div class="info-wrap"><button class="info" type="button" aria-expanded="false" aria-label="About drought history">i</button><div class="popover"><p>Drought history uses the 3-month Standardized Precipitation Index (SPI) to determine drought.</p><p>If <b>SPI &lt; −0.5</b>, the area is in drought (shaded red). The lower the number, the higher the drought intensity.</p><p>Hover over the chart to see values.</p></div></div>
          </div>
          <!-- Severity + ENSO -->
          <div class="cell c-side">
            <div class="cell">
              <h3>Current Drought Severity</h3>
              <div style="margin-top:10px" id="dStatus">—</div>
              <div class="info-wrap"><button class="info" type="button" aria-expanded="false" aria-label="About drought severity">i</button><div class="popover"><p>Drought severity is based on the current Standardized Precipitation Index (SPI).</p><table><tr><td>−0.5 to −0.79</td><td>Abnormally Dry</td></tr><tr><td>−0.8 to −1.29</td><td>Moderate Drought</td></tr><tr><td>−1.3 to −1.59</td><td>Severe Drought</td></tr><tr><td>−1.6 to −1.99</td><td>Extreme Drought</td></tr><tr><td>−2 or less</td><td>Exceptional Drought</td></tr></table></div></div>
            </div>
            <div class="cell">
              <img class="gauge-img" src="../gauge/gauge.png" alt="ENSO gauge">
              <div class="enso-text"><span id="ensoMonth"></span> ENSO (El Niño–Southern Oscillation) Conditions:<br><b id="phaseName">—</b></div>
              <div class="mini-cap">Monthly Rainfall</div>
              <table class="mini-table">
                <tr><td>Historical Avg</td><td id="mrf">—</td></tr>
                <tr><td><span class="phaseLong"></span> Avg</td><td id="merf">—</td></tr>
                <tr><td><span class="phaseLong"></span> Min</td><td id="mnrf">—</td></tr>
              </table>
              <div class="info-wrap"><button class="info" type="button" aria-expanded="false" aria-label="About ENSO">i</button><div class="popover"><p>Current ENSO conditions are determined using NOAA's Relative Oceanic Niño Index (RONI).</p><p><b>During an El Niño:</b> typically wet summers and dry winters.</p><p><b>During a La Niña:</b> typically dry summers and wet winters.</p></div></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= Outlook ================= -->
    <section class="block" id="outlook">
      <div class="section-head"><h2>ENSO Almanac: 3-Month Rainfall Outlook</h2>
        <p>Rainfall at this ranch in past years with the same ENSO phase as now (<span class="phaseShort"></span>, <span id="phaseYears">—</span> years).</p></div>
      <div class="card chart-card">
        <div class="chart" id="outlookChart"></div>
        <div class="card-foot">
          <div class="legend-row">
            <span><i style="background:#8a938e"></i>Historical average</span>
            <span><i style="background:var(--rain)"></i><span class="phaseShort"></span> average</span>
            <span><i style="background:#9cc3e6"></i><span class="phaseShort"></span> minimum</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= Forage tool ================= -->
    <section class="block" id="tool">
      <div class="section-head"><h2>Forage Production Decision Support Tool</h2>
        <p>Select your grass type and pasture condition to estimate forage production for the coming months.</p></div>
      <div class="card">
        <form class="tool-form" id="toolForm">
          <label class="field">Grass type
            <select name="grasstype">
              <option value="Kikuyu">Kikuyu grass</option>
              <option value="Pangola">Pangola grass</option>
              <option value="Buffel">Buffel grass</option>
              <option value="Signal">Signal grass</option>
              <option value="Guinea">Guinea grass</option>
            </select>
          </label>
          <label class="field">Forage condition
            <select name="condition">
              <option value="Improved">Improved</option>
              <option value="Unimproved">Unimproved</option>
            </select>
          </label>
          <button class="btn" type="submit">Submit</button>
        </form>
        <div id="toolResults" aria-live="polite"></div>
      </div>
    </section>

    <!-- ================= Rainfall ================= -->
    <section class="block" id="rainfall">
      <div class="section-head"><div class="kicker" style="color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase">Average Climate Conditions</div><h2>Rainfall</h2></div>
      <div class="grid">
        <div class="stack span-5">
          <div class="stat-pair">
            <div class="card stat-card">
              <div class="v"><span id="s_rfM">—</span><small>in</small></div>
              <div class="d" id="s_rfMDelta">—</div>
              <div id="s_rfStatus"></div>
              <div class="k"><span id="s_dryTotal">—</span> total dry days</div>
              <div class="when" id="s_rfMDate">Monthly rainfall</div>
            </div>
            <div class="card stat-card">
              <div class="v"><span id="s_rfD">—</span><small>in</small></div>
              <div class="k">&nbsp;</div>
              <div class="k"><span id="s_dryConsec">—</span> consecutive dry days</div>
              <div class="k"><span id="s_rfMtd">—</span> in month to date</div>
              <div class="when" id="s_rfDDate">Daily rainfall</div>
            </div>
          </div>
          <div class="card map-card"><a id="rfMapLink" target="_blank"><img id="rfMap" alt="Monthly rainfall map" loading="lazy"></a><div class="cap">Click map to enlarge</div></div>
        </div>
        <div class="card chart-card span-7">
          <div class="card-head"><h3>Last 12 months</h3>
            <div class="legend-row"><span><i style="background:var(--rain-soft)"></i>Monthly average</span><span><i class="ln" style="background:var(--rain)"></i>Observed</span></div></div>
          <div class="chart" id="rf12"></div>
        </div>
        <div class="card chart-card span-12">
          <div class="card-head"><h3>Monthly rainfall since 1920</h3><a class="sub" id="rfCsv" download>Download CSV</a></div>
          <div class="chart hist" id="rfHist"></div>
        </div>
      </div>
    </section>

    <!-- ================= Temperature ================= -->
    <section class="block" id="temperature">
      <div class="section-head"><h2>Temperature</h2></div>
      <div class="grid">
        <div class="stack span-5">
          <div class="stat-pair">
            <div class="card stat-card">
              <div class="v"><span id="s_tD">—</span><small>°F</small></div>
              <div class="d" id="s_tDDelta">—</div>
              <div class="k">Daily average temperature</div>
              <div class="when" id="s_tDate">—</div>
            </div>
            <div class="card stat-card">
              <div class="row">
                <div><div class="v" style="font-size:24px" id="s_tMax">—</div><div class="k">High</div></div>
                <div><div class="v" style="font-size:24px" id="s_tMin">—</div><div class="k">Low</div></div>
              </div>
              <div class="when" id="s_tDate2">—</div>
            </div>
          </div>
          <div class="card map-card"><a id="tMapLink" target="_blank"><img id="tMap" alt="Monthly temperature map" loading="lazy"></a><div class="cap">Click map to enlarge</div></div>
        </div>
        <div class="card chart-card span-7">
          <div class="card-head"><h3>Last 12 months</h3>
            <div class="legend-row"><span><i style="background:var(--temp-soft)"></i>Monthly average</span><span><i class="ln" style="background:var(--temp)"></i>Observed</span></div></div>
          <div class="chart" id="t12"></div>
        </div>
        <div class="card chart-card span-12">
          <div class="card-head"><h3>Monthly mean temperature since 1990</h3><a class="sub" id="tCsv" download>Download CSV</a></div>
          <div class="chart hist" id="tHist"></div>
        </div>
      </div>
    </section>

    <!-- ================= NDVI ================= -->
    <section class="block" id="vegetation">
      <div class="section-head"><h2>Normalized Difference Vegetation Index (NDVI)</h2></div>
      <div class="grid">
        <div class="stack span-5">
          <div class="stat-pair">
            <div class="card stat-card">
              <div class="v" id="s_ndvi">—</div>
              <div class="d" id="s_ndviDelta">—</div>
              <div class="k">Monthly average NDVI</div>
              <div class="when" id="s_ndviDate">—</div>
            </div>
            <div class="card desc"><p>NDVI measures how green the land is, from −1 to +1. Values of about 0.6–0.9 mean dense, healthy vegetation. It is widely used to monitor drought and forage.</p></div>
          </div>
          <div class="card map-card"><a id="nMapLink" target="_blank"><img id="nMap" alt="Monthly NDVI map" loading="lazy"></a><div class="cap">Click map to enlarge</div></div>
        </div>
        <div class="card chart-card span-7">
          <div class="card-head"><h3>Last 12 months</h3>
            <div class="legend-row"><span><i style="background:var(--veg-soft)"></i>Monthly average</span><span><i class="ln" style="background:var(--veg)"></i>Observed</span></div></div>
          <div class="chart" id="n12"></div>
        </div>
        <div class="card chart-card span-12">
          <div class="card-head"><h3>Monthly NDVI since 2000</h3><a class="sub" id="nCsv" download>Download CSV</a></div>
          <div class="chart hist" id="nHist"></div>
        </div>
      </div>
    </section>

    <!-- ================= Drought ================= -->
    <section class="block" id="drought">
      <div class="section-head"><h2>Drought History</h2><p>(Standardized Precipitation Index-3)</p></div>
      <div class="card chart-card">
        <div class="card-head">
          <div class="legend-row">
            <span><i class="ln" style="background:var(--rain)"></i>SPI-3</span><span><i style="background:rgba(214,69,69,.18)"></i>Drought (SPI below −0.5)</span>
          </div>
          <a class="sub" id="sCsv" download>Download CSV</a>
        </div>
        <div class="chart hist" id="spiAll"></div>
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <h4>Hawaiʻi Rangeland Information Portal</h4>
          <p>Funded by the <a href="https://www.drought.gov/" target="_blank">National Integrated Drought Information System (NIDIS)</a>.</p>
          <p style="margin-top:20px"><span style="color:#8fa097">Contact</span><br><a href="mailto:hcdp@hawaii.edu">hcdp@hawaii.edu</a></p>
        </div>
        <div>
          <h4>Partners</h4>
          <div class="partners">
            <div><img src="../logos/NOAA.png" alt="NOAA"></div>
            <div><img src="../logos/NIDIS.jpeg" alt="NIDIS"></div>
            <div><img src="../logos/UHM.png" alt="University of Hawaiʻi at Mānoa"></div>
            <div><img src="../logos/EWC.png" alt="East-West Center"></div>
            <div><img src="../logos/PDKE.png" alt="PDKE"></div>
            <div><img src="../logos/HCC.png" alt="HCC"></div>
            <div><img src="../logos/NRCS.png" alt="NRCS"></div>
          </div>
        </div>
      </div>
      <div class="legal"><span>© <span id="year"></span> University of Hawaiʻi at Mānoa</span><span>hrip.manoa.hawaii.edu</span></div>
    </div>
  </footer>

  <script>
  (async () => {
    const RID = (new URLSearchParams(location.search).get('ranch') || 'RID118').toUpperCase();
    const base = `../RID/${RID}/${RID}`;
    const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    const ABBR = MONTHS.map(m => m.slice(0, 3));
    const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
    const $ = id => document.getElementById(id);
    const set = (id, v) => { const e = $(id); if (e) e.textContent = v; };
    const fmt = (v, d = 2) => (v == null || isNaN(v)) ? '—' : (+v).toFixed(d);
    const signed = (v, d = 1, unit = '') => isNaN(v) ? '—' : (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(d) + unit;
    const dirCls = v => v > 0 ? 'up' : v < 0 ? 'down' : 'neutral';
    const day = (y, m, d) => new Date(+y, +m - 1, +d).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    set('year', new Date().getFullYear());
    document.title = `${RID} · H-RIP`;
    set('ranchId', RID);

    // ---------- Data ----------
    const text = url => fetch(url, { cache: 'no-cache' }).then(r => r.ok ? r.text() : Promise.reject(url));
    const csv = async url => {
      const rows = (await text(url)).trim().split(/\r?\n/), head = rows.shift().split(',');
      return rows.map(l => { const c = l.split(','), o = {}; head.forEach((h, i) => o[h || '_i'] = c[i]); return o; });
    };
    const lines = async url => (await text(url)).trim().split(/\r?\n/);
    const safe = p => p.catch(e => { console.warn('missing', e); return null; });
    const [rf, rfMonth, tmean, tMonth, ndvi, ndviMonth, spi, query, dLast, dThis, rfD, tD, tM, dry, gauge] = await Promise.all([
      safe(csv(`${base}_rf.csv`)), safe(csv(`${base}_rf_month.csv`)), safe(csv(`${base}_tmean.csv`)), safe(csv(`${base}_t_month.csv`)),
      safe(csv(`${base}_ndvi.csv`)), safe(csv(`${base}_ndvi_month.csv`)), safe(csv(`${base}_spi.csv`)), safe(csv(`${base}_query.csv`)),
      safe(csv(`${base}_rf_daily_last_month.csv`)), safe(csv(`${base}_rf_daily_this_month.csv`)),
      safe(lines(`${base}_rf_d.txt`)), safe(lines(`${base}_temp_d.txt`)), safe(lines(`${base}_temp_m.txt`)), safe(lines(`${base}_consec_dry_days.txt`)),
      safe(fetch('../gauge/gauge.json', { cache: 'no-cache' }).then(r => r.json()))
    ]);
    if (!rf) { set('titleMeta', `No data found for ${RID}`); return; }

    const avgBy = (rows, col) => Object.fromEntries((rows || []).map(r => [r.Month, +r[col]]));
    const rfAvg = avgBy(rfMonth, 'RF'), tAvg = avgBy(tMonth, 'Temp'), nAvg = avgBy(ndviMonth, 'NDVI');
    const lastN = (rows, n) => rows.slice(-n);
    const label = r => `${ABBR[+r.Month - 1]} ${String(Math.round(+r.Year)).slice(2)}`;

    // ---------- Title ----------
    const feat = ranchSquares.features.find(f => f.properties.Polygon === RID);
    const isle = feat ? { BI: 'Hawaiʻi Island', MA: 'Maui', OA: 'Oʻahu', MO: 'Molokaʻi', KA: 'Kauaʻi', LA: 'Lānaʻi', KO: 'Kahoʻolawe' }[feat.properties.IS] : '';
    set('crumbIsle', isle || RID);
    set('titleMeta', [isle, rfD ? 'Data through ' + new Date(+rfD[1], +rfD[2] - 1, +rfD[3]).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : ''].filter(Boolean).join(' · '));

    // ---------- Status pills ----------
    const ICON = {
      good: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.6 5.8-4.2 4.6a.8.8 0 0 1-1.2 0L4.4 8.5a.8.8 0 1 1 1.2-1.1l1.2 1.3 3.6-4a.8.8 0 1 1 1.2 1.1z"/></svg>',
      warn: '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm0 3.5a.9.9 0 0 1 .9.9v4a.9.9 0 0 1-1.8 0v-4a.9.9 0 0 1 .9-.9zm0 9.3a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>'
    };
    ICON.bad = ICON.warn;
    const status = (cls, txt, big) => `<span class="status ${cls}${big ? ' big' : ''}">${ICON[cls]}${txt}</span>`;

    // ---------- Rainfall numbers ----------
    const rfLast = rf[rf.length - 1], rfMName = MONTHS[+rfLast.Month - 1];
    const rfMv = +rfLast.RF_in, rfMa = rfAvg[rfMName], rfPct = (rfMv - rfMa) / rfMa * 100;
    const dryTotal = dLast ? dLast.filter(r => +r.RF_in < 0.03937).length : '—';
    const rfStatus = rfMv >= rfMa ? status('good', 'Above average') : status('warn', 'Below average');
    const rfMDate = `${rfMName} ${Math.round(+rfLast.Year)}`;
    const pct = `<span class="${dirCls(rfPct)}">${signed(rfPct, 1, '%')}</span> <span class="neutral" style="font-weight:400">vs. avg</span>`;
    ['rfM', 's_rfM'].forEach(i => set(i, fmt(rfMv)));
    $('s_rfMDelta').innerHTML = pct;
    $('rfMDelta').innerHTML = `<span class="${dirCls(rfPct)}">${signed(rfPct, 1, '%')}</span>`;
    ['rfStatus', 's_rfStatus'].forEach(i => $(i).innerHTML = rfStatus);
    ['dryTotal', 's_dryTotal'].forEach(i => set(i, dryTotal));
    set('s_rfMDate', `Monthly rainfall · ${rfMDate}`); set('rfMDate', `${rfMName}, ${Math.round(+rfLast.Year)}`);
    if (rfD) {
      ['rfD', 's_rfD'].forEach(i => set(i, fmt(+rfD[0])));
      set('rfDDate', day(rfD[1], rfD[2], rfD[3])); set('s_rfDDate', `Daily rainfall · ${day(rfD[1], rfD[2], rfD[3])}`);
    }
    ['dryConsec', 's_dryConsec'].forEach(i => set(i, dry ? dry[0] : '—'));
    set('s_rfMtd', dThis ? fmt(dThis.reduce((s, r) => s + +r.RF_in, 0)) : '—');

    // ---------- Temperature numbers ----------
    const tDelta = (v, name) => { const d = v - tAvg[name]; return `<span class="${d > 0 ? 'down' : d < 0 ? 'up' : 'neutral'}" style="color:var(--ink-2)">${signed(d, 1, '°F')}</span> <span class="neutral" style="font-weight:400">vs. avg</span>`; };
    if (tD) {
      const name = MONTHS[+tD[4] - 1], when = day(tD[3], tD[4], tD[5]);
      ['tD', 's_tD'].forEach(i => set(i, Math.round(+tD[0])));
      $('s_tDDelta').innerHTML = tDelta(+tD[0], name); set('tDDelta', signed(+tD[0] - tAvg[name], 2, '°F'));
      ['tDMax', 's_tMax'].forEach(i => set(i, Math.round(+tD[1]) + '°F')); ['tDMin', 's_tMin'].forEach(i => set(i, Math.round(+tD[2]) + '°F'));
      set('tDDate', when); set('s_tDate', when); set('s_tDate2', when);
    }
    if (tM) {
      const name = MONTHS[+tM[4] - 1];
      set('tM', Math.round(+tM[0])); set('tMDelta', signed(+tM[0] - tAvg[name], 2, '°F'));
      set('tMMax', Math.round(+tM[1]) + '°F'); set('tMMin', Math.round(+tM[2]) + '°F'); set('tMDate', `${name}, ${tM[3]}`);
    }

    // ---------- NDVI numbers ----------
    if (ndvi) {
      const n = ndvi[ndvi.length - 1], name = MONTHS[+n.Month - 1], d = +n.NDVI - nAvg[name];
      set('s_ndvi', fmt(+n.NDVI));
      $('s_ndviDelta').innerHTML = `<span class="${dirCls(d)}">${signed(d, 2)}</span> <span class="neutral" style="font-weight:400">vs. monthly avg</span>`;
      set('s_ndviDate', `${name} ${Math.round(+n.Year)}`);
    }

    // ---------- ENSO ----------
    const PH = [
      { code: 'SEL', name: 'Strong El Niño', test: v => v > 1.1 }, { code: 'WEL', name: 'Weak El Niño', test: v => v > 0.5 },
      { code: 'NUT', name: 'Neutral', test: v => v >= -0.5 }, { code: 'WLA', name: 'Weak La Niña', test: v => v >= -1.1 },
      { code: 'SLA', name: 'Strong La Niña', test: () => true }
    ];
    const phase = gauge ? PH.find(p => p.test(gauge.value)) : null;
    const now = new Date(), m0 = now.getMonth() + 1;
    set('ensoMonth', MONTHS[m0 - 1]);
    document.querySelectorAll('.thisMonth').forEach(e => e.textContent = MONTHS[m0 - 1]);
    if (gauge) {
      document.querySelector('.gauge-img').src = '../gauge/gauge.png?v=' + gauge.updated;
    }
    document.querySelectorAll('.phaseShort').forEach(e => e.textContent = phase ? phase.name : 'Phase');
    document.querySelectorAll('.phaseLong').forEach(e => e.textContent = `${ABBR[m0 - 1]} ${phase ? phase.name : ''}`);
    set('phaseName', phase ? phase.name : '—');

    // ---------- Plotly ----------
    const narrow = innerWidth < 680;
    const baseLayout = () => ({
      font: { family: 'Lato, sans-serif', size: 13, color: css('--ink-2') },
      margin: { l: 44, r: 10, t: 6, b: 34 }, paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      hovermode: 'x unified', hoverlabel: { bgcolor: css('--ink'), bordercolor: css('--ink'), font: { color: '#fff', family: 'Lato, sans-serif' } },
      xaxis: { showgrid: false, linecolor: css('--line'), tickfont: { color: css('--ink-3') }, fixedrange: true, tickangle: 0, nticks: narrow ? 6 : 12 },
      yaxis: { gridcolor: css('--line'), zeroline: false, tickfont: { color: css('--ink-3') }, fixedrange: true },
      showlegend: false, bargap: .3
    });
    const cfg = { displayModeBar: false, responsive: true };
    // Charts that stretch to their card redraw when the card changes size (e.g. after the map image loads).
    const fitObs = new ResizeObserver(es => es.forEach(e => { if (e.target.data) Plotly.Plots.resize(e.target); }));
    const refit = () => document.querySelectorAll(".chart-card.span-7 .chart").forEach(el => { if (el.data) Plotly.Plots.resize(el); });
    document.querySelectorAll(".map-card img").forEach(img => img.addEventListener("load", refit));

    // Dashboard style: monthly average as soft bars, observed as a line on top
    function twelve(id, rows, col, avg, strong, soft, unit, digits, yTitle) {
      const x = rows.map(label), y = rows.map(r => +r[col]), a = rows.map(r => avg[MONTHS[+r.Month - 1]]);
      const L0 = baseLayout(); L0.yaxis.title = { text: yTitle, font: { size: 12 } };
      if (col !== 'RF_in') { const all = y.concat(a); const pad = (Math.max(...all) - Math.min(...all)) * .25; L0.yaxis.range = [Math.min(...all) - pad, Math.max(...all) + pad]; }
      Plotly.newPlot(id, [
        { type: 'bar', x, y: a, name: 'Monthly average', marker: { color: soft, cornerradius: 4 }, hovertemplate: `Average %{y:.${digits}f} ${unit}<extra></extra>` },
        { type: 'scatter', mode: 'lines+markers', x, y, name: 'Observed', line: { color: strong, width: 2.5 }, marker: { size: 8, color: strong, line: { color: '#fff', width: 2 } }, hovertemplate: `Observed %{y:.${digits}f} ${unit}<extra></extra>` }
      ], L0, cfg);
      fitObs.observe($(id));
    }
    function history(id, rows, col, color, unit, digits, years, yTitle) {
      const x = rows.map(r => r.datetime), y = rows.map(r => +r[col]);
      const end = x[x.length - 1], s = new Date(end); s.setFullYear(s.getFullYear() - years);
      const L0 = baseLayout();
      L0.margin.t = 34; L0.yaxis.title = { text: yTitle, font: { size: 12 } };
      L0.xaxis = { ...L0.xaxis, fixedrange: false, nticks: undefined, range: [s.toISOString().slice(0, 10), end], rangeslider: { visible: !narrow, thickness: .08, bgcolor: css('--surface-2') },
        rangeselector: { buttons: [{ count: 5, label: '5y', step: 'year', stepmode: 'backward' }, { count: 10, label: '10y', step: 'year', stepmode: 'backward' }, { count: 30, label: '30y', step: 'year', stepmode: 'backward' }, { step: 'all', label: 'All' }],
          bgcolor: css('--surface-2'), activecolor: css('--brand-soft'), font: { size: 12 }, x: 0, y: 1.1 } };
      Plotly.newPlot(id, [{ type: 'scatter', mode: 'lines', x, y, line: { color, width: 1.6 }, hovertemplate: `%{x|%b %Y}: %{y:.${digits}f} ${unit}<extra></extra>` }], L0, cfg);
    }

    // ---------- Drought ----------
    const SPI_CATS = [
      { max: -2, name: 'Exceptional Drought', cls: 'bad' }, { max: -1.6, name: 'Extreme Drought', cls: 'bad' },
      { max: -1.3, name: 'Severe Drought', cls: 'bad' }, { max: -0.8, name: 'Moderate Drought', cls: 'warn' },
      { max: -0.5, name: 'Abnormally Dry', cls: 'warn' }, { max: Infinity, name: 'No Drought', cls: 'good' }
    ];
    const cat = v => SPI_CATS.find(c => v <= c.max);
    const spiRows = (spi || []).filter(r => r['SPI-3']);
    const spiLine = (id, rows, monthly) => {
      const x = rows.map(r => r.datetime), y = rows.map(r => +r['SPI-3']);
      const lim = Math.max(3, Math.ceil(Math.max(...y.map(Math.abs)) + .5));
      const L0 = baseLayout();
      L0.hovermode = 'x unified';
      L0.yaxis = { ...L0.yaxis, range: [-lim, lim], title: { text: 'Drought        No Drought', font: { size: 12 } }, zeroline: true, zerolinecolor: css('--ink-3') };
      L0.shapes = [{ type: 'rect', xref: 'paper', x0: 0, x1: 1, y0: -0.5, y1: -lim, fillcolor: '#d64545', opacity: .1, line: { width: 0 }, layer: 'below' }];
      if (monthly) L0.xaxis = { ...L0.xaxis, tickformat: '%b %y', dtick: narrow ? 'M3' : 'M1' };
      else { L0.margin.t = 34; L0.xaxis = { ...L0.xaxis, fixedrange: false, nticks: undefined, rangeslider: { visible: !narrow, thickness: .08, bgcolor: css('--surface-2') },
        range: [x[Math.max(0, x.length - 120)], x[x.length - 1]],
        rangeselector: { buttons: [{ count: 10, label: '10y', step: 'year', stepmode: 'backward' }, { count: 30, label: '30y', step: 'year', stepmode: 'backward' }, { step: 'all', label: 'All' }], bgcolor: css('--surface-2'), activecolor: css('--brand-soft'), font: { size: 12 }, x: 0, y: 1.1 } }; }
      Plotly.newPlot(id, [{ type: 'scatter', mode: monthly ? 'lines+markers' : 'lines', x, y, customdata: y.map(v => cat(v).name),
        line: { color: css('--rain'), width: monthly ? 2.5 : 1.4 }, marker: { size: 8, color: css('--rain'), line: { color: '#fff', width: 2 } },
        hovertemplate: 'SPI-3 %{y:.2f} · %{customdata}<extra></extra>' }], L0, cfg);
    };
    if (spiRows.length) {
      const last12 = lastN(spiRows, 12), cur = +last12[last12.length - 1]['SPI-3'], c = cat(cur);
      $('dStatus').innerHTML = status(c.cls, c.name, true);
      set('spiNow', signed(cur, 2));
      set('spiDate', new Date(last12[last12.length - 1].datetime + 'T00:00').toLocaleDateString('en-US', { month: 'long', year: 'numeric' }));
      set('dMonths', `${last12.filter(r => +r['SPI-3'] < -0.5).length} out of 12 months in drought`);
      spiLine('spi12', last12, true);
      spiLine('spiAll', spiRows, false);
    }

    // ---------- Outlook ----------
    if (query && phase) {
      const rows = [0, 1, 2].map(i => ((m0 - 1 + i) % 12) + 1).map(m => query.find(r => +r.Month === m && r.Phase === phase.code)).filter(Boolean);
      if (rows[0]) { set('mrf', fmt(+rows[0].MRF) + ' in'); set('merf', fmt(+rows[0].MeRF) + ' in'); set('mnrf', fmt(+rows[0].MnRF) + ' in'); set('phaseYears', rows[0].Count); }
      const x = rows.map(r => MONTHS[+r.Month - 1]);
      const bar = (col, color, name) => ({ type: 'bar', x, y: rows.map(r => +r[col]), name, marker: { color, cornerradius: 4 }, hovertemplate: `${name}: %{y:.2f} in<extra></extra>` });
      const L0 = baseLayout(); L0.barmode = 'group'; L0.bargroupgap = .08; L0.yaxis.title = { text: 'Monthly rainfall (in)', font: { size: 12 } };
      Plotly.newPlot('outlookChart', [bar('MRF', '#8a938e', 'Historical average'), bar('MeRF', css('--rain'), `${phase.name} average`), bar('MnRF', '#9cc3e6', `${phase.name} minimum`)], L0, cfg);
    }

    // ---------- Climate sections ----------
    twelve('rf12', lastN(rf, 12), 'RF_in', rfAvg, css('--rain'), css('--rain-soft'), 'in', 2, 'Rainfall (in)');
    history('rfHist', rf, 'RF_in', css('--rain'), 'in', 2, 30, 'Rainfall (in)');
    if (tmean) { twelve('t12', lastN(tmean, 12), 'tmean_f', tAvg, css('--temp'), css('--temp-soft'), '°F', 1, 'Temperature (°F)'); history('tHist', tmean, 'tmean_f', css('--temp'), '°F', 1, 10, 'Temperature (°F)'); }
    if (ndvi) { twelve('n12', lastN(ndvi, 12), 'NDVI', nAvg, css('--veg'), css('--veg-soft'), '', 2, 'NDVI'); history('nHist', ndvi, 'NDVI', css('--veg'), '', 2, 10, 'NDVI'); }
    [['rf', 'rf'], ['t', 'temp'], ['n', 'ndvi']].forEach(([k, f]) => { $(k + 'Map').src = `${base}_${f}.png`; $(k + 'MapLink').href = `${base}_${f}.png`; });
    requestAnimationFrame(refit); addEventListener('load', refit);
    $('rfCsv').href = `${base}_rf.csv`; $('tCsv').href = `${base}_tmean.csv`; $('nCsv').href = `${base}_ndvi.csv`; $('sCsv').href = `${base}_spi.csv`;

    // ---------- Interactions ----------
    // Each dashboard card has its own Daily/Monthly switch, as on the live page
    document.querySelectorAll('.seg').forEach(seg => seg.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      seg.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b));
      seg.closest('.cell').querySelectorAll('.m-body').forEach(d => d.hidden = d.dataset.v !== b.dataset.v);
    }));
    const closeAll = () => document.querySelectorAll('.popover.open').forEach(p => { p.classList.remove('open'); p.previousElementSibling.setAttribute('aria-expanded', false); });
    document.querySelectorAll('.info').forEach(btn => btn.addEventListener('click', e => {
      e.stopPropagation(); const pop = btn.nextElementSibling, open = !pop.classList.contains('open');
      closeAll(); pop.classList.toggle('open', open); btn.setAttribute('aria-expanded', open);
    }));
    document.addEventListener('click', e => { if (!e.target.closest('.popover')) closeAll(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAll(); });

    // Section nav: highlight the section in view
    const links = [...document.querySelectorAll('.subnav a')];
    const spy = new IntersectionObserver(es => es.forEach(en => {
      if (!en.isIntersecting) return;
      links.forEach(a => a.classList.toggle('active', a.hash === '#' + en.target.id));
      const a = links.find(a => a.hash === '#' + en.target.id); if (a) a.parentElement.parentElement.scrollTo({ left: a.offsetLeft - 16, behavior: 'smooth' });
    }), { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('main section').forEach(s => spy.observe(s));

    // Forage tool posts to the existing tool.php (needs the PHP server)
    $('toolForm').addEventListener('submit', async e => {
      e.preventDefault();
      const out = $('toolResults'), fd = new FormData(e.target); fd.append('ranch', RID);
      out.innerHTML = '<div class="msg">Calculating…</div>';
      try {
        const r = await fetch(`../tool.php?ranch=${RID}`, { method: 'POST', body: fd }), html = (await r.text()).trim();
        out.innerHTML = r.ok && html && !html.startsWith('<' + '?php') ? html : '<div class="msg">The forage tool needs the PHP server (tool.php). It works on the live site.</div>';
      } catch { out.innerHTML = '<div class="msg">Could not reach tool.php.</div>'; }
    });
  })();
  </script>
</body>
</html>
