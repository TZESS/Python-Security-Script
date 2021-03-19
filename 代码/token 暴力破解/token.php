<?php
session_start();
@$name=$_POST['username'];
@$pass=$_POST['password'];

//生成token
function setToken(){
    $_SESSION['session_token'] = md5( uniqid() );
}

//比较token
function validToken(){
    //先进行比较
    $return=$_POST['csrfToken']==$_SESSION['session_token'] ? true : false;
    //不管结果是否正确，都会重新生成新的token
    setToken();
    return $return;
}

//如果未设置token或token为空，则重新生成一个token
if(!isset($_SESSION['session_token']) || $_SESSION['session_token']==''){
    echo($_SESSION['session_token']);
    setToken();
}
if(isset($_POST['submit'])){
    if(!validToken()){
        echo "token error<br>";
    }else{
        if($name==='admin' && $pass==='admin'){     #简单测试
            echo "login success";
        }
        else{
            header("Location: http://127.0.0.1/token.php");
            exit();
        }   
    }
}



?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="token.php" method="POST">
        用户名<input type="text" name="username"><br>
        密码<input type="text" name="password"><br>
        <input type="hidden" name="csrfToken" value="<?php echo $_SESSION['session_token'] ?>">
        <input type="submit" name='submit'>
    </form>
</body>
</html>
