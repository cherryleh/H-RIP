
    <?php
    //Temperature monthly averages
    $RID = "RID066";
    $file_rf = file('./RID/' . $RID . '/' . $RID . '_rf.csv');
    // Get last row of monthly rainfall file
    //Monthly Rainfall
    if (!empty($file_rf)) {
        $fields_rf = str_getcsv($file_rf[count($file_rf) - 1]); // Parse csv string into an array, get fields from last line
        $rf_m = (round($fields_rf[count($fields_rf) - 2], 2)); //RF value from last row of csv file
        $monthNum_rf_m = $fields_rf[count($fields_rf) - 4]; //Month of last row (should be last month)
        $year_rf_m = (round($fields_rf[count($fields_rf) - 5], 0)); //Year of last row
    
    } else {
        echo "Error";
    };

    //Date reformat
    $dateObj_rf = DateTime::createFromFormat('!m', intval($monthNum_rf_m));
    $monthName_rf_m = $dateObj_rf->format('F'); // March
    $date_rf_m = $monthName_rf_m . ' , ' . $year_rf_m;

    //Daily Rainfall
    $file_rf_d = file('./RID/' . $RID . '/' . $RID . '_rf_d.txt');
    $rf_d = round($file_rf_d[0], 2);
    $year_rf = $file_rf_d[1];
    $monthNum_rf_d = intval($file_rf_d[2]);

    //Date reformat
    $dateObj_rf = DateTime::createFromFormat('!m', $monthNum_rf_d);
    $monthName_rf_d = $dateObj_rf->format('F'); // March
    $date_rf_d = $monthName_rf_d . ' ' . $file_rf_d[3] . ', ' . $file_rf_d[1];

    //Format: e.g. December, 2022
    //$thisMonth_rf = $monthName_rf . ', ' . $year_rf;
    //Open monthly averages file to get average for this month
    $csv_rf = fopen('./RID/' . $RID . '/' . $RID . '_rf_month.csv', 'r');

    // Keep looping as long as we get a new $row
    while ($row_rf = fgetcsv($csv_rf)) {
        if ($row_rf[2] == $monthName_rf_m) {
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
    if (($handle = fopen($rf_daily_month, "r")) !== FALSE) {
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
    }



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
        if ($row_t[3] == $monthName_t_m) {
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
        if ($value < -0.5) {
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