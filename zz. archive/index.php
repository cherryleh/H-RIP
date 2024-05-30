<!DOCTYPE html>
<html>

<head>
    <title>Hawai&#x02BB;i Rangeland Informational Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="./CSS/index.css">
    <link rel="stylesheet" type="text/css" href="./CSS/header.css">
    <link rel="stylesheet" type="text/css" href="./CSS/footer.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

    <!-- Leaflet -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css" crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js" crossorigin=""></script>

    <script src="./Leaflet/ranches.js"></script>
    <script src="./Leaflet/coastline.js"></script>


    <script>
        $(function () {
            $("#header").load("./header.html");
            $("#footer").load("./footer.html");
        });

    </script>
</head>

<body>
    <script>
        $(document).ready(function () {
            $('#island-select').on('change', function () {
                var islvalue = $(this).val();
                window.currentIsl = islvalue;
                $("div.myDiv").hide();
                $("#show" + islvalue).show();

                console.log($("#form-no-data"))
                $("#form-no-data").trigger('click');
            });
        });

        /*Radio buttons to display different raster data on island*/
        $(document).ready(function () {
            $("input[name$='bn']").click(function () {
                var radio_value = $(this).val();
                var isl_value = $('#island-select option:selected')[0].value;
                console.log(isl_value)
                if (radio_value == '0') {
                    $("#nodata" + isl_value).show();
                    $("#rainfall" + isl_value).hide();
                    $("#evapotranspiration" + isl_value).hide();
                }
                else if (radio_value == '1') {
                    $("#nodata" + isl_value).hide();
                    $("#rainfall" + isl_value).show();
                    $("#evapotranspiration" + isl_value).hide();
                }
                else if (radio_value == '2') {
                    $("#nodata" + isl_value).hide();
                    $("#rainfall" + isl_value).hide();
                    $("#evapotranspiration" + isl_value).show();
                }
            });
            $('[name="bn"]:checked').trigger('click');
        });

        function popupFunction() {
            var popup = document.getElementById("myPopup");
            popup.classList.toggle("show");
        }
    </script>
    <?php
    if (date("d") < 8) {
        $m = date("m") - 1;
    } else {
        $m = date("m");
    }
    $month = DateTime::createFromFormat('!m', $m);
    $dateObj = DateTime::createFromFormat('!m', intval($m));
    $monthName = $dateObj->format('F');

    $oni_f = file("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt");
    $line = $oni_f[count($oni_f) - 1];
    $values = preg_split('/\s+/', trim($line));
    $oni = end($values);

    if ($oni > 1.1) {
        $phase = 'SEL';
        $phase_name = 'Strong El Ni&#xf1;o';
    } elseif ($oni > 0.5 && $oni <= 1.1) {
        $phase = 'WEL';
        $phase_name = 'Weak El Ni&#xf1;o';
    } elseif ($oni > -0.5 && $oni <= 0.5) {
        $phase = 'NUT';
        $phase_name = 'Neutral';
    } elseif ($oni > -1.1 && $oni <= -0.5) {
        $phase = 'WLA';
        $phase_name = 'Weak La Ni&#xf1;a';
    } elseif ($oni <= -1.1) {
        $phase = 'SLA';
        $phase_name = 'Strong La Ni&#xf1;a';
    }

    if (date("d") < 5) {
        $m = date("m") - 1;
    } else {
        $m = date("m");
    }
    ?>

    <div id="header">Header</div>
    <div class="headerimg">
        <img src="homepage.jpg"
            alt="Placeholder-Image">
        <div class="imgtext">
            <h1 style="font-size: 36px;">Welcome to the <br> Hawai&#x02BB;i Rangeland Information Portal <br>(H-RIP)
            </h1>
            <a href="#"> Learn more</a>
        </div>
    </div>

    <div>
        <h3 id="subcategory">Statewide Conditions - <span class="month"></span>, <span class="year"></span>
        </h3>

        <div id="oni">
            <div class="gauge"><img src="./gauge/gauge.png">

                <p style="float:none;text-align:center">
                    <?php echo ($monthName) ?> ENSO Conditions:
                    <span style="font-weight: 800">
                        <?php echo ($phase_name) ?>
                    </span>
                </p>
                <br>
                <p>
                    <span>Last updated </span><span class="month"></span> <span> 8, </span><span class="year"></span>
                    <!--<span class="month"></span>8, <span class="year"></span>-->
                </p>
            </div>

            <div class="gauge-i tool">&#9432;
                <span class="tooltext">
                    This gauge displays current El Ni&#241;o-Southern Oscillation (ENSO) conditions based on the monthly
                    Oceanic
                    Ni&#241;o Index (ONI) value released by the National Weather Service Climate Prediction Center. This
                    gauge is
                    updated on the 8th of every month. For more info on ENSO and ONI click <a target="_blank"
                        href="https://www.climate.gov/news-features/understanding-climate/climate-variability-oceanic-nino-index">
                        here</a>.
                </span>
            </div>

        </div>

    </div>


    <div class="content">

        <div class="flex-container">

            <div class="flex-child" id="windy">
                <iframe title="windy.com" id="windy" width="450" height="250"
                    style="display: block; border-style:none;box-shadow:0px 4px 8px 0px rgba(0,0,0,0.2);"
                    cellspacing="0"
                    src="https://embed.windy.com/embed2.html?lat=20.689&lon=-157.843&detailLat=20.589&detailLon=-159.173&width=450&height=250&zoom=6&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
                    frameborder="0"></iframe>
            </div>

            <div class="flex-child" id="droughtMonitor" style="margin-left: 5%;">
                <a href="http://droughtmonitor.unl.edu/data/png/current/current_hi_trd.png" style="color:inherit"
                    target="_blank">
                    <img style="width: 400px; height: auto; border: 2px solid; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"
                        src="http://droughtmonitor.unl.edu/data/png/current/current_hi_trd.png"></a>
                <p style="text-align: left;"> Source: <a id="NDMC" href="https://droughtmonitor.unl.edu/"
                        target="_blank">National Drought
                        Mitigation Center (NDMC)</a></p>
            </div>

        </div>


        <div class="sitespecific" id="ranch">
            <h3 id="subcategory">Site-specific Conditions</h3>

            <p style="text-align: center;">Select an island from the dropdown below.</p>
            <select id='zoombox' onchange="zoomToIsl()">

                <option>Select island</option>

                <option value="Hawaii">Hawai&#x02BB;i</option>
                <option value="Lanai">L&#x0101;na&#x02BB;i</option>
                <option value="Kahoolawe">Kaho&#x02BB;olawe</option>
                <option value="Kauai">Kaua&#x02BB;i</option>
                <option value="Maui">Maui</option>
                <option value="Molokai">Moloka&#x02BB;i</option>
                <option value="Oahu">O&#x02BB;ahu</option>





            </select>
            <div id='mapDIV'></div>
            <script src="./Leaflet/leaflet.js"></script>

        </div>


    </div>

    <div id="footer">Footer</div>
    <script>
        const d = new Date();
        const month = new Array();
        month[0] = "January";
        month[1] = "February";
        month[2] = "March";
        month[3] = "April";
        month[4] = "May";
        month[5] = "June";
        month[6] = "July";
        month[7] = "August";
        month[8] = "September";
        month[9] = "October";
        month[10] = "November";
        month[11] = "December";

        let year = d.getFullYear();
        let classYear = document.getElementsByClassName("year");

        var dd = (d.getDate());

        if (dd < 8) {
            name = month[d.getMonth() - 1];
        } else {
            name = month[d.getMonth()];
        }

        console.log(name)

        let classMonth = document.getElementsByClassName("month");

        for (i = 0; i < classYear.length; i++) {
            classYear[i].innerHTML = year;
        }

        for (i = 0; i < classMonth.length; i++) {
            classMonth[i].innerHTML = name;
        }
    </script>

</body>

</html>