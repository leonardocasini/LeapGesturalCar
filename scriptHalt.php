
<?php
$behavior = $_GET['behavior'];
echo $behavior;
$a- exec("sudo python /var/www/html/apiLeorio/test.py ".$behavior);
echo $a;

?>