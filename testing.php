<?php

$RID = "RID115";

$rf_daily_month = './RID/' . $RID . '/' . $RID . '_rf_daily_last_month.csv';

// Open the CSV file
if (($handle = fopen($rf_daily_month, "r")) !== FALSE) {
    $total_dry_days = 0;
    //$header = fgetcsv($handle); // Read the header row
    // Loop through each row of the CSV
    while (($data = fgetcsv($handle)) !== FALSE) {
        // Check if the value in the target column is less than 1
        if (isset($data[3]) && is_numeric($data[3]) && $data[3] < 0.03937) {
            $total_dry_days++;
        }
    }
    // Close the CSV file
    fclose($handle);

} else {
    $total_dry_days = 'Error';
}
echo $total_dry_days;
?>