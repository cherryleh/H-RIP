<?php 
$grasstype2="None";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $grasstype=($_POST["grasstype"]);
    $grasstype2=($_POST["grasstype2"]);
    $soil = ($_POST["soil"]);
    $soil2 = ($_POST["soil2"]);
    $condition = ($_POST["condition"]);
}

if ($grasstype2 == "None"){
    $secondRow = '';
} else{
    $secondRow = 
    '<tr>
    <td>'.$grasstype2.'</td>
    <td>'.$soil2.'</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>100</td>
    <td>1200</td>
    </tr>';
}

echo '
<div id="output">
    <table id="output-table" class="pure-table pure-table-horizontal">
        <thead>
        <tr>
            <th>Forage</th>
            <th>Soil</th>
            <th>JAN</th>
            <th>FEB</th>
            <th>MAR</th>
            <th>APR</th>
            <th>MAY</th>
            <th>JUN</th>
            <th>JUL</th>
            <th>AUG</th>
            <th>SEP</th>
            <th>OCT</th>
            <th>NOV</th>
            <th>DEC</th>
            <th>Total</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>'.$grasstype.'</td>
            <td>'.$soil.'</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>100</td>
            <td>1200</td>
        </tr>
        
        </tbody>
    </table>

    <br><br>
    <div id="csv">
        <button  type="button" onclick="tableToCSV()">
            Download CSV
        </button>
    </div>

'
?>