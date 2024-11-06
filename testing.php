
    <?php
    //Temperature monthly averages
    $RID = "RID066";
    

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

    
    echo $dif_t_d;
    
    ?>