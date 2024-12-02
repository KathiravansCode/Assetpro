<?php
include("include/protect.php");
include("include/dbconnect.php");
include("encrypt_msg.php");
include("encrypt.php");
include("decrypt.php");
extract($_REQUEST);

$uname=$_SESSION['uname'];
$msg="";
$qry=mysqli_query($connect,"select * from vb_register where uname='$uname'");
$row=mysqli_fetch_array($qry);
$key=$uname;
$rdate=date("d-m-Y");
if(isset($btn))
{
$qry = mysqli_query($connect,"select max(id) as maxid from vb_audio");
$rs=mysqli_fetch_array($qry);
$id = $rs['maxid']+1;

	if($_FILES['file']['name']!="")
	{
$fname="A".$id.$_FILES['file']['name'];
move_uploaded_file($_FILES['file']['tmp_name'],"audio/".$fname);
	}
	else
	{
	$fname="";
	}
	
$ftype1=fnEncrypt($ftype,$key);
$title1=fnEncrypt($title,$key);
$details1=fnEncrypt($details,$key);
$fname1=fnEncrypt($fname,$key);
$rdate1=fnEncrypt($rdate,$key);

$ins=mysqli_query($connect,"insert into vb_audio(id,uname,ftype,title,details,filename,rdate) values($id,'$uname','$ftype1','$title1','$details1','$fname1','$rdate1')");					
					
					header("location:audio.php");
}
////////////////////////////////////////////////
if($_REQUEST['act']=="del")
{
$did=$_REQUEST['did'];
$qq1=mysqli_query($connect,"select * from vb_audio where id=$did");
$rr1=mysqli_fetch_array($qq1);
$fn=$rr1['filename'];
@unlink("audio/$fn");
mysqli_query($connect,"delete from vb_audio where id=$did");
header("location:audio.php");
}
//////
if($act=="down")
{

$qq2=mysqli_query($connect,"select * from vb_audio where id=$fid");
$rr2=mysqli_fetch_array($qq2);
$fn=fnDecrypt($rr2['filename'],$key);
$crypt = "audio/$fn";
	$decrypt = "down/$fn";
	DecryptFile($crypt,$decrypt,$key);
header("location:download.php?file1=".$fn."&folder1=down");
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
		<h3>Your Audio / Video Files</h3>
			<div class="row">
				<div class="col-lg-6">
				
					<form class="contact-form" name="form1" method="post" enctype="multipart/form-data">
					<div class="col-md-8">
								<div class="form-group">
								<label>Type</label>
									<select name="ftype" class="form-control">
									<option>Audio</option>
									<option>Video</option>
								  </select> 
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-8">
								<div class="form-group">
								<label>Title</label>
									<input type="text" name="title" class="check-form" />
									<span><i class="ti-check"></i></span>
								</div>
							</div>
							<div class="col-md-8">
								<div class="form-group">
								<label>Details Audio/Video</label>
									<textarea name="details" class="check-form"></textarea>
									<span><i class="ti-check"></i></span>
								</div>
							</div>
						<div class="col-md-8">
								<div class="form-group">
								<label>Upload File</label>
									<input class="check-form" type="file" name="file" placeholder="">
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
		  $q1=mysqli_query($connect,"select * from vb_audio where uname='$uname'");
		  $n1=mysqli_num_rows($q1);
		  if($n1>0)
		  {
		  while($r1=mysqli_fetch_array($q1))
		  {
		  ?>
						<div class="row">
							
							<div class="col-md-6">
									Title of Document
							</div>
							<div class="col-md-6">
									: <?php echo fnDecrypt($r1['title'],$key); ?>
							</div>
							<div class="col-md-6">
								Details
							</div>
							<div class="col-md-6">
								: <?php echo fnDecrypt($r1['details'],$key); ?>
							</div>
							<div class="col-md-6">
								File
							</div>
							<div class="col-md-6">
								: <?php if($r1['filename']!="") { 
								
								$fna=fnDecrypt($r1['filename'],$key);
			  //echo '<a href="download.php?file1='.$fna.'&folder1=audio">'.$fna.'</a>'; 
			  echo '<a href="audio.php?act=down&fid='.$r1['id'].'">'.$fna.'</a>'; 
			  } else { echo "None"; } ?>
							</div>
							<div class="col-md-6">
								Relative
							</div>
							<div class="col-md-6">
								: <?php 
								if($r1['rid']!="0")
								{
								echo "ID:".$r1['rid'];
			  $q3=mysqli_query($connect,"select * from vb_relative where id=".$r1['rid']."");
			  $r3=mysqli_fetch_array($q3);
			  $rname=fnDecrypt($r3['name'],$key);
			  echo " - ".$rname; 
			  					}
								else
								{
								echo '-';
								}
			  ?>
							</div>
							<div class="col-md-12" style="border-bottom:#D3D3D3 solid 1px">
							<p align="right"><a href="edit_audio.php?act=audio&id=<?php echo $r1['id']; ?>">Edit</a> | 
<a href="audio.php?act=del&did=<?php echo $r1['id']; ?>" onClick="return del()">Delete</a></p>
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
