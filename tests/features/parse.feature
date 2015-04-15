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
    

  Scenario: Parse article XML files
    Given I have the document <document>
    When I build article from xml
    And I have the attribute <attribute>
    Then I have article attribute value <value>
    
  Examples:
    | document              | attribute      | value  
    | elife00013.xml        | doi            | 10.7554/eLife.00013 
    | elife_poa_e06828.xml  | doi            | 10.7554/eLife.06828 
