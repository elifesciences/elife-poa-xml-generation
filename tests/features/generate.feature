Feature: Generate POA XML
  In order to generate XML
  As a user
  I want to use the XML generation libraries

  Scenario: Check settings exist and their value
    Given I have settings
    When I read settings <property>
    Then I have the value <value>
    
  Examples:
    | property                                    | value
    | ROWS_WITH_COLNAMES                          | 3
    | LESS_THAN_ESCAPE_SEQUENCE                   | LTLT
    | GREATER_THAN_ESCAPE_SEQUENCE                | GTGT

  Scenario: Override settings values
    Given I have settings
    When I set settings <property> to <value>
    And I read settings <property>
    Then I have the value <value>
    
  Examples:
    | property                                    | value
    | LESS_THAN_ESCAPE_SEQUENCE                   | foo

  Scenario: Test entity to unicode conversion
    Given I have the string <string>
    When I convert the string with entities to unicode
    Then I have the unicode <unicode>

  Examples:
    | string                                      | unicode
    | muffins                                     | muffins
    | Coffe Ho&#x00FC;se                          | Coffe Hoüse
    | Edit&#x00F3;rial&#x00F3; Department&#x00F3; | Editórialó Departmentó
    
  Scenario: Angle bracket escape sequence conversion
    Given I have the string <string>
    And I reload settings
    When I decode the string with decode brackets
    Then I have the decoded string <decoded_string>
    
  Examples:
    | string                                      | decoded_string
    | LTLT                                        | <
    | GTGT                                        | >
    | LTLTGTGT                                    | <>
    | LTLTiGTGTeyeLTLT/iGTGT                      | <i>eye</i>