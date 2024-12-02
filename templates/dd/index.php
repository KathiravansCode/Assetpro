<?php
session_start();
include("include/dbconnect.php");
include("email.php");
include("encrypt_msg.php");
extract($_POST);
$rdate=date("d-m-Y");

$ip = $_SERVER['REMOTE_ADDR'];
//////MAC Address////////
ob_start();
//Get the ipconfig details using system commond
system('ipconfig /all');

// Capture the output into a variable
$mycom=ob_get_contents();
// Clean (erase) the output buffer
ob_clean();

$findme = "Physical";
//Search the "Physical" | Find the position of Physical text
$pmac = strpos($mycom, $findme);

// Get Physical Address
$mac=substr($mycom,($pmac+36),17);
////////////////////////////////////////////
//////////last access identification & send msg,docs///////////////

$q1=mysqli_query($connect,"select * from vb_register");
while($r1=mysqli_fetch_array($q1))
{
$un=$r1['uname'];
$key1=$un;
	$ldate=fnDecrypt($r1['last_date'],$key1);
	$st=$r1['status'];
	$mobile=fnDecrypt($r1['mobile'],$key1);
	$email=fnDecrypt($r1['email'],$key1);
	$days=(strtotime($rdate)-strtotime($ldate))/(60*60*24);
	$fname=fnDecrypt($r1['fname'],$key1);
	$lname=fnDecrypt($r1['lname'],$key1);
	$name=$fname." ".$lname;
				
		if($days>=45)
		{
			if($st!=3)
			{
			mysqli_query($connect,"update vb_register set status=3 where uname='$un'");
			
				////personal-education
				$rid1=$r1['rid'];
				
				$sq1=mysqli_query($connect,"select * from vb_relative where uname='$un'");
				while($sr1=mysqli_fetch_array($sq1))
				{
				$rid=$sr1['id'];
				$rname=fnDecrypt($sr1['name'],$key1);
				$mob1=fnDecrypt($sr1['mobile'],$key1);
				$email1=fnDecrypt($sr1['email'],$key1);
				$p1=fnDecrypt($sr1['pass'],$key1);
				$rn=rand(100,999);
				$rn2=$rid.$rn;
				$k=md5($rn2);
				$kk=substr($k,0,8);
				
				$kk1=fnEncrypt($kk,$key1);
				mysqli_query($connect,"update vb_relative set secret_key='$kk1' where id=$rid");
				
				$mess1="Dear $rname, Received information from $name, Username:$mob1, Password:$p1, Key: $kk, Link: http://localhost/cloud_brain/login.php";
				$objEmail	=	new CI_Email();
		$objEmail->from('iotcloudadmin@iotcloud.co.in', "Cloud Brain");
		$objEmail->to("$email1");
		//$objEmail->to("sanjeevi@oculusit.in");
		
		//$objEmail->cc($txt_cc);
		//$objEmail->bcc($txt_bcc);
		$objEmail->subject("Cloud Brain - $un");
		$objEmail->message("$mess1");
		//send mail
			
			if ($objEmail->send())
			{	
			//echo "sent";
			}
			else
			{	
			//echo "not";
			}
		
			//echo '<iframe src="http://pay4sms.in/sendsms/?token= b81edee36bcef4ddbaa6ef535f8db03e&credit=2&sender=RnDTRY&message='.$mess1.'&number=91'.$mob1.'" style="display:block"></iframe>';   
				}
			
			//include("mail1.php");
			///other information
			//include("mail2.php");
			//////////////////////
			
			
			}
		}
		else if($days>=30)
		{
			if($st!=2)
			{
			$message="Dear $name, From:Cloud Brain, You are not access your account in last 30 days, so you want to access your account";
			
			//echo '<iframe src="http://pay4sms.in/sendsms/?token= b81edee36bcef4ddbaa6ef535f8db03e&credit=2&sender=RnDTRY&message='.$message.'&number=91'.$mobile.'" style="display:block"></iframe>';   
			mysqli_query($connect,"update vb_register set status=2 where uname='$un'");
			
			//$mess1="Received information from $name, Username:$mob1, Password:$p1, Link: http://iotcloud.co.in/cloud_brain/login.php";
				$objEmail	=	new CI_Email();
		$objEmail->from('iotcloudadmin@iotcloud.co.in', "Personal Details");
		$objEmail->to("$email");
		
		//$objEmail->cc($txt_cc);
		//$objEmail->bcc($txt_bcc);
		$objEmail->subject("Cloud Brain - $un");
		$objEmail->message("$message");
		//send mail
			
				if ($objEmail->send())
				{	
				//echo "sent";
				}
				else
				{	
				//echo "not";
				}
			}
		}
		else if($days>=15)
		{
			if($st!=1)
			{
			$message="Dear $name, From:Cloud Brain, You are not access your account in last 15 days, so you want to access your account";
			
			//echo '<iframe src="http://pay4sms.in/sendsms/?token= b81edee36bcef4ddbaa6ef535f8db03e&credit=2&sender=RnDTRY&message='.$message.'&number=91'.$mobile.'" style="display:block"></iframe>';   
			mysqli_query($connect,"update vb_register set status=1 where uname='$un'");
				$objEmail	=	new CI_Email();
		$objEmail->from('iotcloudadmin@iotcloud.co.in', "Personal Details");
		$objEmail->to("$email");
		
		//$objEmail->cc($txt_cc);
		//$objEmail->bcc($txt_bcc);
		$objEmail->subject("Cloud Brain - $un");
		$objEmail->message("$message");
		//send mail
			
				if ($objEmail->send())
				{	
				//echo "sent";
				}
				else
				{	
				//echo "not";
				}
			}
		}
}
///////////////////////////
	if(isset($btn))
	{
		
		$qry=mysqli_query($connect,"select * from vb_register where uname='".$uname."'");
		$num=mysqli_num_rows($qry);
			if($num==1)
			{
			$row=mysqli_fetch_array($qry);
			$key=$uname;
			$pw=fnDecrypt($row['pass'],$key);
			$rdate1=fnEncrypt($rdate,$key);
				if($pw==$pass)
				{
				$secret=rand(10000,99999);
				
				$_SESSION['uname']=$uname;
				$_SESSION['id']=$row['id'];
				//header("location:user.php");
				mysqli_query($connect,"update vb_register set last_date='$rdate1',secret='$secret',sms_st=0,status=0 where uname='$uname'");
				
				?>
				<script language="javascript">
				window.location.href="user_home.php";
				//window.location.href="verify1.php";
				</script>
				<?php
				}
				else
				{
				$msg="Invalid User!";
				}
			}
			else
			{
			/*$qry1=mysqli_query($connect,"select * from vb_register where uname='$uname'");
			$row1=mysqli_fetch_array($qry1);
			$mobile=$row1['mobile'];
			$message="Someone access your account! IP:$ip,Mac:$mac";*/
			$msg="Invalid User!";
			}
		
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
	<link rel="stylesheet" href="css/animate.css"/>
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
			<a href="register.php" class="site-btn">Sign Up Free</a>
			<nav class="main-menu">
				<ul class="menu-list">
					<li><a href="index.php">Home</a></li>
					<li><a href="">About</a></li>
					<li><a href="">Contact</a></li>
				</ul>
			</nav>
		</div>
	</header>
	<!-- Header section end -->


	<!-- Hero section -->
	<section class="hero-section">
		<div class="container">
			<div class="row">
				<div class="col-md-6 hero-text">
					<h2>Cloud <span>Brain</span> <br></h2>
					<h4>User Login</h4>
					<form name="form1" class="hero-subscribe-from" method="post">
						<input type="text" name="uname" placeholder="Username" required>  
						<input type="password" name="pass" placeholder="Password" required>
						<button type="submit" name="btn" class="site-btn sb-gradients">Login</button>
					</form>
					<span style="color:#FF0000"><?php echo $msg; ?></span>
				</div>
				<div class="col-md-6">
					<!--<img src="img/cbr3.png" class="laptop-image" alt="">-->
				</div>
			</div>
		</div>
	</section>
	<!-- Hero section end -->


	<!-- About section -->
	<section class="about-section spad">
		<div class="container">
			<div class="row">
				<div class="col-lg-6 offset-lg-6 about-text">
					<h2>Cloud Brain</h2>
					<h5>Today scientists are in research to create an artificial brain that can think, response, take decision, and keep anything in memory.</p>
					<a href="date_update.php" class="site-btn sb-gradients sbg-line mt-5">Get Started</a>
				</div>
			</div>
			<div class="about-img">
				<img src="img/cbr7.jpg" class="img-fluid" alt="">
			</div>
		</div>
	</section>
	<!-- About section end -->


	<!-- Features section -->
	
	<!-- Features section end -->


	<!-- Process section -->
	
	<!-- Process section end -->


	<!-- Fact section -->
	
	<!-- Fact section end -->


	<!-- Team section -->
	
	<!-- Team section -->


	<!-- Review section -->
	
	<!-- Review section end -->


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
						<li><a href="index.php">Home</a></li>
					</ul>
				</div>
				<div class="col-md-6 col-lg-2 offset-lg-1 footer-widget">
					<h5 class="widget-title">Quick Links</h5>
					<ul>
						<li><a href="register.php">Register</a></li>
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
