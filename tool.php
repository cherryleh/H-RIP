<?php 

#echo $_POST['grasstype'];
#echo $_POST['drymatter'];
#echo $_POST['animalunits'];
#echo $_POST['acres'];
// define variables and set to empty values
$grasstype = $condition  = "";
$grasstype=($_POST["grasstype"]);
$condition=($_POST["condition"]);
$ranch = ($_POST["ranch"]);

$date = new DateTime("now", new DateTimeZone('Pacific/Honolulu') );

$thismonth = strtoupper($date->format('M'));
$thismonthnum = ($date->format('m'));
$thisyear = ($date->format('Y'));
$thisdate = ($date->format('d'));
//Number of days this month
$numberdays = cal_days_in_month(CAL_GREGORIAN, $thismonthnum, $thisyear);

$currentmonth = date('F');
$lastmonth = date('F', strtotime($currentmonth . " last month"));


if ($thisdate < 8){
    $monthtitle = $lastmonth;}
else{
    $monthtitle = $currentmonth;
}



//Return next month in all caps 3 letters
//$nm = new DateTime( "now", new DateTimeZone('Pacific/Honolulu') );
//$nm->modify( 'next month' );
//$nextmonth = strtoupper($nm->format( 'M' ));


$file = file("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt");
$explode = explode(" ",end($file));
$oni = end($explode);

//Determine current ENSO state
if ($oni > 1.1) {
    $ENSO = "SEL";
    $cond = "Strong El Ni&#241;o";
} elseif (1.1 >= $oni && $oni>= 0.5){
    $ENSO = "WEL";
    $cond = "Weak El Ni&#241;o";
} elseif (0.5>=$oni&&$oni>=-0.5){
    $ENSO = "NUT";
    $cond = "Neutral";
} elseif (-0.5>$oni && $oni>=-1.1){
    $ENSO="WLA";
    $cond = "Weak La Ni&#241;a";
} elseif ($oni < -1.1){
    $ENSO="SLA";
    $cond = "Strong La Ni&#241;a";
} else {
    echo "Error";
}


$arg = [$ranch, $grasstype, $condition];

$command = escapeshellcmd('python3 ./Python/528.py '.$ranch.' '.$grasstype.' '.$condition );

$a = shell_exec($command);

echo($a);



?>