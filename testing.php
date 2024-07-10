<?php
$RID = "RID092";
$file_rf_d = file('./RID/' . $RID . '/' . $RID . '_rf_daily_this_month.csv');
    
if (!empty($file_rf_d)) {
    $fields_rf_d = str_getcsv($file_rf_d[count($file_rf_d) - 1]); // Parse csv string into an array, get fields from last line
    $rf_d = (round($fields_rf_d[count($fields_rf_d) - 1], 3)); //RF value from last row of csv file
    $monthDate_rf_d = $fields_rf_d[count($fields_rf_d) - 2]; //Date
    $monthNum_rf_d = $fields_rf_d[count($fields_rf_d) - 3];//Month of last row (should be last month)
    $year_rf_d = (round($fields_rf_d[count($fields_rf_d) - 4], 0)); //Year of last row
    
} else {
    echo "Error";
};

$dateObj_rf_d = DateTime::createFromFormat('!m', intval($monthNum_rf_d));
$monthName_rf_d = $dateObj_rf_d->format('F');
//$date_rf = $monthName_rf_d . ' ' . $monthDate_rf_d . ', ' . $year_rf_d;
echo $date_rf;

?>
