
    <?php
    //Temperature monthly averages
    $RID = "RID097";
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
    $date_rf_m = $monthName_rf_m . ', ' . $year_rf_m;
    
    echo $monthNum_rf_m;

?>