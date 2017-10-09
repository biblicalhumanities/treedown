declare variable $pos := //parts-of-speech;

declare function local:pos($t)
{
  let $description :=  string($pos/value[@tag = $t/@part-of-speech]/@summary)
  let $class :=
    switch ($description)
      case "interrogative adverb" return "adverb"
      case "relative adverb" return "adverb"
      case "common noun" return "noun"
      case "proper noun" return "noun"
      case "cardinal numeral" return "numeral"
      case "ordinal numeral" return "numeral"      
      case "demonstrative pronoun" return "pronoun"
      case "indefinite pronoun" return "pronoun"
      case "interrogative pronoun" return "pronoun"
      case "relative pronoun" return "pronoun"
      case "personal pronoun" return "pronoun"
      case "personal reflexive pronoun" return "pronoun"
      case "possessive pronoun" return "pronoun"
      case "possessive reflexive pronoun" return "pronoun"
      case "reciprocal pronoun" return "pronoun"
      case "" return ()
      default return $description
  let $type :=
    switch ($description)
      case "interrogative adverb" return "interrogative"
      case "relative adverb" return "relative"
      case "common noun" return "common"
      case "proper noun" return "proper"
      case "cardinal numeral" return "cardinal"
      case "ordinal numeral" return "ordinal"      
      case "demonstrative pronoun" return "demonstrative"
      case "indefinite pronoun" return "indefinite"
      case "interrogative pronoun" return "interrogative"
      case "relative pronoun" return "relative"
      case "personal pronoun" return "personal"
      case "personal reflexive pronoun" return "personal relative"
      case "possessive pronoun" return "possessive"
      case "possessive reflexive pronoun" return "possessive reflexive"
      case "reciprocal pronoun" return "reciprocal"
      default return ()  
  return
    (
      $class ! attribute class {$class},
      $type ! attribute type {$type}
    )
};

declare function local:token($t)
{
  <w>
    {
      local:pos($t),
      attribute role {$t/@relation},
      attribute id {$t/@id},
      $t/@head-id ! attribute head-id {$t/@head-id }
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