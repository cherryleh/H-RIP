<head>

    <title>
        <?php echo $_GET["ranch"]; ?> Ranch Page
    </title>

    <meta name="viewport" content="width=device-width, initial-scale=1"> <!--mobile-->

    <script src="jquery.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400&display=swap"
        rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"
        integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous">
        </script>

    <script>
        $(function () {
            $("#header").load("./header.html");
            $("#footer").load("./footer.html");
        });
    </script>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" type="text/css" href="./CSS/form.css">
    <link rel="stylesheet" type="text/css" href="./CSS/528table.css">
    <link rel="stylesheet" type="text/css" href="./CSS/header.css">
    <link rel="stylesheet" type="text/css" href="./CSS/dashboard.css">
    <link rel="stylesheet" href="./CSS/ranchpage.css">
    <script src="plotly-2.24.1.min.js" charset="utf-8"></script>


    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">

</head>

<body>
    <?php
    //rainfall
    $RID = $_GET["ranch"];
    $file_rf = file('./RID/' . $RID . '/' . $RID . '_rf.csv');
    // Get last row of monthly rainfall file
    //Monthly Rainfall
    if (!empty($file_rf)) {
        $fields_rf = str_getcsv($file_rf[count($file_rf) - 1]); // Parse csv string into an array, get fields from last line
        $rf_m = (round($fields_rf[count($fields_rf) - 2], 2)); //RF value from last row of csv file
        $monthNum_rf = $fields_rf[count($fields_rf) - 4]; //Month of last row (should be last month)
        $year_rf = (round($fields_rf[count($fields_rf) - 5], 0)); //Year of last row
    
    } else {
        echo "Error";
    };

    //Daily Rainfall
    $file_rf_d = file('./RID/' . $RID . '/' . $RID . '_rf_daily_this_month.csv');
    
    if (!empty($file_rf_d)) {
        $fields_rf_d = str_getcsv($file_rf_d[count($file_rf_d) - 1]); // Parse csv string into an array, get fields from last line
        $rf_d = (round($fields_rf_d[count($fields_rf_d) - 1], 3)); //RF value from last row of csv file
        $monthDate_rf_d = $fields_rf_d[count($fields_rf_d) - 2]; //Date
        $monthNum_rf_d = $fields_rf_d[count($fields_rf_d) - 3];//Month of last row (should be last month)
        $year_rf_d = (round($fields_rf_d[count($fields_rf_d) - 4], 0)); //Year of last row
        echo $fields_rf_d[count($fields_rf_d) - 2];
    } else {
        echo "Error";
    };

    $dateObj_rf_d = DateTime::createFromFormat('!m', intval($monthNum_rf_d));
    $monthName_rf_d = $dateObj_rf_d->format('F');
    $date_rf = $monthName_rf_d . ' ' . $monthDate_rf_d . ', ' . $year_rf_d;

    //Date reformat
    $dateObj_rf = DateTime::createFromFormat('!m', intval($monthNum_rf));
    $monthName_rf = $dateObj_rf->format('F');

    //Format: e.g. December, 2022
    $thisMonth_rf = $monthName_rf . ', ' . $year_rf;
    //Open monthly averages file to get average for this month
    $csv_rf = fopen('./RID/' . $RID . '/' . $RID . '_rf_month.csv', 'r');

    // Keep looping as long as we get a new $row
    while ($row_rf = fgetcsv($csv_rf)) {
        if ($row_rf[3] == $monthName_rf) {
            $avg_rf = (round($row_rf[count($row_rf) - 1], 2));
        }
    }
    fclose($csv_rf);

    if ($rf_m > $avg_rf) {
        $status_rf_m = 'Above Average';
        $icon_rf_m = 'class="bi bi-check-circle-fill fs-3" style="color:green; display:inline-block;vertical-align: middle"';
        //$stat_rf_m = '+';
        $color_rf_m = 'green';
    } else {
        $status_rf_m = 'Below Average';
        $icon_rf_m = 'class="bi bi-exclamation-circle-fill fs-3" style="color:orange; display:inline-block; vertical-align: middle"';
        $stat_rf_m = '';
        $color_rf_m = 'red';
    }

    //Percent difference monthly (m) and daily (d)
    $dif_m = ($rf_m - $avg_rf) / $avg_rf * 100;
    $dif_d = ($rf_d - $avg_rf) / $avg_rf * 100;

    $file_consec_dry_days = file('./RID/' . $RID . '/' . $RID . '_consec_dry_days.txt');
    $consec_dry_days = $file_consec_dry_days[0];

    $rf_daily_month = './RID/' . $RID . '/' . $RID . '_rf_daily_last_month.csv';

    // Open the CSV file
