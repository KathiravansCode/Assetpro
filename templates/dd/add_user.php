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

$rdate=date("d-m-Y");
if(isset($btn))
{
	$uq1=mysqli_query($connect,"select * from vb_register where uname='$userid'");
	$un1=mysqli_num_rows($uq1);
	$uq2=mysqli_query($connect,"select * from vb_user where userid='$userid'");
	$un2=mysqli_num_rows($uq2);
	
	if($un1==0 && $un2==0)
	{
$msg1="Sending to Mail...";		
	
$qry = mysqli_query($connect,"select max(id) as maxid from vb_user");
$rs=mysqli_fetch_array($qry);
$id = $rs['maxid']+1;
$ps=rand(100,999);
$pass=$id.$ps;

$name1=fnEncrypt($name,$key);
$mobile1=fnEncrypt($mobile,$key);
$email1=fnEncrypt($email,$key);
$pass1=fnEncrypt($pass,$key);
$rdate1=fnEncrypt($rdate,$key);

$ins=mysqli_query($connect,"insert into vb_user(id,uname,name,mobile,email,userid,pass,rdate) values($id,'$uname','$name1','$mobile1','$email1','$userid','$pass1','$rdate1')");					
//header("location:add_user.php");

$message="Dear $name, Sub User ID: $userid, Password: $pass, by $uname";
	

			$objEmail	=	new CI_Email();
			$objEmail->from('iotcloudadmin@iotcloud.co.in', "Cloud Brain");
			$objEmail->to("$email");
			
			//$objEmail->cc($txt_cc);
			//$objEmail->bcc($txt_bcc);
			$objEmail->subject("Sub User Info");
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
			
			?>
			<script>
//Using setTimeout to execute a function after 5 seconds.
setTimeout(function () {
   //Redirect with JavaScript
   window.location.href= 'add_user.php';
}, 3000);
</script>
			<?php


	}
	else
	{
	$msg="User Id Already Exist!";
	}
}
///////////////////
if($_REQUEST['act']=="del")
{
$did=$_REQUEST['did'];
mysqli_query($connect,"delete from vb_user where id=$did");
header("location:add_user.php");
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
function del()
{
	if(!confirm("Are you sure want to delete?"))
	{
	return false;
	}
	return true;
}
function validate()
{
  	if(document.form1.name.value=="")
	{
	alert("Enter the Name");
	document.form1.name.focus();
	return false;
	}
	
	if(document.form1.mobile.value=="")
	{
	alert("Enter the Mobile No.");
	document.form1.mobile.focus();
	return false;
	}
	if (isNaN(document.form1.mobile.value))
                {
                    alert("Invalid Mobile No.");
                    document.form1.mobile.select();
                    return false;
                }
				if (document.form1.mobile.value.length != 10)
                {
                    alert("10 digists only allowed!!");
                    document.form1.mobile.select();
                    return false;
                }
	if(document.form1.email.value=="")
	{
	alert("Enter the E-mail");
	document.form1.email.focus();
	return false;
	}
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.form1.email.value))  
				  {  
					//return (true)  
				  }  
				  else
				  {
					alert("You have entered an invalid email address!");
					document.form1.email.select();
					return false; 
				  }
	if(document.form1.userid.value=="")
	{
	alert("Enter the User ID");
	document.form1.userid.focus();
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
		<h3>Sub User Information</h3>
			<div class="row">
				<div class="col-lg-6">
				<span style="color:#FF0000"><?php echo $msg; ?></span>
				<span style="color:#0033CC"><?php echo $msg1; ?></span>
					<form class="contact-form" name="form1" method="post">
					<div class="col-md-8">
								<div class="form-group">
								<label>Name</label>
									<input class="check-form" type="text" name="name" placeholder="">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							
							<div class="col-md-8">
								<div class="form-group">
								<label>Mobile No.</label>
									<input class="check-form" type="text" name="mobile" maxlength="10" placeholder="">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-8">
								<div class="form-group">
								<label>E-mail</label>
									<input class="check-form" type="text" name="email" placeholder="">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-8">
								<div class="form-group">
								<label>User ID</label>
									<input class="check-form" type="text" name="userid" placeholder="">
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							
					<div class="col-md-12">
								<button type="submit" name="btn" class="site-btn sb-gradients mt-4" onClick="return validate()">Add</button>
							</div>
					</form>
						
				</div>
				<div class="col-lg-6 mt-5 mt-lg-0">
					
					<?php
		  $q1=mysqli_query($connect,"select * from vb_user where uname='$uname'");
		  $n1=mysqli_num_rows($q1);
		  if($n1>0)
		  {
		  while($r1=mysqli_fetch_array($q1))
		  {
		  ?>
						<div class="row">
						
							<div class="col-md-6">
									Name
							</div>
							<div class="col-md-6">
									: <?php echo fnDecrypt($r1['name'],$key); ?>
							</div>
							<div class="col-md-6">
								User ID
							</div>
							<div class="col-md-6">
								: <?php echo $r1['userid']; ?>
							</div>
							<div class="col-md-6">
								Mobile No.
							</div>
							<div class="col-md-6">
								: <?php echo fnDecrypt($r1['mobile'],$key); ?>
							</div>
							<div class="col-md-6">
								E-mail
							</div>
							<div class="col-md-6">
								: <?php echo fnDecrypt($r1['email'],$key); ?>
							</div>
							
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"><a href="edit_user.php?id=<?php echo $r1['id']; ?>">Edit</a> | 
			  <a href="add_user.php?act=del&did=<?php echo $r1['id']; ?>" onClick="return del()">Delete</a></p>
							</div>
						</div>
						
				<?php
				}
				}
				else
				{
				?>
				<img src="img/cbr7.jpg" class="img-fluid" alt="">
				<?php
				}
				?>			
		  
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