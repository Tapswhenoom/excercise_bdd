Feature: Temperature Control Unit Behavior

  Scenario: Initial state is OFF
    Given the temperature control unit is initially OFF

  Scenario: Transition to HEATING 
    Given the temperature control unit is initially OFF
    When the user starts the coffee machine
    And  the user selects a valid coffee brewing option
    Then the temperature control unit should transition to HEATING

  Scenario: Transition to READY
    Given the temperature control unit is HEATING
    When the temperature reaches the desired temperature
    Then the temperature control unit should transition to READY

  Scenario: Transition to OFF
    Given any temperature control unit state other than OFF
    When the coffee machine is turned off
    Then the temperature control unit should transition to OFF