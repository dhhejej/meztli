<?php
header("Content-Type: application/json");
require_once 'config.php';

$action = $_GET['action'] ?? '';
$categoria = $_GET['categoria'] ?? '';
$input = json_decode(file_get_contents('php://input'), true);

if ($action == 'login') {
    $u = $input['user']; $p = $input['pwd'];
    $res = $conn->query("SELECT * FROM usuarios WHERE BINARY usuario='$u' AND BINARY password='$p'");
    echo json_encode(["status" => $res->num_rows > 0 ? "success" : "error"]);
} 
elseif ($action == 'reporte') {
    $res = $conn->query("SELECT * FROM $categoria ORDER BY id DESC");
    echo json_encode($res->fetch_all(MYSQLI_ASSOC));
}
// Agrega aquí las demás acciones (guardar, eliminar) siguiendo el mismo patrón
?>