/*    if (($handle = fopen($rf_daily_month, "r")) !== FALSE) {
        $total_dry_days = 0;
        //$header = fgetcsv($handle); // Read the header row
        // Loop through each row of the CSV
        while (($data = fgetcsv($handle)) !== FALSE) {
            // Check if the value in the target column is less than 1
            if (isset($data[4]) && is_numeric($data[4]) && $data[4] < 0.03937) {
                $total_dry_days++;
            }
        }
        // Close the CSV file
        fclose($handle);

    } else {
        $total_dry_days = 'Error';
    }*/

    $total_dry_day = 'X';


    //Temperature
    
    //Read daily temp file
    $file_t_d = file('./RID/' . $RID . '/' . $RID . '_temp_d.txt');
    $mean_t_d = round($file_t_d[0], 0);
    $max_t_d = round($file_t_d[1], 0);
    $min_t_d = round($file_t_d[2], 0);
    $year_t = $file_t_d[3];
    $monthNum_t = intval($file_t_d[4]);

    //Read monthly temp avg file
    $file_t = file('./RID/' . $RID . '/' . $RID . '_temp.csv');
    if (!empty($file_t)) {
        $fields_t = str_getcsv($file_t[count($file_t) - 1]); // Parse csv string into an array, get fields from last line
        $mean_t_m = (round(floatval($fields_t[count($fields_t) - 2])));
        $monthNum_t_m = $fields_t[count($fields_t) - 3];
        $year_t_m = (round($fields_t[count($fields_t) - 4], 0));

    } else {
        echo "Error";
    }
    ;

    $dateObj_t_m = DateTime::createFromFormat('!m', intval($monthNum_t_m));
    $monthName_t_m = $dateObj_t_m->format('F');

    $thisMonth_t_m = $monthName_t_m . ', ' . $year_t_m;

    $file_t_max = file('./RID/' . $RID . '/' . $RID . '_temp_max.csv');
    if (!empty($file_t_max)) {
        $fields_t_max = str_getcsv($file_t_max[count($file_t_max) - 1]); // Parse csv string into an array, get fields from last line
        $max_t_m = (round(floatval($fields_t_max[count($fields_t_max) - 3]))); //RF value from last row of csv file
    
    } else {
        echo "Error";
    }
    ;

    $file_t_min = file('./RID/' . $RID . '/' . $RID . '_temp_min.csv');
    if (!empty($file_t_min)) {
        $fields_t_min = str_getcsv($file_t_min[count($file_t_min) - 1]); // Parse csv string into an array, get fields from last line
        $min_t_m = (round(floatval($fields_t_min[count($fields_t_min) - 3]))); //RF value from last row of csv file
    
    } else {
        echo "Error";
    }
    ;


    $dateObj_t = DateTime::createFromFormat('!m', $monthNum_t);
    $monthName_t_d = $dateObj_t->format('F'); // March
    $date_t = $monthName_t_d . ' ' . $file_t_d[5] . ', ' . $file_t_d[3];


    //Temperature monthly averages
    $csv_t = fopen('./RID/' . $RID . '/' . $RID . '_t_month.csv', 'r');
    while ($row_t = fgetcsv($csv_t)) {
        if ($row_t[3] == $monthName_t_d) {
            $avg_t = (round($row_t[count($row_t) - 1], 2));
        }
    }

    fclose($csv_t);

    //Above/below average style formatting
    if ($mean_t_d > $avg_t) {
        $status_t = 'above';
        $style_t = 'style="vertical-align:middle;position:absolute;color:orange;"';
        $stat_t = '+';
    } else {
        $status_t = 'below';
        $style_t = 'style="vertical-align:middle;position:absolute;color:green;" ';
        $stat_t = '';
    }
    //Temperature difference
    $dif_t_d = sprintf("%+.2f", ($mean_t_d - $avg_t));
    $dif_t_m = sprintf("%+.2f", ($mean_t_m - $avg_t));

    $file_et = file('./RID/' . $RID . '/' . $RID . '_et.csv');
    if (!empty($file_et)) {
        $fields_et = str_getcsv($file_et[count($file_et) - 1]); // Parse csv string into an array, get fields from last line
        $et = (round($fields_et[count($fields_et) - 2], 2)); // print last field
        $monthNum_et = round($fields_et[count($fields_et) - 3], 0);
        $year_et = (round($fields_et[count($fields_et) - 4], 0));

    } else {
        echo "Error";
    }
    ;


    $dateObj_et = DateTime::createFromFormat('!m', $monthNum_et);
    $monthName_et = $dateObj_et->format('F'); // March
    

    $csv_et = fopen('./RID/' . $RID . '/' . $RID . '_et_month.csv', 'r');

    // Keep looping as long as we get a new $row
    while ($row_et = fgetcsv($csv_et)) {
        if ($row_et[3] == $monthName_et) {
            $avg_et = (round($row_et[count($row_et) - 1], 2));
        }
    }

    // Don't forget to close the file!
    fclose($csv_et);

    if ($et >= $avg_et) {
        $status_et = 'above';
        $style_et = 'style="color:orange;"';
    } else {
        $status_et = 'below';
        $style_et = 'style="color:green;"';
    }

    $dif_et = sprintf("%+.2f", ($et - $avg_et) / $avg_et * 100, 2);


    $file_ndvi = file('./RID/' . $RID . '/' . $RID . '_ndvi.csv');
    if (!empty($file_ndvi)) {
        $fields_ndvi = str_getcsv($file_ndvi[count($file_ndvi) - 1]); // Parse csv string into an array, get fields from last line
        $ndvi = (round($fields_ndvi[count($fields_ndvi) - 2], 2)); // print last field
        $monthNum_ndvi = round($fields_ndvi[count($fields_ndvi) - 3], 0);
        $year_ndvi = (round($fields_ndvi[count($fields_ndvi) - 4], 0));

    } else {
        echo "Error";
    }
    ;


    $dateObj_ndvi = DateTime::createFromFormat('!m', intval($monthNum_ndvi));
    $monthName_ndvi = $dateObj_ndvi->format('F'); // March
    

    $csv_ndvi = fopen('./RID/' . $RID . '/' . $RID . '_ndvi_month.csv', 'r');

    // Keep looping as long as we get a new $row
    $avg_ndvi = 0;
    while ($row_ndvi = fgetcsv($csv_ndvi)) {
        if ($row_ndvi[3] == $monthName_ndvi) {
            $avg_ndvi = (round($row_ndvi[count($row_ndvi) - 1], 2));
        }
    }

    // Don't forget to close the file!
    fclose($csv_ndvi);

    if ($ndvi >= $avg_ndvi) {
        $status_ndvi = 'above';
        $style_ndvi = 'style="color:green;"';
    } else {
        $status_ndvi = 'below';
        $style_ndvi = 'style="color:orange;"';
    }

    $dif_ndvi = sprintf("%+.2f", ($ndvi - $avg_ndvi), 2);

    //SPI
    $file_spi = "./RID/" . $RID . "/" . $RID . "_spi.csv";
    $max = count(file($file_spi, FILE_SKIP_EMPTY_LINES));
    $min = $max - 13;

    $csv_spi = fopen($file_spi, "r");

    $array_spi = [];

    while ($data = fgetcsv($csv_spi)) {
        if ($data[0] >= $min && $data[0] <= $max) {
            array_push($array_spi, floatval($data[3]));
        }

    }



    //Count how many months in last year is in drought (<0)
    $d = 0;
    foreach ($array_spi as $value) {
        if ($value < 0) {
            $d++;
        }
    }

    $spi = end($array_spi);
    fclose($csv_spi);

    //Drought status
    if ($spi <= -2) {
        $drought_status = "Exceptional Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:red; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -1.6 && $spi > -2) {
        $drought_status = "Extreme Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:red; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -1.3 && $spi > -1.6) {
        $drought_status = "Severe Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:darkorange; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -0.8 && $spi > -1.3) {
        $drought_status = "Moderate Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:orange; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -0.5 && $spi > -0.8) {
        $drought_status = "Abnormally Dry";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:orange; display:inline-block; vertical-align: middle"';
    } else {
        $drought_status = "No Drought";
        $icon_spi = 'class="bi bi-check-circle-fill fs-3" style="color:green; display:inline-block;vertical-align: middle"';
    }



    //ONI
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

    if (date("d") < 8) {
        $m = date("m") - 1;
    } else {
        $m = date("m");
    }

    $month = DateTime::createFromFormat('!m', $m);
    $dateObj = DateTime::createFromFormat('!m', intval($m));
    $monthName = $dateObj->format('F');
    $monthName_abbrev = $dateObj->format('M');

    //Open query file
    $csv_query = fopen("./RID/" . $RID . "/" . $RID . "_query.csv", 'r');

    while ($query = fgetcsv($csv_query)) {
        if ($query[1] == $m && $query[3] == $phase) {
            $MRF = round($query[2], 2);
            $MeRF = round($query[5], 2);
            $MnRF = round($query[6], 2);

        }
    }

    fclose($csv_query);
    ?>
    <div class="grid-container">
        <header class="header" id="header">
        </header>
        <aside id="sidebar" class="animated bounceInDown">
            <p style="padding-left: 1%;font-size:1.5em"> Menu </p>
            <ul style="padding-left:5px">
                <li><a href="#dashboard">Dashboard</a></li>
                <li><a href="#rainOutlook">Rainfall Outlook</a></li>
                <li><a href="#tool">Decision Support Tool</a></li>
                <li class='sub-menu'><a href='#settings'>Average Climate Conditions<div class='fa fa-caret-down right'>
                        </div></a>
                    <ul>
                        <li><a href="#rf">Rainfall</a></li>
                        <li><a href="#temperature">Temperature</a></li>
                        <li><a href="#et">Evapotranspiration</a></li>
                        <li><a href="#ndvi">NDVI</a></li>
                        <li><a href="#drought">Drought</a></li>
                    </ul>
                </li>
                <!--<li><a href="#data">Historical Data</a></li>-->
            </ul>

        </aside>

        <script>
            $('.sub-menu ul').hide();
            $(".sub-menu a").click(function () {
                $(this).parent(".sub-menu").children("ul").slideToggle("100");
                $(this).find(".right").toggleClass("fa-caret-up fa-caret-down");
            });
        </script>


        <div class="anchor" id="dashboard"></div>
        <main class="main">

            <div id="ranchname">
                <?php echo $RID ?> - Ranch Page
            </div>
            
            <!--<div class="mobile-msg">
                <p> H-RIP is currently only available on desktop. The mobile version is coming soon.</p>
            </div>-->

            <div class="for-mobile">
                <div class="subtitleB" style="padding-top: 5px">Dashboard</div>
                <div id="dashboard" class="card-margin">
                    <div class="dashboardCard" id="rain">
                        <div class="box-left">
                            <div class="table" style="text-align: center;">
                                <p> Rainfall </p>
                                <br>
                                <i class="bi bi-cloud-rain" style="background-color: #3d89f7;"></i>
                                <br>
                                <div>
                                    <form class="switchButton">
                                        <div class="switch-field">
                                            <input type="radio" id="radio-one" name="switch-one" value="daily_r"
                                                checked />
                                            <label for="radio-one">Daily</label>
                                            <input type="radio" id="radio-two" name="switch-one" value="monthly_r" />
                                            <label for="radio-two">Monthly</label>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="box-right">

                            <div class='area' id="daily_r">

                                <i class="bi bi-question-circle tool" style="float:right">
                                    <div class="tooltip">
                                        <div class="tooltip-content">
                                            <p class='tooltip-header'>Daily Rainfall</p>
                                            <p>Total accumulated rainfall for yesterday.</p>
                                            <p><span class="bold">Consecutive dry days:</span> Number of days where
                                                rainfall
                                                has
                                                been consecutively under 0.04 inches in region</p>
                                        </div>
                                    </div>
                                </i>
                                <p class="date">
                                    <?php echo $date_rf ?>

                                </p>
                                <div class="box rel">
                                    <div class="data">
                                        <p class="index1">
                                            <?php echo $rf_d ?>
                                        </p>
                                        <p>Total Rainfall</p>
                                    </div>
                                    <div class="data" style="">
                                        <p class="index1">
                                            <?php echo $consec_dry_days ?>
                                        </p>
                                        <p> Consecutive Dry Days </p>
                                    </div>
                                </div>
                            </div>
                            <div class='area' id="monthly_r">
                                <i class="bi bi-question-circle tool" style="float:right">
                                    <div class="tooltip">
                                        <div class="tooltip-content">
                                            <p class='tooltip-header'>Monthly Rainfall</p>
                                            <p>Total accumulated rainfall for last month.
                                            <p>Percent difference between rainfall of the last month and the typical
                                                rainfall expected for that specific month.</p>
                                            <p><span class="bold">Total dry days: </span> Total days in month where
                                                rainfall
                                                was less than x inches in region</p>

                                        </div>
                                    </div>
                                </i>
                                <p class="date">
                                    <?php echo $thisMonth_rf ?>
                                </p>
                                <div class="box data big">
                                    <div style="text-align: center;">
                                        <span class="value" style="vertical-align:middle; font-size:2vw;">
                                            <?php echo $rf_m ?> in
                                        </span>
                                        <span style="color:<?php echo $color_rf_m ?>">
                                            <?php printf("%+.1f", $dif_m); ?>%
                                            </p>
                                        </span>
                                    </div>
                                    <p style="font-size:0.7vw;">Total Rainfall</p>
                                    <div class="status" style="text-align:center;">
                                        <i <?php echo $icon_rf_m ?>></i>
                                        <p style="display:inline-block; vertical-align:middle;font-size:0.8vw;">
                                            <?php echo $status_rf_m ?>
                                        </p>
                                        <br>

                                        <p style="font-size:0.8vw;"> <?php echo $total_dry_days ?> total dry days </p>
                                    </div>
                                </div>

                            </div>



                        </div>
                    </div>
                    <div class="dashboardCard" id="temp">
                        <div>
                            <div class="box-left">
                                <div class="table" style="">
                                    <p> Temperature </p>
                                    <br>

                                    <i class="bi bi-thermometer-half" style="background-color: #f03737;"></i>
                                    <br>
                                    <div>
                                        <form class="switchButton">
                                            <div class="switch-field">
                                                <input type="radio" id="radio-three" name="switch-two" value="daily_t"
                                                    checked />
                                                <label for="radio-three">Daily</label>
                                                <input type="radio" id="radio-four" name="switch-two"
                                                    value="monthly_t" />
                                                <label for="radio-four">Monthly</label>
                                            </div>

                                        </form>
                                    </div>
                                </div>
                            </div>
                            <div class="box-right">
                                <div class='area1' id="daily_t">
                                    <i class="bi bi-question-circle tool" style="float:right">
                                        <div class="tooltipRight">
                                            <div class="tooltip-content">
                                                <p class='tooltip-header'>Daily temperature</p>
                                                <p>Yesterday's average, minimum, and maximum temperature. Difference is
                                                    in
                                                    comparison to the average monthly temperature.</p>
                                            </div>
                                        </div>
                                    </i>
                                    <p class="date">
                                        <?php echo $date_t; ?>
                                    </p>

                                    <div class="box data big">
                                        <div style="line-height:2em;text-align:center">
                                            <span class="value" style="vertical-align:middle;">
                                                <?php echo $mean_t_d . '&deg;F ' ?>
                                            </span>
                                            <span>
                                                <?php echo $dif_t_d . '&deg;F ' ?>

                                            </span>
                                        </div>
                                        <p>Daily Temperature</p>
                                        <div class="status" style="text-align:center">
                                            <p style="font-size: 0.8em;margin-top: 2%"> Min:
                                                <?php echo $min_t_d . '&deg;F' ?> Max:
                                                <?php echo $max_t_d . '&deg;F' ?>
                                            </p>
                                        </div>
                                    </div>

                                </div>
                                <div class='area1' id="monthly_t">
                                    <i class="bi bi-question-circle tool" style="float:right">
                                        <div class="tooltipRight">
                                            <div class="tooltip-content">
                                                <p class='tooltip-header'>Monthly temperature</p>
                                                <p>Last month's average, minimum, and maximum temperature. Difference is
                                                    in
                                                    comparison to the average temperature for that particular month.</p>
                                            </div>
                                        </div>
                                    </i>
                                    <p class="date">
                                        <?php echo $thisMonth_t_m ?>

                                    </p>
                                    <div class="box data big">
                                        <div style="line-height:2em;text-align:center">
                                            <span class="value" style="vertical-align:middle;">
                                                <?php echo $mean_t_m . '&deg;F ' ?>
                                            </span>
                                            <span>
                                                <?php echo $dif_t_m . '&deg;F ' ?>
                                                </p>
                                            </span>
                                        </div>
                                        <p>Monthly Temperature</p>
                                        <div class="status" style="text-align:center">
                                            <p style="font-size: 0.8em;margin-top: 2%"> Min:
                                                <?php echo $min_t_m . '&deg;F' ?> Max:
                                                <?php echo $max_t_m . '&deg;F' ?>
                                            </p>
                                        </div>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="dashboardCard" style="display: table; height:95%">
                        <div class="table rel">
                            <p style="font-size:20px;display:inline-block;">12-Month Drought History </p>
                            <i class="bi bi-question-circle tool pos">
                                <div class="tooltip">
                                    <div class="tooltip-content">
                                        <p>Drought history uses the 3-month Standard Precipitation Index (SPI) to
                                            determine
                                            drought.
                                        </p>

                                        <p>If <span class="bold">SPI&lt; 0</span>, the area is in drought. The lower the
                                            number, the higher the drought intensity.</p>
                                        <p>Mouse over the chart to view specific values.</p>
                                    </div>
                                </div>
                            </i>
                            <p>
                                <?php echo $d; ?> out of 12 months in drought
                            </p>
                            <div id="SPI-12m" style="height:80%"></div>
                        </div>
                    </div>
                    <div class="dashboardCard">
                        <i class="bi bi-question-circle tool" style="float:right">
                            <div class="tooltipRight">
                                <div class="tooltip-content">
                                    <p>Drought severity indicator is based on the current Standard Precipitation Index
                                        (SPI). </p>

                                    <table id="droughtTable">
                                        <colgroup>
                                            <col span="1" style="width: 45%;">
                                            <col span="1" style="width: 55%;">
                                        </colgroup>
                                        <tr>
                                            <td>-0.5 to -0.79:</td>
                                            <td>Abnormally Dry</td>
                                        </tr>
                                        <tr>
                                            <td>-0.8 to -1.29:</td>
                                            <td>Moderate Drought</td>
                                        </tr>
                                        <tr>
                                            <td>-1.3 to -1.59:</td>
                                            <td>Severe Drought</td>
                                        </tr>
                                        <tr>
                                            <td>-1.6 to -1.99:</td>
                                            <td>Extreme Drought</td>
                                        </tr>
                                        <tr>
                                            <td>-2 or less:</td>
                                            <td>Exceptional Drought</td>
                                        </tr>
                                    </table>

                                    <!--<span class="bold">Less than -2:</span> Extreme Drought<br>
                                <span class="bold">-1.5 to -2:</span> Severe Drought<br>
                                <span class="bold">-1 to -1.5:</span> Moderate Drought<br>
                                <span class="bold">More than -1:</span> Mild Drought-->

                                </div>
                            </div>
                        </i>

                        <div id="spi">
                            <p class="spi">Current Drought Severity</p>
                            <p class="spi"> <span <?php echo $icon_spi ?>></span>
                                <?php echo $drought_status; ?>
                            </p>
                        </div>
                    </div>
                    <div class="dashboardCard" style="display: table;">
                        <div class="table rel">
                            <i class="bi bi-question-circle tool pos" style="z-index:0">
                                <div class="tooltipRight">
                                    <div class="tooltip-content">
                                        <p>Current ENSO Conditions are determined using the ONI Index.</p>
                                        <p><span class="bold">During an El Niño: </span> Typically wet summers and dry
                                            winters<br>
                                        </p>
                                        <p><span class="bold">During a La Niña: </span>Typically dry summers and wet
                                            winters
                                        </p>
                                    </div>
                                </div>
                            </i>

                            <div style="text-align:center; ">
                                <img style="width: 80%;height:auto;" src="./gauge/gauge.png">
                                <p>
                                    <?php echo ($monthName) ?> ENSO Conditions:
                                    <br>
                                    <span style="font-weight: 800">
                                        <?php echo ($phase_name) ?>
                                    </span>
                                    <br>
                                <p style="margin-top: 5%;">Monthly Rainfall</p>
                                <table id="oni-table" style="">
                                    <colgroup>
                                        <col span="1" style="width: 65%;">
                                        <col span="1" style="width: 35%;">
                                    </colgroup>
                                    <tr>
                                        <td>Historical Avg</td>
                                        <td>
                                            <?php echo $MRF; ?> in.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <?php echo $monthName_abbrev . ' ' . $phase_name; ?> Avg
                                        </td>
                                        <td>
                                            <?php echo $MeRF; ?> in.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <?php echo $monthName_abbrev . ' ' . $phase_name; ?> Min
                                        </td>
                                        <td>
                                            <?php echo $MnRF; ?> in.
                                        </td>
                                    </tr>
                                </table>
                            </div>

                        </div>
                    </div>
                </div>
                <div class="anchor" id="rainOutlook"></div>
                <div id="rainOutlook-content">
                    <p class="subtitleB">Rainfall Outlook</p>
                    <img id="gauge" src="./gauge/gauge.png"
                        style="width: 30%; display: block; margin-left: auto;margin-right: auto;">
                    <div id="rainProj">
                        <p style="font-size: 20px">ENSO Almanac: 3-Month Rainfall Outlook</p>
                        <a href="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_rainfall.png"
                            style="color:inherit" target="_blank">
                            <img class="shadow" style=""
                                src="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_rainfall.png"></a>
                    </div>
                </div>
                <div class="anchor" id="tool"></div>
                <div id="tool-content">
                    <p class="subtitleB">Forage Production Decision Support Tool</p>
                    <div id="input">

                        <form id="toolForm" method="post">
                            Select the following for your location and click submit:
                            <br><br>
                            Grass Type: <select class="question" id="grasstype" name="grasstype">
                                <option value="Kikuyu" <?php if (isset($_POST['grasstype']) && $_POST['grasstype'] == 'Kikuyu grass')
                                    echo ' selected="selected"'; ?>>
                                    Kikuyu Grass</option>
                                <option value="Pangola" <?php if (isset($_POST['grasstype']) && $_POST['grasstype'] == 'Pangola grass')
                                    echo ' selected="selected"'; ?>>
                                    Pangola Grass</option>
                                <option value="Buffel" <?php if (isset($_POST['grasstype']) && $_POST['grasstype'] == 'Buffel grass')
                                    echo ' selected="selected"'; ?>>
                                    Buffel Grass</option>
                                <option value="Signal" <?php if (isset($_POST['grasstype']) && $_POST['grasstype'] == 'Signal grass')
                                    echo ' selected="selected"'; ?>>
                                    Signal Grass</option>
                                <option value="Guinea" <?php if (isset($_POST['grasstype']) && $_POST['grasstype'] == 'Guinea grass')
                                    echo ' selected="selected"'; ?>>
                                    Guinea Grass</option>
                            </select>
                            <br><br>
                            Forage Condition: <select class="question" id="condition" name="condition">
                                <option value="Improved" <?php if (isset($_POST['condition']) && $_POST['condition'] == 'Improved')
                                    echo ' selected="selected"'; ?>>
                                    Improved</option>
                                <option value="Unimproved" <?php if (isset($_POST['condition']) && $_POST['condition'] == 'Unimproved')
                                    echo ' selected="selected"'; ?>>
                                    Unimproved</option>
                            </select>

                            <input type="button" id="submit" onclick=" showDiv(); SubmitFormData();" value="Submit" />
                        </form>
                    </div>
                    <div id="results" style="display:none;height:auto">
                    </div>

                    <div class="anchor" id="rf"></div>
                    <p class="subtitleB">Average Climate Conditions</p>
                    <div class="name">
                        <p>Rainfall</p>
                    </div>
                    <div class="main_cards card-margin">
                        <div class="card" id="RF-div"></div>
                        <div class="card center">
                            <div style="line-height:2em;text-align:center">
                                <span class="value" style="vertical-align:middle;">
                                    <?php echo $rf_m ?> in
                                </span>
                                <span style="color:<?php echo $color_rf_m ?>">
                                    <?php //echo $stat_rf_m;
                                    printf("%+.1f", $dif_m) ?>%
                                    </p>
                                </span>
                            </div>

                            <div class="status">
                                <i <?php echo $icon_rf_m ?>></i>
                                <p style="">
                                    <?php echo $status_rf_m ?>
                                </p>

                            </div>
                            <div> <?php echo $total_dry_days ?> total dry days</div>
                            <div style="text-align: center;margin-top:2%; ">
                                <p style="font-style:italic; color: #696969">
                                    <?php echo $thisMonth_rf ?>
                                </p>
                                <p style="font-size:12px;color: #696969">Monthly Rainfall</p>
                            </div>
                        </div>
                        <div class="card center">
                            <div style="line-height:2em;text-align:center">
                                <span class="value" style="vertical-align:middle;">
                                    <?php echo $rf_d ?> in
                                </span>
                                <span style="color:<?php echo $color_rf_m ?>">
                                    <!--<?php echo $stat_rf_d;
                                    echo $dif_d ?>%
                                    <?php echo printf("%+.1f", $dif_d) ?>%-->
                                    </p>
                                    </p>
                                </span>
                            </div>
                            <div class="status">
                                <i <?php echo $icon_rf_m ?>></i>
                                <p style="display:inline-block; vertical-align:middle">
                                    <?php echo $status_rf_m ?>
                                </p>

                            </div>
                            <div> <?php echo $consec_dry_days?> consec. dry days</div>
                            <div style="text-align: center;margin-top:2%;">

                                <p style="font-style:italic; color: #696969">
                                    <?php echo $date ?>
                                </p>
                                <p style="font-size:12px;color: #696969">Daily Rainfall</p>
                            </div>
                        </div>
                        <div class="card">
                            <a class="map-img"
                                href="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_rf.png"
                                style="color:inherit" target="_blank">
                                <img style=""
                                    src="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_rf.png"></a>
                        </div>

                    </div>
                    <div class="hist" id="RF-hist"></div>
                    <div class="anchor" id="temperature"></div>
                    <div class="name">
                        <p>Temperature</p>
                    </div>
                    <div class="main_cards card-margin">
                        <div class="card" id="temp-div"></div>
                        <div class="card center">
                            <div style="line-height:2em;text-align:center">
                                <span class="value" style="vertical-align:middle;">
                                    <?php echo $mean_t_d ?>&degF
                                </span>
                                <span>
                                    <?php echo $dif_t_d ?> &degF
                                </span>
                            </div>

                            <div class="diff_temp">

                            </div>
                            <div style="text-align: center; padding-top: 10px;">
                                <p>Daily Average Temperature</p>
                                <p style="font-style:italic; color: #696969;">
                                    <?php echo $date_t ?>
                                </p>
                            </div>

                        </div>
                        <div class="card center">
                            <p style="text-align:center"> Max temperature:<br><span style="font-size: 1.5vw">
                                    <?php echo $max_t_d . '&degF'; ?>
                                </span><br> Min temperature:<br><span style="font-size: 1.5vw">
                                    <?php echo $min_t_d . '&degF'; ?>
                                </span><br>
                                <span style="font-style:italic; color: #696969">
                                    <?php echo $date_t ?>
                                </span>
                            </p>
                        </div>
                        <div class="card">
                            <a class="map-img"
                                href="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_temp.png"
                                style="color:inherit" target="_blank">
                                <img style=""
                                    src="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_temp.png"></a>
                        </div>
                    </div>

                    <div class="anchor" id="et"></div>
                    <div class="name">
                        <p>Evapotranspiration</p>
                    </div>
                    <div class="et_cards card-margin">
                        <div class="card1" id="ET-div"></div>
                        <div class="card1 center">
                            <div class="value">
                                <?php echo $et ?> mm/day
                            </div>
                            <div class="diff_temp">
                                <p><span <?php echo $style_et . '>' . $dif_et . '%</span> ' . $status_et ?> monthly
                                        average</p>
                            </div>
                            <div style="text-align: center; margin-top: 2%;">
                                <p>Monthly Average Evapotranspiration</p>
                                <p style="font-style:italic; color: #696969">
                                    <?php echo $monthName_et . ', ' . $year_et ?>
                                </p>
                            </div>
                        </div>

                        <div class="card1">
                            <a class="map-img"
                                href="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_et.png"
                                style="color:inherit" target="_blank">
                                <img style=""
                                    src="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_et.png"></a>

                        </div>
                        <div class="card1">
                            <p> Evapotranspiration is the combination of processes that takes water from the surface
                                and transforms it into water vapor in the air. These processes include the movement
                                of water through plant roots and the evaporation of that water through pores in the
                                plant's leaves, a process called transpiration. To learn more, click <a
                                    href="http://evapotranspiration.geography.hawaii.edu/" target="_blank"
                                    style="color:blue;text-decoration:underline">here</a>. <span
                                    style="font-style: italic;">Source: <a href="https://earthengine.google.com/">Google
                                        Earth
                                        Engine</a></span>
                            </p>
                        </div>
                    </div>
                    <div class="hist" id="ET-hist">
                    </div>

                    <div class="anchor" id="ndvi"></div>
                    <div class="name">
                        <p>Normalized Difference Vegetation Index (NDVI)</p>
                    </div>
                    <div class="et_cards card-margin">
                        <div class="card1" id="NDVI-div"></div>

                        <div class="card1 center">
                            <div class="value">
                                <?php echo $ndvi ?>
                            </div>
                            <div class="diff_temp">
                                <p>
                                    <?php echo '<span ' . $style_ndvi . '>' . $dif_ndvi . '</span> ' . $status_ndvi ?>
                                    monthly
                                    average
                                </p>
                            </div>
                            <div style="text-align: center; margin-top: 2%;">
                                <p>Monthly Average NDVI</p>
                                <p style="font-style:italic; color: #696969">
                                    <?php echo $monthName_ndvi . ', ' . $year_ndvi ?>
                                </p>
                            </div>

                        </div>
                        <div class="card1">
                            <a class="map-img"
                                href="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_ndvi.png"
                                style="color:inherit" target="_blank">
                                <img style=""
                                    src="./RID/<?php echo $_GET["ranch"] ?>/<?php echo $_GET["ranch"] ?>_ndvi.png"></a>
                        </div>
                        <div class="card1">
                            <p>Normalized Difference Vegetation Index (NDVI) is a widely used vegetation index that
                                measures the
                                density of green in a region and is often used to monitor drought, forecast agricultural
                                production, and more. Values range from +1.0 to -1.0. High NDVI values (approximately
                                0.6 to
                                0.9) suggest dense vegetation such as crops at their peak growth.</p>
                        </div>
                    </div>
                    <div class="hist" id="NDVI-hist"></div>
                    <div class="anchor" id="drought"></div>
                    <div class="name">
                        <p>Drought History (SPI-3)</p>
                    </div>
                    <div id="SPI-div" class="hist"></div>

                    <br>
                    <br>


                    <script>
                        var input = document.getElementById("input");
                        input.addEventListener("keydown", function (e) {
                            if (e.key === "Enter") {
                                e.preventDefault();
                                document.getElementById("submit").click();
                            }
                        });

                        function SubmitFormData() {
                            var grasstype = $("#grasstype").val();
                            var condition = $("#condition").val();
                            var ranch = '<?php echo $_GET["ranch"] ?>';


                            $.post("tool.php?ranch=<?php echo $_GET["ranch"] ?>", {
                                grasstype: grasstype,
                                condition: condition,
                                ranch: ranch,

                            },
                                function (data) {
                                    $('#results').html(data);
                                });
                        }


                        function showDiv() {
                            document.getElementById('results').style.display = "block";
                        }

                        function popupFunction() {
                            var popup = document.getElementById("myPopup");
                            popup.classList.toggle("show");
                        }
                    </script>
                </div>
                <div class="anchor" id="data"></div>
                </div>

                <!--<div id="data-content">
                <p class="subtitleB">Historical Data</p>
                <p style="text-align: center"> Drought History (Standard Precipitation Index-3 months)</p>
                <div id="SPI-div" class="shadow" style="width: 80%;margin: 5% auto;"></div>
                <div class="wrapperHist">
                    <div id="rainHist" class="graphHist">
                        <p class="dataTitles">Average Rainfall and Temperature</p>
                        <img class="shadow"
                            src=" ./fromRyan/<?php //echo $_GET["ranch"]?>/<?php echo $_GET["ranch"] ?>_Climograph.png">
                    </div>
                    <span></span>
                    <div id="droughtHist" class="graphHist">
                        <p class="dataTitles">100-year Rainfall Trends</p>
                        <img class="shadow"
                            src="./fromRyan/<?php //echo $_GET["ranch"]?>/<?php echo $_GET["ranch"] ?>_RF_Trend.png">
                    </div>
                </div>

                    
            </div>-->


                <script>
                    document.addEventListener("DOMContentLoaded", function () {
                        document.querySelectorAll('.sidebar .nav-link').forEach(function (element) {

                            element.addEventListener('click', function (e) {

                                let nextEl = element.nextElementSibling;
                                let parentEl = element.parentElement;

                                if (nextEl) {
                                    e.preventDefault();
                                    let mycollapse = new bootstrap.Collapse(nextEl);

                                    if (nextEl.classList.contains('show')) {
                                        mycollapse.hide();
                                    } else {
                                        mycollapse.show();
                                        // find other submenus with class=show
                                        var opened_submenu = parentEl.parentElement.querySelector(
                                            '.submenu.show');
                                        // if it exists, then close all of them
                                        if (opened_submenu) {
                                            new bootstrap.Collapse(opened_submenu);
                                        }
                                    }
                                }
                            }); // addEventListener
                        }) // forEach
                    });
                </script>


        </main>

    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            document.querySelectorAll('.sidebar .nav-link').forEach(function (element) {

                element.addEventListener('click', function (e) {

                    let nextEl = element.nextElementSibling;
                    let parentEl = element.parentElement;

                    if (nextEl) {
                        e.preventDefault();
                        let mycollapse = new bootstrap.Collapse(nextEl);

                        if (nextEl.classList.contains('show')) {
                            mycollapse.hide();
                        } else {
                            mycollapse.show();
                            // find other submenus with class=show
                            var opened_submenu = parentEl.parentElement.querySelector(
                                '.submenu.show');
                            // if it exists, then close all of them
                            if (opened_submenu) {
                                new bootstrap.Collapse(opened_submenu);
                            }
                        }
                    }
                }); // addEventListener
            }) // forEach
        });
    </script>
    <script type="text/javascript">
        var ranch = '<?php echo $_GET["ranch"] ?>';
    </script>
    <script>
        $("input[name$='switch-one']").click(function () {
            $('.area').hide();
            $('#' + $(this).val()).show();
            console.log($(this).val());
        });

        $("input[name$='switch-two']").click(function () {
            $('.area1').hide();
            $('#' + $(this).val()).show();
            console.log($(this).val());
        });

        var RID = '<?php echo $_GET["ranch"] ?>';
    </script>
    <script src="plotly.js"></script>

</body>