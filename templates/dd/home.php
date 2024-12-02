<?php
include("include/protect2.php");
include("include/dbconnect.php");
include("encrypt_msg.php");
extract($_POST);

$uname=$_SESSION['uname'];
$rid=$_SESSION['rid'];
$msg="";

$qry1=mysqli_query($connect,"select * from vb_relative where id='$rid'");
$row1=mysqli_fetch_array($qry1);
$un=$row1['uname'];
$key=$un;
?>
<html>
<head>
	<title><?php include("include/title2.php"); ?></title>
	<meta charset="UTF-8">
	<meta name="description" content="Cryptocurrency Landing Page Template">
	<meta name="keywords" content="cryptocurrency, unica, creative, html">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<!-- Favicon -->
	<link href="img/favicon.ico" rel="shortcut icon"/>

	<!-- Google Fonts -->
	<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet">

	<!-- Stylesheets -->
	<link rel="stylesheet" href="css/bootstrap.min.css"/>
	<link rel="stylesheet" href="css/font-awesome.min.css"/>
	<link rel="stylesheet" href="css/themify-icons.css"/>
	<link rel="stylesheet" href="css/owl.carousel.css"/>
	<link rel="stylesheet" href="css/style.css"/>


	<!--[if lt IE 9]>
	  <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
	  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
	<![endif]-->
</head>
<body>
	<!-- Page Preloder -->
	<!--<div id="preloder">
		<div class="loader"></div>
	</div>-->

	<!-- Header section -->
	<header class="header-section clearfix">
		<div class="container-fluid">
			<a href="index.html" class="site-logo">
				<img src="img/cbr2.png" alt="">
			</a>
			<div class="responsive-bar"><i class="fa fa-bars"></i></div>
			<a href="" class="user"><i class="fa fa-user"></i></a>
			<!--<a href="register.php" class="site-btn">Sign Up Free</a>-->
			<nav class="main-menu">
				<ul class="menu-list">
					<li><a href="home.php">Home</a></li>
					<li><a href="logout.php">Logout</a></li>
				</ul>
			</nav>
		</div>
	</header>
	<!-- Header section end -->



	<!-- Page info section -->
	<section class="page-info-section">
		<div class="container">
			<h3>Welcome <?php echo fnDecrypt($row1['name'],$key); ?></h3>
			<div class="site-beradcamb">
				Relative ID: <?php echo $row1['id']; ?>
				<!--<span><i class="fa fa-angle-right"></i> </span>-->
			</div>
		</div>
	</section>
	<!-- Page info end -->



	<!-- Contact section -->
	<section class="contact-page spad">
		<div class="container">
			<div class="row">
				<div class="col-lg-8">
					<form class="contact-form" name="form1" method="post">
			<?php		
					//personal
		$qry=mysqli_query($connect,"select * from vb_register where uname='$un' && rid='$rid'");
