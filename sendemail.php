<?php

if (isset($_POST['email'])){
    echo "testing"
}
require("phpmailer/class.phpmailer.php");
$mail = new PHPMailer();

$mail->name = $_POST['name']; 
$mail->email = $_POST['email']; 
$mail->subject = $_POST['subject']; 
$mail->message = $_POST['message']; 

$mail->email_from = $email;
$mail->email_to = 'novelbooksinc@gmail.com';

$mail->body = 'Name: ' . $name . "\n\n" . 'Email: ' . $email . "\n\n" . 'Subject: ' . $subject . "\n\n" . 'Message: ' . $message;

$mail->Host = "ssl://smtp.gmail.com"; // GMail
    $mail->Port = 465;
    $mail->IsSMTP(); // use SMTP
    $mail->SMTPAuth = true; // turn on SMTP authentication
    $mail->From = $mail->Username;
    if(!$mail->Send())
        echo "Mailer Error: " . $mail->ErrorInfo;
    else
        echo "Message has been sent";
?>
