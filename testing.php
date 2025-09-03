<?php
//rainfall
$RID = "RID097";
$file_t = file('./RID/' . $RID . '/' . $RID . '_tmean.csv');
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
echo $year_t_m;

?>