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
    <link rel="stylesheet" type="text/css" href="528table.css">
    <link rel="stylesheet" type="text/css" href="./CSS/header.css">

    <!--<link href="bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">-->

    <link rel="stylesheet" type="text/css" href="dashboard.css">
    <link rel="stylesheet" href="ranchpage.css">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    

    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>   
</head>
<body>
<div id="output" style="width: 50%">
        <div class="tabs">
            <input type="radio" name="tabs" id="tabone" checked="checked">
            <label for="tabone">3-Month Outlook</label>
            <div class="tab" id="three-month">
                <h3 class="" style="margin:0"> Estimated Forage Production: 3-Month Outlook</h3> 
                <div class="" style="margin-left:40px"><b>Grasstype:</b> Kikuyu<span style="margin-left:20px"></span><b>Conditions:</b> Improved<span style="margin-left:20px"><b>ENSO Phase:</b>Neutral</div>
                <br>
                <table class="output-table">
                    <colgroup>
                        <col>
                        <col class="outlined-3">
                        <col class="outlined-3">
                        <col class="outlined-3">
                    </colgroup>
                    <tr>
                        <th></th>
                        <th>Jul</th>
                        <th>Aug</th>
                        <th>Sep</th>

                    </tr>
                    <tr>
                        <td>Historical Average Production</td>
                        <td>516 <br> <span class="change"> lbs/acre </span> </td>
                        <td>523 <br> <span class="change"> lbs/acre </span>  </td>
                        <td>381 <br> <span class="change"> lbs/acre </span>  </td>

                    </tr>
                    <tr>
                        <td>Estimated Average Production</td>
                        <td style="color:red">&#x2193;-1% <br> <span class="change">-3 lbs/acre </span> </td>
                        <td style="color:red">&#x2193;-3% <br> <span class="change">-18 lbs/acre </span> </td>
                        <td style="color:red">&#x2193;-1% <br> <span class="change">-2 lbs/acre </span> </td>
                    </tr>
                    <tr>
                        <td>Estimated Minimum Production</td>
                        <td style="color:red"> &#x2193;-9% <br> <span class="change">-48 lbs/acre </span></td>
                        <td style="color:red"> &#x2193;-5% <br> <span class="change">-28 lbs/acre </span></td>
                        <td style="color:red"> &#x2193;-76% <br> <span class="change">-290 lbs/acre </span></td>
                    </tr>

                </table>

            </div>

            <input type="radio" name="tabs" id="tabtwo">
            <label for="tabtwo">6-Month Outlook</label>
            <div class="tab six-month">
                <h3 style="margin:0"> Estimated Forage Production: 6-Month Outlook</h3>
                <div class="" style="margin-left:40px"><b>Grasstype:</b> Kikuyu<span style="margin-left:20px"></span><b>Conditions:</b> Improved<span style="margin-left:20px"><b>ENSO Phase:</b>Neutral</div>
                <br>
                <div class="scroll">
                    <table class="output-table">
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
                            <th>Jul</th>
                            <th>Aug</th>
                            <th>Sep</th>
                            <th>Oct</th>
                            <th>Nov</th>
                            <th>Dec</th>

                        </tr>
                        <tr>
                            <td>Average Production</td>
                            <td>516 <br> <span class="change"> lbs/acre </span> </td>
                            <td>523 <br> <span class="change"> lbs/acre </span> </td>
                            <td>381 <br> <span class="change"> lbs/acre </span> </td>
                            <td>397 <br> <span class="change"> lbs/acre </span> </td>
                            <td>458 <br> <span class="change"> lbs/acre </span> </td>
                            <td>513 <br> <span class="change"> lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Average Production Outlook</td>
                            <td style="color:red">&#x2193;-1% <br> <span class="change">-3 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-3% <br> <span class="change">-18 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-1% <br> <span class="change">-2 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-2% <br> <span class="change">-7 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;3% <br> <span class="change">+14 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;1% <br> <span class="change">+7 lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Minimum Production Outlook</td>
                            <td style="color:red">&#x2193;-9% <br> <span class="change">-48 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-5% <br> <span class="change">-28 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-76% <br> <span class="change">-290 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-90% <br> <span class="change">-359 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-62% <br> <span class="change">-284 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-33% <br> <span class="change">-169 lbs/acre </span> </td>
                        </tr>

                    </table>
                </div>
            </div>

            <input type="radio" name="tabs" id="tabthree">
            <label for="tabthree">Prior Months</label>
            <div class="tab six-month">
                <h3 style="margin:0"> Estimated Forage Production: Prior Months</h3>
                <div class="" style="margin-left:40px"><b>Grasstype:</b> Kikuyu<span style="margin-left:20px"></span><b>Conditions:</b> Improved<span style="margin-left:20px"><b>ENSO Phase:</b>Neutral</div>
                <br>
                <div class="scroll">
                    <table class="output-table">
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
                            <th>Jun</th>
                            <th>May</th>
                            <th>Apr</th>
                            <th>Mar</th>
                            <th>Feb</th>
                            <th>Jan</th>

                        </tr>
                        <tr>
                            <td>Average Production</td>
                            <td>466 <br> <span class="change"> lbs/acre </span> </td>
                            <td>527 <br> <span class="change"> lbs/acre </span> </td>
                            <td>605 <br> <span class="change"> lbs/acre </span> </td>
                            <td>592 <br> <span class="change"> lbs/acre </span> </td>
                            <td>494 <br> <span class="change"> lbs/acre </span> </td>
                            <td>519 <br> <span class="change"> lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Average Production Outlook</td>
                            <td style="color:green">&#x2191;0% <br> <span class="change">+2 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-1% <br> <span class="change">-7 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-1% <br> <span class="change">-8 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;4% <br> <span class="change">+21 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;3% <br> <span class="change">+14 lbs/acre </span> </td>
                            <td style="color:green">&#x2191;10% <br> <span class="change">+54 lbs/acre </span> </td>

                        </tr>
                        <tr>
                            <td>Minimum Production Outlook</td>
                            <td style="color:red">&#x2193;-52% <br> <span class="change">-244 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-56% <br> <span class="change">-295 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-57% <br> <span class="change">-344 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-41% <br> <span class="change">-242 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-57% <br> <span class="change">-281 lbs/acre </span> </td>
                            <td style="color:red">&#x2193;-56% <br> <span class="change">-293 lbs/acre </span> </td>
                        </tr>

                    </table>
                </div>
            </div>
        </div>


    </div>
</body>