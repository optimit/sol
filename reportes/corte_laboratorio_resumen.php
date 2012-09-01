<?php
//============================================================+
// Archivo  : corte_laboratorio.php
// Inicio       : 2008-03-04
// Ultima actualizacion : 2012-07-25
//
// Descripcion : Example 001 for TCPDF class
//               Default Header and Footer
//
// Autor: optimIT | Ricardo Avila | ricardo@optimit.com.mx
//
//               www.optimit.com.mx
//============================================================+
require_once "Mail.php";
require_once "Mail/mime.php";

if (isset ($_GET['documentos'])){


$documentos = $_GET['documentos'];
$documentos = str_replace("[","",$documentos);
$documentos = str_replace("]","",$documentos);
$documentos = explode(",", $documentos);
require_once('tcpdf/config/lang/eng.php');
require_once('tcpdf/tcpdf.php');
$conexion= pg_connect("host=192.168.1.4 port=5432 dbname=solvmex user=postgres password=Base#$DF") 
   or die ("Nao consegui conectar ao PostGres --> " . pg_last_error($conn)); 
// SE CREA EL DOCUMENTO CON FORMATO HORIZONTAL
//define ('PDF_PAGE_ORIENTATION', 'L');
$pdf = new TCPDF('L', PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);

// set document information
$pdf->SetCreator(PDF_CREATOR);
$pdf->SetAuthor('Solvmex S.A.');
$pdf->SetTitle('Listado de pedidos');
$pdf->SetSubject('TCPDF Tutorial');

// set default header data
$dias = array("Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sábado");
$meses = array("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");

$fecha = $dias[date('w')]." ".date('d')." de ".$meses[date('n')-1]. " del ".date('Y');

$pdf->setFooterData($tc=array(0,64,0), $lc=array(0,64,128));

// set header and footer fonts
$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
$pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

// set default monospaced font
$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

//set margins
$pdf->SetMargins(5, 25, 5);
$pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
$pdf->SetFooterMargin(PDF_MARGIN_FOOTER);

//set auto page breaks
$pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);

//set image scale factor
$pdf->setImageScale(PDF_IMAGE_SCALE_RATIO);

//set some language-dependent strings
$pdf->setLanguageArray($l);

// ---------------------------------------------------------

// set default font subsetting mode
$pdf->setFontSubsetting(true);

// Set font
// dejavusans is a UTF-8 Unicode font, if you only need to
// print standard ASCII chars, you can use core fonts like
// helvetica or times to reduce file size.
$pdf->SetFont('helvetica', '', 8, '', true);

// Add a page
// This method has several options, check the source code documentation for more information.
   

foreach ($documentos As $documento){
$query = "SELECT name,fecha_corte FROM laboratorio_corte WHERE id IN ($documento);";
$result = pg_query($conexion, $query);
$datos_corte = pg_fetch_array($result);
$pdf->setHeaderData('logo_solvmex.jpg', PDF_HEADER_LOGO_WIDTH, 'Listado de pedidos - Resumen por producto, envasado de tambores', '', array(0,64,255), array(0,64,128));

$pdf->AddPage();
$query = "SELECT * from product_uom order by id asc;";
$result = pg_query($conexion, $query);
while ($row = pg_fetch_assoc($result)) {

$num = $row['id'];
$unidades[$num] = $row['name'];
}
$query = "SELECT stock_move.name,stock_move.tambores, SUM(stock_move.product_qty) AS cantidad,SUM(stock_move.cantidad_tambor) AS tambores_cantidad
FROM stock_move,product_product,res_partner WHERE stock_move.partner_id = res_partner.id AND 
product_product.id = stock_move.product_id AND stock_move.id IN
(SELECT listado_id FROM corte_listado_rel WHERE pedido_id IN ($documento)) GROUP BY stock_move.name,stock_move.tambores  ORDER BY stock_move.name ;";
$result = pg_query($conexion, $query);



$html = '<h>' .$datos_corte[0] .' | ' .$datos_corte[1] . ' </p> Impresion: ' .$fecha .' ' . date('H:i:s T') .'</h>
</p>
<table border="1"  cols="6" width="100%" cellpadding="1" >
<tr>
<th width="2%">#</th>
<th width="20%">Producto</th>
<th width="10%">Tipo de envase</th>
<th width="30%">Cantidad (Litros)</th>
<th width="15%">N&uacute;mero de tambores</th>
<th>Comentarios</th>
</tr>';
$num = 1;
while ($row = pg_fetch_assoc($result)) {
  $html .= '<tr><td width="2%">' .$num .'</td>';
  $html .= '<td width="20%">' .$row['name'] .'</td>';
  $html .= '<td width="10%" align="center">' .$row['tambores'] .'</td>';
  $html .= '<td width="30%">' .$row['cantidad'] .'</td>';
  $html .= '<td width="15%">' .$row['tambores_cantidad'] .'</td>';
  $html .= '<td></td></tr>';
  
  $num += 1;
}

$html .= '
';
$html .= '</table>';
// output the HTML content
//$pdf->writeHTML($html, true, false, true, false, '');
$pdf->writeHTML($html, true, false,false,false,'left');
// ---------------------------------------------------------

// Close and output PDF document
// This method has several options, check the source code documentation for more information.
}
		$random = rand (10,1000);
		$fileatt = $pdf->Output("Listado_producto$random.pdf", 'I');
		// $data = chunk_split($fileatt);
		// $from = "optimitit<ricardo.avila.garcia@gmail.com>";
		// $to = "ricardo@optimit.com.mx";
		// $subject = "Prueba";
		// $host = "ssl://smtp.gmail.com";
		// $port = "465";
		// $username = "ricardo.avila.garcia@gmail.com";
		// $password = "ajonjoli";

		// $message = new Mail_mime();
		// $message->setTXTBody("Mensaje de prueba");
		// $message->addAttachment("Listado$random.pdf");
		// $body = $message->get();
		// $extraheaders = array("From" => $from, "To" => $to, "Subject"=>$subject,"Reply-To"=>$from);
		// $headers = $message->headers($extraheaders);
		// $mail = Mail::factory('smtp',
		  // array ('host' => $host,
			// 'port' => $port,
			// 'auth' => true,
			// 'username' => $username,
			// 'password' => $password));
		// $mail->send($to, $headers, $body);
		// @unlink("Listado$random.pdf");

} else {
echo "No se especifico el numero de documento";
}
//============================================================+
// END OF FILE
//============================================================+
