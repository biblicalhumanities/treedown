declare function local:unwrap($t, $stok)
{
  let $children :=  $stok[@head-id = $t/@id]
  let $seq := ($children | $t)/.
  return
    if ($children)
    then 
      <wg relation="{$t/@relation}">
        {
          for $s in $seq
          return 
            if ($s is $t)
            then $t
            else local:unwrap($s, $stok)
        }
      </wg>
    else $t
};

for $s in //sentence
let $stok := $s//token
let $t := $stok[not(@head-id)][1]  (: hack ... get rid of subscript :)
return 
  <sentence>
    {
      local:unwrap($t, $stok)
    }
  </sentence>