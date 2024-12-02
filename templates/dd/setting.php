<?php
include("include/protect.php");
include("include/dbconnect.php");
include("email.php");
include("encrypt_msg.php");
extract($_REQUEST);

$uname=$_SESSION['uname'];
$msg="";
$msg1="";
$key=$uname;
$qry=mysqli_query($connect,"select * from vb_register where uname='$uname'");
$row=mysqli_fetch_array($qry);

$fname=fnDecrypt($row['fname'],$key);
$lname=fnDecrypt($row['lname'],$key);
$name=$fname." ".$lname;
$rid1=$row['rid'];

$rdate=date("d-m-Y");
if($act=="yes")
{
mysqli_query($connect,"update vb_register set alert_st=0 where uname='$uname'");
?>
<script language="javascript">
window.location.href="setting.php";
</script>
<?php
}
if($act=="no")
{
mysqli_query($connect,"update vb_register set alert_st=1 where uname='$uname'");
?>
<script language="javascript">
window.location.href="setting.php";
</script>
<?php
}

if($act=="sendmail")
{
$msg1="Sending Mail...";
$sq1=mysqli_query($connect,"select * from vb_relative where uname='$uname'");
				while($sr1=mysqli_fetch_array($sq1))
				{
				$rid=$sr1['id'];
				$rname=fnDecrypt($sr1['name'],$key);
				$mob1=fnDecrypt($sr1['mobile'],$key);
				$email1=fnDecrypt($sr1['email'],$key);
				$p1=fnDecrypt($sr1['pass'],$key);
				$rn=rand(100,999);
				$rn2=$rid.$rn;
				$k=md5($rn2);
				$kk=substr($k,0,8);
				
				$kk1=fnEncrypt($kk,$key);
				mysqli_query($connect,"update vb_relative set secret_key='$kk1' where id=$rid");
				
				$mess1="Dear $rname, Received information from $name, Username:$mob1, Password:$p1, Key: $kk, Link: http://localhost/cloud_brain/login.php";
				$objEmail	=	new CI_Email();
		$objEmail->from('iotcloudadmin@iotcloud.co.in', "Cloud Brain");
		$objEmail->to("$email1");
		//$objEmail->to("sanjeevi@oculusit.in");
		
		//$objEmail->cc($txt_cc);
		//$objEmail->bcc($txt_bcc);
		$objEmail->subject("Cloud Brain - $uname");
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
				}//while
				
				
				?>
				<script>
//Using setTimeout to execute a function after 5 seconds.
setTimeout(function () {
   //Redirect with JavaScript
   window.location.href= 'setting.php?act=sent';
}, 3000);
</script>
				<?php
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
<script language="javascript">
function checkMail()
{
	if(!confirm("Are you sure send to Mail?"))
	{
	return false;
	}
	return true;
}

</script>
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
		<h3>Setting</h3>
			<div class="row">
				<div class="col-lg-6">
					<form class="contact-form" name="form1" method="post">
					<div class="col-md-8">
								<div class="form-group">
								<label>Alert Status: </label>
									
									<p>
									<?php
									if($row['alert_st']=="1")
									{
									?>
									<h5 style="color:#FF0000">In-Activate</h5> 
									
									<a href="setting.php?act=yes" class="site-btn sb-gradients sbg-line mt-5">Click to Activate</a>
									<?php
									}
									else
									{
									?>
									<h5 style="color:#00CC33">Activated</h5> 
									<a href="setting.php?act=no" class="site-btn sb-gradients sbg-line mt-5">Click to In-Activate</a>
									<?php
									}
									?>
									</p>
								</div>
							</div>
							
							<div class="col-md-8">
								<div class="form-group">
								<label>Information has send to Relatives - Manually</label>
									<p style="color:#0033CC"><?php echo $msg1; ?></p>
									<p><a href="setting.php?act=sendmail" class="site-btn sb-gradients sbg-line mt-5" onClick="return checkMail()">Click to Send</a></p>
									<?php
									if($act=="sent")
									{
									?><p style="color:#009933">Mail has Sent Successfully</p><?php
									}
									?>
								</div>
							</div>
							
					</form>
						
				</div>
				<div class="col-lg-6 mt-5 mt-lg-0">

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