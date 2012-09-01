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
//Conexion a BD
require_once('parametros.php');
if (isset ($_GET['documentos'])){


$documentos = $_GET['documentos'];
$documentos = str_replace("[","",$documentos);
$documentos = str_replace("]","",$documentos);
$documentos = explode(",", $documentos);
require_once('tcpdf/config/lang/eng.php');
require_once('tcpdf/tcpdf.php');
$conexion= pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password") 
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
$pdf->SetHeaderData('logo_solvmex.jpg', PDF_HEADER_LOGO_WIDTH, 'Listado de pedidos', '', array(0,64,255), array(0,64,128));

$pdf->AddPage();
$query = "SELECT * from product_uom order by id asc;";
$result = pg_query($conexion, $query);
while ($row = pg_fetch_assoc($result)) {

$num = $row['id'];
$unidades[$num] = $row['name'];
}
$query = "SELECT stock_move.name, stock_move.product_qty,  stock_move.product_uos_qty, stock_move.note, product_uom, product_uos, 
stock_move.origin, product_product.name_template,product_product.default_code,res_partner.name AS cliente,stock_move.forma_envio,stock_move.tambores,stock_move.cantidad_tambor
FROM stock_move,product_product,res_partner WHERE stock_move.partner_id = res_partner.id AND 
product_product.id = stock_move.product_id AND stock_move.id IN
(SELECT listado_id FROM corte_listado_rel WHERE pedido_id IN ($documento)) ORDER BY stock_move.origin;";
$result = pg_query($conexion, $query);

$pdf->SetFont('helvetica', '', 6, '', true);

$html = '<h>' .$datos_corte[0] .' | ' .$datos_corte[1] . ' </p> Impresion: ' .$fecha .' ' . date('H:i:s T') .'</h>
</p>
<table border=".1"  cols="7" width="100%" cellpadding="1" >
<tr>
<th width="2%">#</th>
<th width="5%">Pedido</th>
<th width="15%">Cliente</th>
<th width="15%">Producto</th>
<th width="15%">Etiqueta</th>
<th width="6%">Cantidad</th>
<th width="5%">Unidad</th>
<th width="8%">Envase</th>
<th width="29%">Comentarios</th>
</tr>';
$num = 1;
while ($row = pg_fetch_assoc($result)) {
  $html .= '<tr><td width="2%">' .$num .'</td>';
  $html .= '<td width="5%">' .$row['origin'] .'</td>';
  $html .= '<td width="15%">' .$row['cliente'] .'</td>';
  $html .= '<td width="15%">' .$row['default_code'] . '|' .$row['name_template'] .'</td>';
  $html .= '<td width="15%">' .$row['name'] .'</td>';
  $html .= '<td width="6%">' .$row['product_uos_qty'] .'</td>';
  $html .= '<td width="5%">' . $unidades[$row['product_uos']].'</td>';
  $html .= '<td width="8%">' .$row['forma_envio'] ." | " .$row['tambores'] ." | " .$row['cantidad_tambor'] .'</td>';
  $html .= '<td width="29%">' .$row['note'] .'</td></tr>';
  
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
		$fileatt = $pdf->Output("Listado$random.pdf", 'I');
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