$row=mysqli_fetch_array($qry);
$num=mysqli_num_rows($qry);
		if($num>0)
		{  
		?>
					<h3>Personal Information</h3>
						<div class="row">
						
							<div class="col-md-3">
									Name
							</div>
							<div class="col-md-3">
									: <?php 
									$fname=$row['fname'];
									$lname=$row['lname'];
									echo $fname." ".$lname; ?>
							</div>
							<div class="col-md-3">
								Gender
							</div>
							<div class="col-md-3">
								: <?php echo $row['gender']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								D.O.B:
							</div>
							<div class="col-md-3">
								: <?php echo $row['dob']; ?>
							</div>
							<div class="col-md-6">
								
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Temporary Address
							</div>
							<div class="col-md-9">
								: <?php echo $row['address']; ?>
							</div>
							<div class="col-md-3">
								Permanent Address
							</div>
							<div class="col-md-9">
								: <?php echo $row['address2']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Pincode
							</div>
							<div class="col-md-3">
								: <?php echo $row['pincode']; ?>
							</div>
							<div class="col-md-3">
								City
							</div>
							<div class="col-md-3">
								: <?php echo $row['city']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								State
							</div>
							<div class="col-md-3">
								: <?php echo $row['state']; ?>
							</div>
							<div class="col-md-3">
								Country
							</div>
							<div class="col-md-3">
								: <?php echo $row['country']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Email
							</div>
							<div class="col-md-3">
								: <?php echo $row['email']; ?>
							</div>
							<div class="col-md-3">
								Mobile No.
							</div>
							<div class="col-md-3">
								: <?php echo $row['mobile']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Landline No.
							</div>
							<div class="col-md-3">
								: <?php echo $row['landline']; ?>
							</div>
							<div class="col-md-3">
								Aadhar Card Number
							</div>
							<div class="col-md-3">
								: <?php echo $row['adhar']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Voter ID
							</div>
							<div class="col-md-3">
								: <?php echo $row['voter']; ?>
							</div>
							<div class="col-md-3">
								PAN Card
							</div>
							<div class="col-md-3">
								: <?php echo $row['pancard']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Driving License
							</div>
							<div class="col-md-3">
								: <?php echo $row['driving']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
						</div>
						
						
						
						<h3>Educational Information</h3>
						<div class="row">
							<div class="col-md-3">
								SSLC School Name
							</div>
							<div class="col-md-3">
								: <?php echo $row['sslc_school']; ?>
							</div>
							<div class="col-md-3">
								Marks
							</div>
							<div class="col-md-3">
								: <?php echo $row['sslc_mark']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							
							<div class="col-md-3">
								Passout Year
							</div>
							<div class="col-md-3">
								: <?php echo $row['sslc_year']; ?>
							</div>
							<div class="col-md-3">
								Percentage
							</div>
							<div class="col-md-3">
								: <?php echo $row['sslc_per']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							
							<div class="col-md-3">
								HSC School Name
							</div>
							<div class="col-md-3">
								: <?php echo $row['hsc_school']; ?>
							</div>
							<div class="col-md-3">
								Marks
							</div>
							<div class="col-md-3">
								: <?php echo $row['hsc_mark']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Passout Year
							</div>
							<div class="col-md-3">
								: <?php echo $row['hsc_year']; ?>
							</div>
							<div class="col-md-3">
								Percentage
							</div>
							<div class="col-md-3">
								: <?php echo $row['hsc_per']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							
							<div class="col-md-3">
								UG College Name
							</div>
							<div class="col-md-3">
								: <?php echo $row['ug_college']; ?>
							</div>
							<div class="col-md-3">
								Percentage
							</div>
							<div class="col-md-3">
								: <?php echo $row['ug_per']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Passout Year
							</div>
							<div class="col-md-3">
								: <?php echo $row['ug_year']; ?>
							</div>
							<div class="col-md-3">
								
							</div>
							<div class="col-md-3">
								
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							
							<div class="col-md-3">
								PG College Name
							</div>
							<div class="col-md-3">
								: <?php echo $row['pg_college']; ?>
							</div>
							<div class="col-md-3">
								Percentage
							</div>
							<div class="col-md-3">
								: <?php echo $row['pg_year']; ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>
							<div class="col-md-3">
								Passout Year
							</div>
							<div class="col-md-3">
								: <?php echo $row['pg_year']; ?>
							</div>
							<div class="col-md-3">
								
							</div>
							<div class="col-md-3">
								
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							&nbsp;
							</div>

						</div>
				
				<?php
				}//per
				
			$q1=mysqli_query($connect,"select * from vb_occupation where rid=$rid && uname='$un'");
		  $n1=mysqli_num_rows($q1);
		  if($n1>0)
		  {
		  ?><h3>Occupation</h3><?php
		  while($r1=mysqli_fetch_array($q1))
		  {
		  ?>
						<div class="row">
						
							<div class="col-md-6">
									Company
							</div>
							<div class="col-md-6">
									: <?php echo $r1['company']; ?>
							</div>
							<div class="col-md-6">
								Position
							</div>
							<div class="col-md-6">
								: <?php echo $r1['position']; ?>
							</div>
							<div class="col-md-6">
								Monthly Salary
							</div>
							<div class="col-md-6">
								: <?php echo $r1['salary']; ?>
							</div>
							<div class="col-md-6">
								Working Duration
							</div>
							<div class="col-md-6">
								: <?php echo $r1['duration']; ?>
							</div>
							<div class="col-md-6">
								Experience
							</div>
							<div class="col-md-6">
								: <?php echo $r1['experience']; ?>
							</div>
							
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"></p>
							</div>
						</div>
						
				<?php
				}
				}//occu		
				
		  $q2=mysqli_query($connect,"select * from vb_account where rid=$rid && uname='$un'");
		  $n2=mysqli_num_rows($q2);
		  if($n2>0)
		  {
		  ?><h3>Bank Account Information</h3><?php
		  while($r2=mysqli_fetch_array($q2))
		  {
		  ?>
						<div class="row">
						
							<div class="col-md-6">
									Bank
							</div>
							<div class="col-md-6">
									: <?php echo $r2['bank']; ?>
							</div>
							<div class="col-md-6">
								Branch
							</div>
							<div class="col-md-6">
								: <?php echo $r2['branch']; ?>
							</div>
							<div class="col-md-6">
								Account No.
							</div>
							<div class="col-md-6">
								: <?php echo $r2['account']; ?>
							</div>
							<div class="col-md-6">
								PIN Number
							</div>
							<div class="col-md-6">
								: <?php echo $r2['pinno']; ?>
							</div>
							<div class="col-md-6">
								Card Number
							</div>
							<div class="col-md-6">
								: <?php echo $r2['cardno']; ?>
							</div>
							<div class="col-md-6">
								Account Password
							</div>
							<div class="col-md-6">
								: <?php echo $r2['acpass']; ?>
							</div>
							
							
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"></p>
							</div>
						</div>
						
				<?php
				}
				}//bank
				
				$q3=mysqli_query($connect,"select * from vb_email where rid=$rid && uname='$un'");
		  $n3=mysqli_num_rows($q3);
		  if($n3>0)
		  {
		  ?><h3>Email Information</h3><?php
		  while($r3=mysqli_fetch_array($q3))
		  {
		  ?>
						<div class="row">
						
							<div class="col-md-6">
									E-mail ID
							</div>
							<div class="col-md-6">
									: <?php echo $r3['email']; ?>
							</div>
							<div class="col-md-6">
								E-mail Password
							</div>
							<div class="col-md-6">
								: <?php echo $r3['pass']; ?>
							</div>
							
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"></p>
							</div>
						</div>
						
				<?php
				}
				}//email
				 $q4=mysqli_query($connect,"select * from vb_document where rid=$rid && uname='$un'");
		  $n4=mysqli_num_rows($q4);
		  if($n4>0)
		  {
		  ?><h3>Documents</h3><?php
		  while($r4=mysqli_fetch_array($q4))
		  {
		  ?>
						<div class="row">
						
							<div class="col-md-6">
									Title of Document
							</div>
							<div class="col-md-6">
									: <?php echo $r4['title']; ?>
							</div>
							<div class="col-md-6">
								Details
							</div>
							<div class="col-md-6">
								: <?php echo $r4['details']; ?>
							</div>
							<div class="col-md-6">
								File
							</div>
							<div class="col-md-6">
								: <?php 
								if($r1['filename']!="") { 
								
								
			  echo '<a href="">'.$r4['filename'].'</a>'; 
			  } else { echo "None"; } ?>
							</div>
							<div class="col-md-6">
								Relative
							</div>
							
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"></p>
							</div>
						</div>
						
				<?php
				}
				}//document
				 $q5=mysqli_query($connect,"select * from vb_audio where rid=$rid && uname='$un'");
		  $n5=mysqli_num_rows($q5);
		  if($n5>0)
		  {
		  ?><h3>Audio / Video Information</h3><?php
		  while($r5=mysqli_fetch_array($q5))
		  {
		  ?>
						<div class="row">
							
							<div class="col-md-6">
									Title of Document
							</div>
							<div class="col-md-6">
									: <?php echo $r5['title']; ?>
							</div>
							<div class="col-md-6">
								Details
							</div>
							<div class="col-md-6">
								: <?php echo $r5['details']; ?>
							</div>
							<div class="col-md-6">
								File
							</div>
							<div class="col-md-6">
								: <?php if($r5['filename']!="") { 
								
								
			  //echo '<a href="download.php?file1='.$fna.'&folder1=audio">'.$fna.'</a>'; 
			  echo '<a href="">'.$r5['filename'].'</a>'; 
			  } else { echo "None"; } ?>
							</div>
							
							
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"></p>
							</div>
						</div>
						
				<?php
				}
				}//audio
				?>
					</form>
					<p><a href="home_dec.php">Decryption</a></p>
				</div>
				<div class="col-lg-4 mt-5 mt-lg-0">
					
				<img src="img/cbr7.jpg" class="img-fluid" alt="">
		  
				</div>
			</div>
		</div>
	</section>
	<!-- Contact section end -->


	<!-- Newsletter section -->
	<section class="newsletter-section gradient-bg">
		<div class="container text-white">
			<div class="row">
				<div class="col-lg-7 newsletter-text">
					<h2>Cloud Information</h2>
					<p>The user has store the information into cloud. Information has send to alloted persons after user's death.</p>
				</div>
				<div class="col-lg-5 col-md-8 offset-lg-0 offset-md-2">
					<!--<form class="newsletter-form">
						<input type="text" placeholder="Enter your email">
						<button>Get Started</button>
					</form>-->
				</div>
			</div>
		</div>
	</section>
	<!-- Newsletter section end -->



	<!-- Blog section -->
	
	<!-- Blog section end -->


	<!-- Footer section -->
	<footer class="footer-section">
		<div class="container">
			<div class="row spad">
				<div class="col-md-6 col-lg-3 footer-widget">
					<img src="img/cbr2.png" class="mb-4" alt="">
					<p>Create an artificial brain that can think, alerts, take decision, Store and Retrieve Information from Cloud.</p>
					<span><!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
