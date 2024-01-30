<?php
$RID = "RID073";
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


fclose($csv_ndvi);

if ($ndvi >= $avg_ndvi) {
    $status_ndvi = 'above';
    $style_ndvi = 'style="color:green;"';
} else {
    $status_ndvi = 'below';
    $style_ndvi = 'style="color:orange;"';
}

$dif_ndvi = sprintf("%+.2f", ($ndvi - $avg_ndvi), 2);
echo $avg_ndvi;
?>
