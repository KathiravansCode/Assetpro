<?php
include("include/protect.php");
include("include/dbconnect.php");
include("encrypt_msg.php");
extract($_REQUEST);

$uname=$_SESSION['uname'];
$msg="";
$key=$uname;
$qry=mysqli_query($connect,"select * from vb_register where uname='$uname'");
$row=mysqli_fetch_array($qry);

if(isset($btn))
{
$sslc_school1=fnEncrypt($sslc_school,$key);
$sslc_mark1=fnEncrypt($sslc_mark,$key);
$sslc_year1=fnEncrypt($sslc_year,$key);
$sslc_per1=fnEncrypt($sslc_per,$key);
$hsc_school1=fnEncrypt($hsc_school,$key);
$hsc_mark1=fnEncrypt($hsc_mark,$key);
$hsc_year1=fnEncrypt($hsc_year,$key);
$hsc_per1=fnEncrypt($hsc_per,$key);
$ug_college1=fnEncrypt($ug_college,$key);
$ug_per1=fnEncrypt($ug_per,$key);
$ug_year1=fnEncrypt($ug_year,$key);
$pg_college1=fnEncrypt($pg_college,$key);
$pg_per1=fnEncrypt($pg_per,$key);
$pg_year1=fnEncrypt($pg_year,$key);


mysqli_query($connect,"update vb_register set sslc_school='$sslc_school1',sslc_mark='$sslc_mark1',sslc_year='$sslc_year1',sslc_per='$sslc_per1',hsc_school='$hsc_school1',hsc_mark='$hsc_mark1',hsc_year='$hsc_year1',hsc_per='$hsc_per1',ug_college='$ug_college1',ug_per='$ug_per1',ug_year='$ug_year1',pg_college='$pg_college1',pg_per='$pg_per1',pg_year='$pg_year1' where uname='$uname'");
header("location:user_home.php");
}
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
	<div id="preloder">
		<div class="loader"></div>
	</div>

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
					<li><a href="user_home.php">Home</a></li>
					<li><a href="education.php">Education</a></li>
					<li><a href="occupation.php">Occupation</a></li>
					<li><a href="relative.php">Relatives</a></li>
					<li><a href="logout.php">Logout</a></li>
				</ul>
			</nav>
		</div>
	</header>
	<!-- Header section end -->



	<!-- Page info section -->
	<section class="page-info-section">
		<div class="container">
			<h3>Welcome <?php 
			$fname=fnDecrypt($row['fname'],$key);
			$lname=fnDecrypt($row['lname'],$key);
			echo $fname." ".$lname;
			 ?></h3>
			<div class="site-beradcamb">
				User ID: <?php echo $uname; ?>
				<!--<span><i class="fa fa-angle-right"></i> </span>-->
			</div>
		</div>
	</section>
	<!-- Page info end -->



	<!-- Contact section -->
	<section class="contact-page spad">
		<div class="container">
		<h3>Update Education Information</h3>
			<div class="row">
				<div class="col-lg-8">
					<form class="contact-form" name="form1" method="post">
					<div class="col-md-6">
								<div class="form-group">
								<label>SSLC School Name</label>
									<input class="check-form" type="text" name="sslc_school" placeholder="" value="<?php if($row['sslc_school']!="") echo fnDecrypt($row['sslc_school'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>SSLC Mark</label>
									<input class="check-form" type="text" name="sslc_mark" placeholder="" value="<?php if($row['sslc_mark']!="") echo fnDecrypt($row['sslc_mark'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>SSLC Passout Year</label>
									<input class="check-form" type="text" name="sslc_year" placeholder="" value="<?php if($row['sslc_year']!="") echo fnDecrypt($row['sslc_year'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>SSLC Percentage</label>
									<input class="check-form" type="text" name="sslc_per" placeholder="" value="<?php if($row['sslc_per']!="") echo fnDecrypt($row['sslc_per'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>HSC School Name</label>
									<input class="check-form" type="text" name="hsc_school" placeholder="" value="<?php if($row['hsc_school']!="") echo fnDecrypt($row['hsc_school'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>HSC Mark</label>
									<input class="check-form" type="text" name="hsc_mark" placeholder="" value="<?php if($row['hsc_mark']!="") echo fnDecrypt($row['hsc_mark'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>HSC Passout Year</label>
									<input class="check-form" type="text" name="hsc_year" placeholder="" value="<?php if($row['hsc_year']!="") echo fnDecrypt($row['hsc_year'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>HSC Percentage</label>
									<input class="check-form" type="text" name="hsc_per" placeholder="" value="<?php if($row['hsc_per']!="") echo fnDecrypt($row['hsc_per'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>UG College Name</label>
									<input class="check-form" type="text" name="ug_college" placeholder="" value="<?php if($row['ug_college']!="") echo fnDecrypt($row['ug_college'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>UG Percentage</label>
									<input class="check-form" type="text" name="ug_per" placeholder="" value="<?php if($row['ug_per']!="") echo fnDecrypt($row['ug_per'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>UG Passout Year</label>
									<input class="check-form" type="text" name="ug_year" placeholder="" value="<?php if($row['ug_year']!="") echo fnDecrypt($row['ug_year'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>PG College Name</label>
									<input class="check-form" type="text" name="pg_college" placeholder="" value="<?php if($row['pg_college']!="") echo fnDecrypt($row['pg_college'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>PG Percentage</label>
									<input class="check-form" type="text" name="pg_per" placeholder="" value="<?php if($row['pg_per']!="") echo fnDecrypt($row['pg_per'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
								<label>PG Passout Year</label>
									<input class="check-form" type="text" name="pg_year" placeholder="" value="<?php if($row['pg_year']!="") echo fnDecrypt($row['pg_year'],$key); ?>">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							
					<div class="col-md-12">
								<button type="submit" name="btn" class="site-btn sb-gradients mt-4" onClick="return validate()">Submit</button>
							</div>
					</form>
				</div>
				<div class="col-lg-4 mt-5 mt-lg-0">
					
					<?php
		  if($row['photo']!="")
		  {
		  $photo=fnDecrypt($row['photo'],$key);
		  ?><img src="photo/<?php echo $photo; ?>" class="img-fluid" style="border-radius: 50%" /><?php
		  }
		  else
		  {
		  ?><img src="img/cbr8.jpg" class="img-fluid" /><?php
		  }
		  ?>
		  <br>
		  <a href="edit.php">Edit Profile</a> / 
		  <a href="upload.php">Change Photo</a>
		  
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
						<li><a href="user_home.php">Home</a></li>
						<li><a href="education.php">Education</a></li>
						<li><a href="occupation.php">Occupation</a></li>
						<li><a href="relative.php">Relatives</a></li>
					</ul>
				</div>
				<div class="col-md-6 col-lg-2 offset-lg-1 footer-widget">
					<h5 class="widget-title">Quick Links</h5>
					<ul>
						<li><a href="account.php">Bank Account</a></li>
						<li><a href="ac_email.php">E-mail</a></li>
						<li><a href="document.php">Documents</a></li>
						<li><a href="audio.php">Audio/Video</a></li>
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