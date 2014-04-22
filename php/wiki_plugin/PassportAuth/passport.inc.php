<?php
session_start();

$passport_url = 'http://passport.com/login.php';
$passport_login_timeout = 86400; // passport登录状态重新验证时间间隔
$passport_username = isset($_SESSION['passport_username']) ? $_SESSION['passport_username'] : false;
$tmp_passport_logout=isset($_GET["passport_logout"]) ? $_GET["passport_logout"]: false;
if ($tmp_passport_logout) {
	//退出登录状态
	passport_logout($passport_url);
} elseif ($passport_username and $_SESSION['passport_ticket']) {
	//已登录状态流程处理
	passport_logon($passport_username, $passport_login_timeout, $passport_url);
	//error_log("pl: <$passport_username>");
	$passport_login_succeed = 1; //登录成功
} elseif (!empty($_GET["ticket"])) {
	//passport登录成功，验证passport返回票据有效性
	//error_log("tc: <$passport_username>");
	passport_ticket_check($passport_username,$passport_url);
} else {
	//未登录状态则跳转到passport登录页面
	passport_redirect($passport_url);
}

if ($passport_login_succeed != 1) {
	passport_redirect($passport_url);
}
### 登录流程处理完成 ###

function passport_ticket_check($passport_username, $passport_url) {
	$passport_username = auth_check_valid($_GET['ticket']);
	if ($passport_username) {
		//票验证成功
		$_SESSION["passport_username"] = $passport_username;
		$_SESSION["passport_ticket"] = $_GET['ticket'];
		$_SESSION["passport_check"] = time();
		if ($_SESSION["passport_forward"]) {
			$r_url = $_SESSION["passport_forward"];
		} else {
			$r_url = "http://".$_SERVER["HTTP_HOST"].$_SERVER["SCRIPT_NAME"]."?";
		}
		//登录成功，跳回登录前页面(url中去掉_GET["ticket"])
		header("Location: $r_url");
		exit;
		
	} else {
        	$forward = "http://".$_SERVER["HTTP_HOST"].$_SERVER["SCRIPT_NAME"].'?'.$_SERVER["QUERY_STRING"];
		$forward = rawurlencode($forward);
		header("Location: $passport_url?forward=$forward");
        	exit;
	}
}

function passport_logon($passport_username, $passport_login_timeout, $passport_url) {
	//已登录时间超过设定值,则重新验证票的有效性
        if (time() - $_SESSION["passport_check"] > $passport_login_timeout) {
		if (auth_check_valid($_SESSION['passport_ticket']) != $passport_username) {
                        $forward = "http://".$_SERVER["HTTP_HOST"].$_SERVER["SCRIPT_NAME"].'?'.$_SERVER["QUERY_STRING"];
			$_SESSION["passport_forward"] = $forward;
			unset($_SESSION["passport_ticket"]);
                        $forward = rawurlencode($forward);
			header("Location: $passport_url?m=passport&forward=$forward");
                        exit;
		} else {
			$_SESSION["passport_check"] = time();
		}
        }
}

function passport_redirect($passport_url) {
	$forward = "http://".$_SERVER["HTTP_HOST"].$_SERVER["SCRIPT_NAME"].'?'.$_SERVER["QUERY_STRING"];
	$_SESSION["passport_forward"] = $forward;
	$forward = rawurlencode($forward);
	header("Location: $passport_url?forward=$forward");
	exit;
}

function passport_logout($passport_url) {
	unset($_SESSION['passport_ticket']);
	unset($_SESSION['passport_forward']);
	$forward = "http://".$_SERVER["HTTP_HOST"].$_SERVER["SCRIPT_NAME"];
	header("Location: $passport_url?act=logout");
        exit;
}

//passport返回票据验证
function auth_check_valid($ticket){

        $opts=array(
                'http'=>array(
                'header'=>"Referer :".$_SERVER['REQUEST_URI']
                )
        );

        $context = stream_context_create($opts);//构造HTTP REFERER头
        $url = "https://passport./verify.php?t=".$ticket;
        $user_id = file_get_contents($url,false,$context);//二次验证，远程请求用户名

        return $user_id;//返回登录用户名，需进行后续判断是否为空串

}
?>
