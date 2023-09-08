Feature: Logic Control Unit Behaviour

    Scenario: Transition from OFF to WAITING
      Given the tcu is OFF
      When the coffee machine is turned on
      Then tcu transitions to WAITING
    
    Scenario: Transition from WAITING to VALID_REQUEST
      Given the tcu is WAITING
      When the user selects a valid coffee brewing option
      Then coffee machine transitions to VALID_REQUEST
    
    Scenario: Transition from VALID_REQUEST to HEATING
      Given the tcu is VALID_REQUEST
      Then coffee machine transitions to HEATING
      
    Scenario: Transition from READY to WAITING
      Given the temperature control unit state is READY
      When coffee is served
      Then temperature control unit should transition to WAITING

    Scenario: Transition from WAITING to OFF
      Given the logic control unit is WAITING
      When the coffee machine is turned off
      Then the temperature control unit should transition to OFF

    Scenario: User doesnt choose an available option
      Given the logic control unit is WAITING
      When When the user selects a invalid coffee brewing option
      Then coffee machine stays in WAITING 