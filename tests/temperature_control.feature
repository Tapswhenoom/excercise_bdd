Feature: Temperature Control Unit Behavior

  Scenario: Initial state is OFF
    Given the temperature control unit is initially OFF

  Scenario: Transition to HEATING
    Given the temperature control unit is initially OFF
    When the user selects a coffee brewing option
    Then the temperature control unit should transition to HEATING
  
  Scenario: Transition to READY
    Given the temperature control unit is HEATING
    When the water reached the desired temperature
    Then the temperature control unit should transition to READY
  
  Scenario: Two coffees change nothing
    Given the temperature control unit is HEATING
    When the user selects a coffee brewing option
    Then the temperature control unit should remain in HEATING
