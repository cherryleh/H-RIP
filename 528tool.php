<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400&display=swap"
        rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"
        integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous">
    </script>
    <link rel="stylesheet" 
              href=
    "https://unpkg.com/purecss@2.0.6/build/pure-min.css"
              integrity=
    "sha384-Uu6IeWbM+gzNVXJcM9XV3SohHtmWE+3VGi496jvgX1jyvDTXfdK+rfZc8C1Aehk5"
              crossorigin="anonymous">

    <script>
    $(function() {
        $("#header").load("./header.html");
        $("#footer").load("./footer.html");
    });
    </script>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css">
    <link rel="stylesheet" type="text/css" href="form.css">
    <link rel="stylesheet" type="text/css" href="./CSS/528table.css">
    <link rel="stylesheet" type="text/css" href="./CSS/header.css">

    <!--<link href="bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">-->

    <link rel="stylesheet" type="text/css" href="dashboard.css">
    <link rel="stylesheet" href="ranchpage.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    

    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>   
</head>
<body>
    <div id="output">
        <div class="tabs">
            <input type="radio" name="tabs" id="tabone" checked="checked">
            <label for="tabone">3-Month Outlook</label>
            <div class="tab" id="three-month">
                <h3 class="" style="margin:0"> Estimated Forage Production: 3-Month Outlook</h3> 
                <div class="" style="margin-left:40px"><b>Grass Type:</b> Signal<span style="margin-left:20px"></span><b>Conditions:</b> Unimproved<span style="margin-left:20px"><b>ENSO Phase:</b> Neutral</div>
                <br>
                <table id="output-table">
                    <colgroup>
                        <col>
                        <col class="outlined-3">
                        <col class="outlined-3">
                        <col class="outlined-3">
                    </colgroup>
                    <tr>
                        <th></th>
                        <th>Oct</th>
                        <th>Nov</th>
                        <th>Dec</th>

                    </tr>
                    <tr>
                        <td>Historical Average Production</td>
                        <td>118 <br> <span class="change"> lbs/acre </span> </td>
                        <td>250 <br> <span class="change"> lbs/acre </span>  </td>
                        <td>332 <br> <span class="change"> lbs/acre </span>  </td>

                    </tr>
                    <tr>
                        <td>Average Production during ENSO-Neutral Years</td>
                        <td style="color:green">&#x2191;1.5% <br> <span class="change">+2 lbs/acre </span> </td>
                        <td style="color:green">&#x2191;17% <br> <span class="change">+44 lbs/acre </span> </td>
                        <td style="color:green">&#x2191;0.5% <br> <span class="change">+2 lbs/acre </span> </td>
                    </tr>
                    <tr>
                        <td>Minimum Production during ENSO-Neutral Years</td>
                        <td style="color:red"> &#x2193;-54% <br> <span class="change">-64 lbs/acre </span></td>
                        <td style="color:red"> &#x2193;-57% <br> <span class="change">-143 lbs/acre </span></td>
                        <td style="color:red"> &#x2193;-40% <br> <span class="change">-134 lbs/acre </span></td>
                    </tr>

                </table>

            </div>

            <input type="radio" name="tabs" id="tabtwo">
            <label for="tabtwo">6-Month Outlook</label>
            <div class="tab six-month">
                <h3 style="margin:0"> Estimated Forage Production: 6-Month Outlook</h3>
                <div class="" style="margin-left:40px"><b>Grass Type:</b> Signal<span style="margin-left:20px"></span><b>Conditions:</b> Unimproved<span style="margin-left:20px"><b>ENSO Phase:</b>Neutral</div>
                <br>
                <div class="scroll">
                    <table id="output-table">
                        <colgroup>
                            <col>
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                        </colgroup>
                        <tr>
                            <th></th>
                            <th>Oct</th>
                            <th>Nov</th>
                            <th>Dec</th>
                            <th>Jan</th>
                            <th>Feb</th>
                            <th>Mar</th>

                        </tr>
                        <tr>
                            <td>Historical Average Production</td>
                            <td>118 <br> <span class="change"> lbs/acre </span> </td>
                            <td>250 <br> <span class="change"> lbs/acre </span> </td>
                            <td>332 <br> <span class="change"> lbs/acre </span> </td>
                            <td>278 <br> <span class="change"> lbs/acre </span> </td>
                            <td>235 <br> <span class="change"> lbs/acre </span> </td>
                            <td>398 <br> <span class="change"> lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Average Production during ENSO-Neutral Years</td>
                            <td style="color:green">&#x2191;1.5% <br> <span class="change">+2 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;17% <br> <span class="change">+44 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;0.5% <br> <span class="change">+2 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;8.0% <br> <span class="change">+22 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;8.8% <br> <span class="change">+21 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;3.5% <br> <span class="change">+14 lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Minimum Production during ENSO-Neutral Years</td>
                            <td style="color:red">&#x2193;-54% <br> <span class="change">-64 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-57% <br> <span class="change">-143 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-40% <br> <span class="change">-134 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-44% <br> <span class="change">-122 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-49% <br> <span class="change">-115 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-36% <br> <span class="change">-143 lbs/acre </span> </td>
                        </tr>

                    </table>
                </div>
            </div>

            <input type="radio" name="tabs" id="tabthree">
            <label for="tabthree">Prior Months</label>
            <div class="tab six-month">
                <h3 style="margin:0"> Estimated Forage Production: Prior Months</h3>
                <div class="" style="margin-left:40px"><b>Grass Type:</b> Signal<span style="margin-left:20px"></span><b>Conditions:</b> Unimproved<span style="margin-left:20px"><b>ENSO Phase:</b>Neutral</div>
                <br>
                <div class="scroll">
                    <table id="output-table">
                        <colgroup>
                            <col>
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                            <col class="outlined-6">
                        </colgroup>
                        <tr>
                            <th></th>
                            <th>Sep</th>
                            <th>Aug</th>
                            <th>Jul</th>
                            <th>Jun</th>
                            <th>May</th>
                            <th>Apr</th>

                        </tr>
                        <tr>
                            <td>Historical Average Production</td>
                            <td>102 <br> <span class="change"> lbs/acre </span> </td>
                            <td>137 <br> <span class="change"> lbs/acre </span> </td>
                            <td>138 <br> <span class="change"> lbs/acre </span> </td>
                            <td>144 <br> <span class="change"> lbs/acre </span> </td>
                            <td>217 <br> <span class="change"> lbs/acre </span> </td>
                            <td>353 <br> <span class="change"> lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Average Production during ENSO-Neutral Years</td>
                            <td style="color:green">&#x2191;1.4% <br> <span class="change">+1 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-5% <br> <span class="change">-7 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;13% <br> <span class="change">+17 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;2.6% <br> <span class="change">+4 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;3.4% <br> <span class="change">+7 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-3% <br> <span class="change">-10 lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Minimum Production during ENSO-Neutral Years</td>
                            <td style="color:red">&#x2193;-26% <br> <span class="change">-26 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-30% <br> <span class="change">-41 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-35% <br> <span class="change">-48 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-47% <br> <span class="change">-67 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-51% <br> <span class="change">-111 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-55% <br> <span class="change">-193 lbs/acre </span> </td>
                        </tr>

                    </table>
                </div>
            </div>
        </div>


    </div>
</body>