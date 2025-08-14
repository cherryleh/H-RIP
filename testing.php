<?php
//rainfall
$RID = "RID097";

echo $RID;
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

//Daily Rainfall
$file_rf_d = file('./RID/' . $RID . '/' . $RID . '_rf_d.txt');
$rf_d = round($file_rf_d[0], 2);
echo $rf_d;
$year_rf = $file_rf_d[1];
$monthNum_rf_d = intval($file_rf_d[2]);

//Date reformat
$dateObj_rf = DateTime::createFromFormat('!m', $monthNum_rf_d);
$monthName_rf_d = $dateObj_rf->format('F'); // March
$date_rf_d = $monthName_rf_d . ' ' . $file_rf_d[3] . ', ' . $file_rf_d[1];

echo $date_rf_d;

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

?>