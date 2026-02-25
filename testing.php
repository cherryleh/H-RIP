<?php

$RID = "RID115";

//ONI
$oni_f = file("https://www.cpc.ncep.noaa.gov/data/indices/Rnino34.ascii.txt");
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