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
    | elife02935.xml        | False 

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
  
    | elife02935.xml        | doi            | 10.7554/eLife.02935
    | elife02935.xml        | manuscript     | 02935
    | elife02935.xml        | volume         | 3
    | elife02935.xml        | articleType    | research-article
    | elife02935.xml        | title          | Origins and functional consequences of somatic mitochondrial DNA mutations in human cancer
    | elife02935.xml        | abstract       | Recent sequencing studies have extensively explored the somatic alterations present in the nuclear genomes of cancers. Although mitochondria control energy metabolism and apoptosis, the origins and impact of cancer-associated mutations in mtDNA are unclear. In this study, we analyzed somatic alterations in mtDNA from 1675 tumors. We identified 1907 somatic substitutions, which exhibited dramatic replicative strand bias, predominantly C > T and A > G on the mitochondrial heavy strand. This strand-asymmetric signature differs from those found in nuclear cancer genomes but matches the inferred germline process shaping primate mtDNA sequence content. A number of mtDNA mutations showed considerable heterogeneity across tumor types. Missense mutations were selectively neutral and often gradually drifted towards homoplasmy over time. In contrast, mutations resulting in protein truncation undergo negative selection and were almost exclusively heteroplasmic. Our findings indicate that the endogenous mutational mechanism has far greater impact than any other external mutagens in mitochondria and is fundamentally linked to mtDNA replication.
    | elife_poa_e07118.xml  | doi            | 10.7554/eLife.07118
    | elife_poa_e07118.xml  | manuscript     | 07118
    | elife_poa_e07118.xml  | volume         | None
    | elife_poa_e07118.xml  | articleType    | research-article
    | elife_poa_e07118.xml  | title          | Coordination of peptidoglycan synthesis and outer membrane constriction during <italic>Escherichia coli</italic> cell division
    | elife_poa_e07118.xml  | abstract       | To maintain cellular structure and integrity during division, Gram-negative bacteria must carefully coordinate constriction of a tripartite cell envelope of inner membrane (IM), peptidoglycan (PG) and outer membrane (OM). It has remained enigmatic how this is accomplished. Here, we show that envelope machines facilitating septal PG synthesis (PBP1B-LpoB complex) and OM constriction (Tol system) are physically and functionally coordinated via YbgF, renamed CpoB (<underline><bold>C</bold></underline>oordinator of <underline><bold>P</bold></underline>G synthesis and <underline><bold>O</bold></underline>M constriction, associated with PBP1<underline><bold>B</bold></underline>). CpoB localizes to the septum concurrent with PBP1B-LpoB and Tol at the onset of constriction, interacts with both complexes, and regulates PBP1B activity in response to Tol energy state. This coordination links PG synthesis with OM invagination and imparts a unique mode of bifunctional PG synthase regulation by selectively modulating PBP1B cross-linking activity. Coordination of the PBP1B and Tol machines by CpoB contributes to effective PBP1B function <italic>in vivo</italic> and maintenance of cell envelope integrity during division.
    | elife_poa_e07118.xml  | is_poa         | True
    | elife_poa_e00662.xml  | abstract       | <italic>Candida albicans</italic> is both a member of the healthy human microbiome and a major pathogen in immunocompromised individuals. Infections are typically treated with azole inhibitors of ergosterol biosynthesis often leading to drug resistance. Studies in clinical isolates have implicated multiple mechanisms in resistance, but have focused on large-scale aberrations or candidate genes, and do not comprehensively chart the genetic basis of adaptation. Here, we leveraged next-generation sequencing to analyze 43 isolates from 11 oral candidiasis patients. We detected newly selected mutations, including single-nucleotide polymorphisms (SNPs), copy-number variations and loss-of-heterozygosity (LOH) events.  LOH events were commonly associated with acquired resistance, and SNPs in 240 genes may be related to host adaptation. Conversely, most aneuploidies were transient and did not correlate with drug resistance. Our analysis also shows that isolates also varied in adherence, filamentation, and virulence. Our work reveals new molecular mechanisms underlying the evolution of drug resistance and host adaptation.
    
    | elife06003.xml        | abstract       | Lipids are critical to cellular function and it is generally accepted that lipid turnover is rapid and dysregulation in turnover results in disease (Dawidowicz 1987; Phillips et al., 2009; Liu et al., 2013). In this study, we present an intriguing counter-example by demonstrating that in the center of the human ocular lens, there is no lipid turnover in fiber cells during the entire human lifespan. This discovery, combined with prior demonstration of pronounced changes in the lens lipid composition over a lifetime (Hughes et al., 2012), suggests that some lipid classes break down in the body over several decades, whereas others are stable. Such substantial changes in lens cell membranes may play a role in the genesis of age-related eye disorders. Whether long-lived lipids are present in other tissues is not yet known, but this may prove to be important in understanding the development of age-related diseases.

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

    | elife02935.xml        | contributor        | 0       | contrib_type   | author
    | elife02935.xml        | contributor        | 33      | collab         | ICGC Breast Cancer Group
    | elife02935.xml        | contributor        | 52      | contrib_type   | author
    | elife02935.xml        | contributor        | 52      | surname        | Campbell
    | elife02935.xml        | contributor        | 53      | contrib_type   | author non-byline
    | elife02935.xml        | contributor        | 53      | surname        | Provenzano

  Scenario: Parse article XML file contributor affiliations
    Given I have the document <document>
    When I build article from xml
    And I set the object to article <property> index <index>
    And I set the object to contributor affiliation index <aff_index>
    And I have the attribute <attribute>
    Then I have object attribute value <value>
    
  Examples:
    | document              | property      | index | aff_index  | attribute      | value
    | elife00013.xml        | contributor   | 0     | 0          | text           | Department of Molecular and Cell Biology, University of California, Berkeley, Berkeley, United States
    | elife_poa_e06828.xml  | contributor   | 0     | 0          | text           | Department of Neuroscience, Perelman School of Medicine, University of Pennsylvania, Philadelphia, United States
    | elife_poa_e02923.xml  | contributor   | 0     | 0          | text           | Department of Pediatrics, University of Colorado, Anschutz Medical Campus, Aurora, United States
    | elife02935.xml        | contributor   | 0     | 0          | text           | Cancer Genome Project, Wellcome Trust Sanger Institute, Hinxton, United Kingdom
    

  Scenario: Parse article XML file dates
    Given I have the document <document>
    When I build article from xml
    And I set the object to article date type <date_type>
    And I have the attribute <attribute>
    Then I have date object attribute value <value>

  Examples:
    | document              | date_type  | attribute      | value
    | elife00013.xml        | accepted   | day            | 18
    | elife00013.xml        | accepted   | month          | 7
    | elife00013.xml        | accepted   | year           | 2012
    | elife00013.xml        | received   | day            | 22
    | elife00013.xml        | received   | month          | 5
    | elife00013.xml        | received   | year           | 2012
    | elife00013.xml        | pub        | day            | 15
    | elife00013.xml        | pub        | month          | 10
    | elife00013.xml        | pub        | year           | 2012
    
    | elife_poa_e06828.xml  | accepted   | day            | 1
    | elife_poa_e06828.xml  | accepted   | month          | 4
    | elife_poa_e06828.xml  | accepted   | year           | 2015
    | elife_poa_e06828.xml  | received   | day            | 3
    | elife_poa_e06828.xml  | received   | month          | 2
    | elife_poa_e06828.xml  | received   | year           | 2015
    | elife_poa_e06828.xml  | pub        | day            | None
    | elife_poa_e06828.xml  | pub        | month          | None
    | elife_poa_e06828.xml  | pub        | year           | None
    
    | elife_poa_e02923.xml  | accepted   | day            | 7
    | elife_poa_e02923.xml  | accepted   | month          | 1
    | elife_poa_e02923.xml  | accepted   | year           | 2015
    | elife_poa_e02923.xml  | received   | day            | 27
    | elife_poa_e02923.xml  | received   | month          | 3
    | elife_poa_e02923.xml  | received   | year           | 2014
    | elife_poa_e02923.xml  | pub        | day            | None
    | elife_poa_e02923.xml  | pub        | month          | None
    | elife_poa_e02923.xml  | pub        | year           | None

    | elife02935.xml        | accepted   | day            | 26
    | elife02935.xml        | accepted   | month          | 9
    | elife02935.xml        | accepted   | year           | 2014
    | elife02935.xml        | received   | day            | 28
    | elife02935.xml        | received   | month          | 3
    | elife02935.xml        | received   | year           | 2014
    | elife02935.xml        | pub        | day            | 1
    | elife02935.xml        | pub        | month          | 10
    | elife02935.xml        | pub        | year           | 2014
    

