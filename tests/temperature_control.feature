Feature: Temperature Control Unit Behavior

  Scenario: Initial state is OFF
    Given the temperature control unit is initially OFF

  Scenario: Transition to HEATING 
    When the temperature control unit receives an event with a temperature request
    Then the temperature control unit should transition to HEATING

  Scenario: Transition to READY
    Given the temperature control unit is initially HEATING
    When the temperature reaches the desired temperature
    Then the temperature control unit should transition to READY

  Scenario: Transition to OFF
    When the temperature control unit receives an event to turn OFF
    Then the temperature control unit should transition to OFF
  
  Scenario: Transition to OFF because waiting for request
    Given the temperature control unit is initially READY
    When the temperature control unit receives an event to wait
    Then the temperature control unit should transition to OFF

  Scenario: Transition to OFF by threads timeout
    Given the temperature control unit receives an event with a high temperature request
    When the brewing process is called
    And the brewing process timesout
    Then the temperature control unit should transition to OFF
     
  Scenario: Test water heating and sensor logic
    Given the temperature control unit receives an event with a temperature request
    When the brewing process is called
    Then water will reach the needed temp
    And the temperature control unit should transition to READY

  Scenario: Complete loop from the tcu
    Given the temperature control unit is initially OFF
    When the temperature control unit receives an event with a temperature request
    And the temperature reaches the desired temperature
    And the temperature control unit receives an event to turn OFF
    Then the temperature control unit should transition to OFF


