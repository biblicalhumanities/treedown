declare function local:token($t)
{
  <w>{ string($t/@form) }</w>,
  $t/@presentation-after[. != ' '] ! <pc>{string(.)}</pc>
};

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
            then local:token($t)
            else local:unwrap($s, $stok)
        }
      </wg>
    else local:token($t)
};

for $s in //sentence
return 
  <sentence>
    {      
      let $stok := $s//token
      for $t in $stok[not(@head-id)]     
      return local:unwrap($t, $stok)
    }
  </sentence>