<?php
$conn = new mysqli("127.0.0.1", "root", "1234", "flower", 3306);
if ($conn->connect_error) die("Error: " . $conn->connect_error);
?>