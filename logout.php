<?php
session_start();
session_unset();    // Elimina las variables
session_destroy();  // Destruye la sesión
setcookie("id_usuario", "", time() - 3600, "/");
header("Location: index.php");
exit();
?>