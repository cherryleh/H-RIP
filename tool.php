<?php
// --- Get form inputs ---
$grasstype = $_POST["grasstype"] ?? "";
$condition = $_POST["condition"] ?? "";
$ranch     = $_POST["ranch"] ?? "";

// --- Date setup ---
date_default_timezone_set('Pacific/Honolulu');
$date = new DateTime();

$thismonth     = strtoupper($date->format('M'));
$thismonthnum  = (int)$date->format('m');
$thisyear      = (int)$date->format('Y');
$thisdate      = (int)$date->format('d');
$numberdays    = cal_days_in_month(CAL_GREGORIAN, $thismonthnum, $thisyear);

$currentmonth  = date('F');
$lastmonth     = date('F', strtotime($currentmonth . " last month"));
$monthtitle    = ($thisdate < 8) ? $lastmonth : $currentmonth;

// --- Read Niño 3.4 data file ---
$url  = "https://psl.noaa.gov/data/correlation/nina34.anom.data";
$file = @file($url, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

if (!$file) {
    die("Failed to read Nino3.4 data file.");
}

// --- Parse: keep only numeric lines that start with a 4-digit year ---
$data = [];
foreach ($file as $line) {
    $trim = trim($line);
    if (preg_match('/^\d{4}/', $trim)) {
        // Split by whitespace, filter out empty parts
        $parts = preg_split('/\s+/', $trim);
        $year = array_shift($parts);
        foreach ($parts as $v) {
            if (is_numeric($v) && $v != -99.99) {
                $data[] = (float)$v;
            }
        }
    }
}

// --- Get last valid anomaly value ---
if (empty($data)) {
    die("No valid Nino3.4 data found.");
}
$oni = end($data);

// --- Determine ENSO category ---
if ($oni > 1.1) {
    $ENSO = "SEL";
    $cond = "Strong El Ni&#241;o";
} elseif ($oni >= 0.5) {
    $ENSO = "WEL";
    $cond = "Weak El Ni&#241;o";
} elseif ($oni >= -0.5) {
    $ENSO = "NUT";
    $cond = "Neutral";
} elseif ($oni >= -1.1) {
    $ENSO = "WLA";
    $cond = "Weak La Ni&#241;a";
} else {
    $ENSO = "SLA";
    $cond = "Strong La Ni&#241;a";
}

// --- Call your Python ranch script (if needed) ---
$command = escapeshellcmd("python3 Python/528.py $ranch $grasstype $condition");
$a = shell_exec($command);
echo "<pre>$a</pre>";
?>
