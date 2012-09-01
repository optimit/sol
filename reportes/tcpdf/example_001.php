<?php
//============================================================+
// File name   : example_001.php
// Begin       : 2008-03-04
// Last Update : 2012-07-25
//
// Description : Example 001 for TCPDF class
//               Default Header and Footer
//
// Author: Nicola Asuni
//
// (c) Copyright:
//               Nicola Asuni
//               Tecnick.com LTD
//               Manor Coach House, Church Hill
//               Aldershot, Hants, GU12 4RQ
//               UK
//               www.tecnick.com
//               info@tecnick.com
//============================================================+
if (isset ($_GET['documentos'])){


$documentos = $_GET['documentos'];
$documentos = explode(",", $documentos);
require_once('config/lang/eng.php');
require_once('tcpdf.php');
$conexion= pg_connect("host=localhost port=5432 dbname=solvmex_gil_v0 user=openerp password=Burlpen61") 
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
$pdf->SetHeaderData('logo_solvmex.jpg', PDF_HEADER_LOGO_WIDTH, 'Listado de pedidos', 'Fecha y num de folio', array(0,64,255), array(0,64,128));
$pdf->setFooterData($tc=array(0,64,0), $lc=array(0,64,128));

// set header and footer fonts
$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
$pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

// set default monospaced font
$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

//set margins
$pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
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
$pdf->AddPage();
$query = "SELECT * from product_uom order by id asc;";
$result = pg_query($conexion, $query);
while ($row = pg_fetch_assoc($result)) {

$num = $row['id'];
$unidades[$num] = $row['name'];
}
$query = "SELECT stock_move.name,stock_move.product_qty,stock_move.note,product_uom, product_uos,stock_move.origin, product_product.name_template,product_product.default_code FROM stock_move,product_product WHERE product_product.id = stock_move.product_id AND stock_move.id IN (SELECT listado_id FROM corte_listado_rel WHERE pedido_id IN ($documento));";
$result = pg_query($conexion, $query);



$html ='
<table border=".5" cellspacing="1" cellpadding="1" cols="7">
<tr>
<th>Pedido</th>
<th>Producto</th>
<th>Etiqueta</th>
<th>Cantidad</th>
<th>Unidad</th>
<th>Envase</th>
<th>Unidad de venta</th>
</tr>';
while ($row = pg_fetch_assoc($result)) {
  $html .= '<tr><td>' .$row['origin'] .'</td>';
  $html .= '<td>' .$row['default_code'] . '|' .$row['name_template'] .'</td>';
  $html .= '<td>' .$row['name'] .'</td>';
  $html .= '<td>' .$row['product_qty'] .'</td>';
  $html .= '<td>' . $unidades[$row['product_uom']].'</td>';
  $html .= '<td>' .substr($row['note'],8) .'</td>';
  $html .= '<td>' .$unidades[$row['product_uos']] .'</td></tr>';
}

$html .= '
</table>';

// output the HTML content
$pdf->writeHTML($html, true, false, true, false, '');

// ---------------------------------------------------------

// Close and output PDF document
// This method has several options, check the source code documentation for more information.
}
$pdf->Output('Listado.pdf', 'I');
} else {
echo "No se especifico el numero de documento";
}
//============================================================+
// END OF FILE
//============================================================+