<?php include("include/title2.php"); ?> <a href="https://colorlib.com" target="_blank"></a>
<!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. --></span>
				</div>
				<div class="col-md-6 col-lg-2 offset-lg-1 footer-widget">
					<h5 class="widget-title">Resources</h5>
					<ul>
						<li><a href="home.php">Home</a></li>
					</ul>
				</div>
				<div class="col-md-6 col-lg-2 offset-lg-1 footer-widget">
					<h5 class="widget-title">Quick Links</h5>
					<ul>
						<li><a href="logout.php">Logout</a></li>
					</ul>
				</div>
				<div class="col-md-6 col-lg-3 footer-widget pl-lg-5 pl-3">
					<h5 class="widget-title">Follow Us</h5>
					<div class="social">
						<a href="" class="facebook"><i class="fa fa-facebook"></i></a>
						<a href="" class="google"><i class="fa fa-google-plus"></i></a>
						<a href="" class="instagram"><i class="fa fa-instagram"></i></a>
						<a href="" class="twitter"><i class="fa fa-twitter"></i></a>
					</div>
				</div>
			</div>
			<div class="footer-bottom">
				<div class="row">
					<div class="col-lg-4 store-links text-center text-lg-left pb-3 pb-lg-0">
						<!--<a href=""><img src="img/appstore.png" alt="" class="mr-2"></a>
						<a href=""><img src="img/playstore.png" alt=""></a>-->
					</div>
					<div class="col-lg-8 text-center text-lg-right">
						<ul class="footer-nav">
							<li><a href="">Terms of Use</a></li>
							<li><a href="">Privacy Policy </a></li>
							<li><a href="">cloudbrain@info.com</a></li>
							<li><a href="">(123) 456-7890</a></li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</footer>


	<!--====== Javascripts & Jquery ======-->
	<script src="js/jquery-3.2.1.min.js"></script>
	<script src="js/owl.carousel.min.js"></script>
	<script src="js/main.js"></script>
</body>
</html>