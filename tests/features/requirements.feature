Feature: Use python imports and requirements
  In order to use python
  As a user
  I want to import packages
  
  Scenario: Import python packages by name
    Given I have the package name <package_name>
    When I import the package
    Then I get the package with name <package_name>

  Examples:
    | package_name
    | git
    | elementtree
    | generatePoaXml
    | xml_generation
    | parseCSVFiles
    | settings
    | lxml
    | requests