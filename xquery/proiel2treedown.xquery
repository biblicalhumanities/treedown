declare function local:token($t)
{
  <w>
    {
      attribute role {$t/@relation},
      attribute id {$t/@id},
      attribute head-id {$t/@head-id }
    }
    {
      string($t/@form)
    }
  </w>,
  $t/@presentation-after[. != ' '] ! <pc>{string(.)}</pc>
};


declare function local:unwrap($t, $stok)
{
  let $children :=  $stok[@head-id = $t/@id]
  let $seq := ($children | $t)/.
  return
    if ($children)
    then 
      <wg role="{$t/@relation}">
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

declare function local:sentence($s)
{
  <sentence>
    {
      attribute id { $s/@id }
    }  
    {      
      let $stok := $s//token
      for $t in $stok[not(@head-id)]     
      return local:unwrap($t, $stok)
    }
  </sentence>  
};


<?xml-stylesheet href="treedown.css"?>,
<?xml-stylesheet href="boxwood.css"?>,
<book>
  {
    for $s in //sentence
    return local:sentence($s)
  }
</book>