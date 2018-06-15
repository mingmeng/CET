<?php
require_once("AipOcr.php");
require_once("config.php");

header('Content-type: application/json');
if ($_SERVER['REQUEST_METHOD'] != 'POST')
    AipOcr::resultJson(404, 'method is wrong', '');


$typeArr=array("image/jpg","image/jpeg","image/png");
if (!in_array($_FILES['picture']['type'], $typeArr)) {
	AipOcr::resultJson(404,"type is wrong",'');
}

if ($_FILES['picture']['size']>8*1024*1024) {
	AipOcr::resultJson(404,"file is too large");
}


$binaryFile =file_get_contents($_FILES['picture']['tmp_name']);


$test = new AipOcr(config::APP_ID, config::API_KEY, config::SECRET_KEY);
$result = $test->basicGeneral($binaryFile, array(
    'detect_direction' => 'true'
));
$dataResult = array();


if (empty($result['words_result']))
    AipOcr::resultJson(404, "没有拿到结果", '');
foreach ($result['words_result'] as $value) {
    $tempValue = $value['words'];
    if (preg_match('/姓名:/', $tempValue))
        $dataResult['name'] = str_replace('姓名:', '', $tempValue);
    elseif (preg_match('/准考证号:/', $tempValue))
        $dataResult['examID'] = str_replace('准考证号:', '', $tempValue);
}

if (empty($dataResult['examID'] || empty($dataResult['name'])))
    AipOcr::resultJson(404, "the photo can`t be recognized", '');

AipOcr::resultJson(200, 'success', $dataResult);







