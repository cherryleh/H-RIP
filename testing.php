<?php

$RID = "RID115";


$file_t_d = file('./RID/' . $RID . '/' . $RID . '_temp_d.txt');
$mean_t_d = round($file_t_d[0], 0);
$max_t_d = round($file_t_d[1], 0);
$min_t_d = round($file_t_d[2], 0);
$year_t_d = $file_t_d[3];
$monthNum_t_d = intval($file_t_d[4]);

$dateObj_t = DateTime::createFromFormat('!m', $monthNum_t_d);
$monthName_t_d = $dateObj_t->format('F'); // March
$date_t = $monthName_t_d . ' ' . $file_t_d[5] . ', ' . $file_t_d[3];

//Monthly
$file_t_m = file('./RID/' . $RID . '/' . $RID . '_temp_m.txt');
$mean_t_m = round($file_t_m[0], 0);
$max_t_m = round($file_t_m[1], 0);
$min_t_m = round($file_t_m[2], 0);
$year_t_m = $file_t_m[3];
$monthNum_t_m = intval($file_t_m[4]);

$dateObj_t_m = DateTime::createFromFormat('!m', intval($monthNum_t_m));
$monthName_t_m = $dateObj_t_m->format('F');


$csv_t = fopen('./RID/' . $RID . '/' . $RID . '_t_month.csv', 'r');
while ($row_t = fgetcsv($csv_t)) {
    if ($row_t[3] == $monthName_t_d) {
        $avg_t_yest = (round($row_t[count($row_t) - 1], 2)); 
    }
    if ($row_t[3] == $monthName_t_m) {
        $avg_t_lastM = (round($row_t[count($row_t) - 1], 2)); 
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
$dif_t_d = sprintf("%+.2f", ($mean_t_d - $avg_t_yest));
$dif_t_m = sprintf("%+.2f", ($mean_t_m - $avg_t_lastM));

echo $dif_t_d;
echo $dif_t_m;
?>