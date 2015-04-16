Feature: Parse article XML
  In order to generate XML
  As a user
  I want to parse data from article XML


  Scenario: Parse article XML files
    Given I have the document <document>
    When I build article from xml
    Then I have errors <errors>
    
  Examples:
    | document              | errors
    | elife00013.xml        | False            
    | elife_poa_e06828.xml  | False             
    | elife_poa_e02923.xml  | False 

  Scenario: Parse article XML files attributes
    Given I have the document <document>
    When I build article from xml
    And I set the object to article
    And I have the attribute <attribute>
    Then I have object attribute value <value>
    
  Examples:
    | document              | attribute      | value  
    | elife00013.xml        | doi            | 10.7554/eLife.00013
    | elife00013.xml        | manuscript     | 00013
    | elife00013.xml        | volume         | 1
    | elife00013.xml        | articleType    | research-article
    | elife00013.xml        | title          | A bacterial sulfonolipid triggers multicellular development in the closest living relatives of animals
    | elife00013.xml        | abstract       | Bacterially-produced small molecules exert profound influences on animal health, morphogenesis, and evolution through poorly understood mechanisms. In one of the closest living relatives of animals, the choanoflagellate <italic>Salpingoeca rosetta</italic>, we find that rosette colony development is induced by the prey bacterium <italic>Algoriphagus machipongonensis</italic> and its close relatives in the Bacteroidetes phylum. Here we show that a rosette inducing factor (RIF-1) produced by <italic>A. machipongonensis</italic> belongs to the small class of sulfonolipids, obscure relatives of the better known sphingolipids that play important roles in signal transmission in plants, animals, and fungi. RIF-1 has extraordinary potency (femtomolar, or 10<sup>−15</sup> M) and <italic>S. rosetta</italic> can respond to it over a broad dynamic range—nine orders of magnitude. This study provides a prototypical example of bacterial sulfonolipids triggering eukaryotic morphogenesis and suggests molecular mechanisms through which bacteria may have contributed to the evolution of animals.    
    | elife00013.xml        | is_poa         | False
    
    | elife_poa_e06828.xml  | doi            | 10.7554/eLife.06828 
    | elife_poa_e06828.xml  | manuscript     | 06828
    | elife_poa_e06828.xml  | volume         | None
    | elife_poa_e06828.xml  | articleType    | research-article
    | elife_poa_e06828.xml  | title          | <italic>Cis</italic> and <italic>trans</italic> RET signaling control the survival and central projection growth of rapidly adapting mechanoreceptors
    | elife_poa_e06828.xml  | abstract       | RET can be activated in <italic>cis</italic> or <italic>trans</italic> by its co-receptors and ligands <italic>in vitro</italic>, but the physiological roles of <italic>trans</italic> signaling are unclear. Rapidly adapting (RA) mechanoreceptors in dorsal root ganglia (DRGs) express <italic>Ret</italic> and the co-receptor <italic>Gfrα2</italic> and depend on <italic>Ret</italic> for survival and central projection growth. Here, we show that <italic>Ret</italic> and <italic>Gfrα2</italic> null mice display comparable early central projection deficits, but <italic>Gfrα2</italic> null RA mechanoreceptors recover later. Loss of <italic>Gfrα1</italic>, the co-receptor implicated in activating RET <italic>in trans</italic>, causes no significant central projection or cell survival deficit, but <italic>Gfrα1;Gfrα2</italic> double nulls phenocopy <italic>Ret</italic> nulls. Finally, we demonstrate that GFRα1 produced by neighboring DRG neurons activates RET in RA mechanoreceptors. Taken together, our results suggest that <italic>trans</italic> and <italic>cis</italic> RET signaling could function in the same developmental process and that the availability of both forms of activation likely enhances but not diversifies outcomes of RET signaling.
    | elife_poa_e06828.xml  | is_poa         | True
    
    | elife_poa_e02923.xml  | doi            | 10.7554/eLife.02923
    | elife_poa_e02923.xml  | manuscript     | 02923
    | elife_poa_e02923.xml  | volume         | None
    | elife_poa_e02923.xml  | articleType    | research-article
    | elife_poa_e02923.xml  | title          | Potassium dependent rescue of a myopathy with core-like structures in mouse
    | elife_poa_e02923.xml  | abstract       | Myopathies decrease muscle functionality. Mutations in ryanodine receptor 1 (RyR1) are often associated with myopathies with microscopic core-like structures in the muscle fiber. Here we identify a mouse RyR1 model in which heterozygous animals display clinical and pathological hallmarks of myopathy with core-like structures. The RyR1 mutation decreases sensitivity to activated calcium release and myoplasmic calcium levels, subsequently affecting mitochondrial calcium and ATP production. Mutant muscle shows a persistent potassium leak and disrupted expression of regulators of potassium homeostasis. Inhibition of K<sub>ATP</sub> channels or increasing interstitial potassium by diet or FDA-approved drugs can reverse the muscle weakness, fatigue-like physiology and pathology. We identify regulators of potassium homeostasis as biomarkers of disease that may reveal therapeutic targets in human patients with myopathy of central core disease (CCD). Altogether, our results suggest that amelioration of potassium leaks through potassium homeostasis mechanisms may minimize muscle damage of myopathies due to certain RyR1 mutations.
    | elife_poa_e02923.xml  | is_poa         | True
  

  Scenario: Parse article XML file properties
    Given I have the document <document>
    When I build article from xml
    And I set the object to article <property> index <index>
    And I have the attribute <attribute>
    Then I have object attribute value <value>
    
  Examples:
    | document              | property           | index   | attribute      | value  
    | elife00013.xml        | contributor        | 0       | contrib_type   | author
    | elife00013.xml        | contributor        | 0       | surname        | Alegado
    | elife00013.xml        | contributor        | 0       | given_name     | Rosanna A
    | elife00013.xml        | contributor        | 0       | collab         | None
    | elife00013.xml        | contributor        | 0       | corresp        | False
    | elife00013.xml        | license            |         | href           | http://creativecommons.org/licenses/by/3.0/
    | elife00013.xml        | article_categories | 0       |                | Cell biology
    | elife00013.xml        | author_keywords    | 0       |                | Salpingoeca rosetta
    | elife00013.xml        | research_organisms | 0       |                | Other
    
    | elife_poa_e06828.xml  | contributor        | 0       | contrib_type   | author
    | elife_poa_e06828.xml  | contributor        | 0       | surname        | Fleming
    | elife_poa_e06828.xml  | contributor        | 0       | given_name     | Michael S
    | elife_poa_e06828.xml  | contributor        | 0       | collab         | None
    | elife_poa_e06828.xml  | contributor        | 0       | corresp        | False
    | elife_poa_e06828.xml  | contributor        | 6       | corresp        | True 
    | elife_poa_e06828.xml  | license            |         | href           | http://creativecommons.org/licenses/by/4.0/
    | elife_poa_e06828.xml  | article_categories | 0       |                | Developmental biology and stem cells
    | elife_poa_e06828.xml  | article_categories | 1       |                | Neuroscience
    | elife_poa_e06828.xml  | author_keywords    | 0       |                | neurotrophins
    | elife_poa_e06828.xml  | research_organisms | 0       |                | Mouse
    
    | elife_poa_e02923.xml  | contributor        | 0       | contrib_type   | author
    | elife_poa_e02923.xml  | contributor        | 0       | surname        | Hanson
    | elife_poa_e02923.xml  | contributor        | 0       | given_name     | M Gartz
    | elife_poa_e02923.xml  | contributor        | 0       | collab         | None
    | elife_poa_e02923.xml  | contributor        | 0       | corresp        | False
    | elife_poa_e02923.xml  | license            |         | href           | http://creativecommons.org/licenses/by/4.0/
    | elife_poa_e02923.xml  | article_categories | 0       |                | Cell biology
    | elife_poa_e02923.xml  | author_keywords    | 0       |                | ryanodine receptor
    | elife_poa_e02923.xml  | research_organisms | 0       |                | Human


# TODO!!!
# history_dates
# pub_dates
