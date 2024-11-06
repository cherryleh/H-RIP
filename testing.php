
    <?php
    //Temperature monthly averages
    $RID = "RID066";
    
    //SPI
    $file_spi = "./RID/" . $RID . "/" . $RID . "_spi.csv";
    $max = count(file($file_spi, FILE_SKIP_EMPTY_LINES));
    $min = $max - 13;
    
    $csv_spi = fopen($file_spi, "r");
    
    $array_spi = [];
    
    while ($data = fgetcsv($csv_spi)) {
        if ($data[0] >= $min && $data[0] <= $max) {
            array_push($array_spi, floatval($data[2]));
        }
    }

    
    echo $min;
    echo $max;
    //Count how many months in last year is in drought (<0)
    $d = 0;
    foreach ($array_spi as $value) {
        if ($value < -0.5) {
            $d++;
        }
    }
    
    $spi = end($array_spi);

    fclose($csv_spi);
    
    //Drought status
    if ($spi <= -2) {
        $drought_status = "Exceptional Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:red; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -1.6 && $spi > -2) {
        $drought_status = "Extreme Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:red; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -1.3 && $spi > -1.6) {
        $drought_status = "Severe Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:darkorange; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -0.8 && $spi > -1.3) {
        $drought_status = "Moderate Drought";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:orange; display:inline-block; vertical-align: middle"';
    } elseif ($spi <= -0.5 && $spi > -0.8) {
        $drought_status = "Abnormally Dry";
        $icon_spi = 'class="bi bi-exclamation-circle-fill fs-3" style="color:orange; display:inline-block; vertical-align: middle"';
    } else {
        $drought_status = "No Drought";
        $icon_spi = 'class="bi bi-check-circle-fill fs-3" style="color:green; display:inline-block;vertical-align: middle"';
    }


    
    
    ?>