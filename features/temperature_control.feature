Feature: Temperature Control Unit Behavior
  Background:
    Given the temperature control unit is initially OFF

  Scenario: Transition from OFF to IDLE
    When user turns ON the machine
    Then the machine is switeched to IDLE

 
  Scenario Outline: Transition from IDLE to HEATING
    Given machine in IDLE 
    When the user selects a coffee <option>
    Then the machine is switeched to HEATING
   
    Examples:

       | option        | 
       | Espresso      | 
       | Cappuccino    | 
       | Latte         | 
       | Black_Coffee  | 

  Scenario: Transition from HEATING to READY
    Given machine in HEATING 
    When once target temperature is reashed
    Then the machine is switeched to READY
  
  Scenario: Transition from HEATING to ERROR
    Given machine in HEATING 
    When target temperature is not reached 
    And  timeout reached
    Then the machine is switeched to ERROR
    
  Scenario: Transition from ERROR to IDLE
    Given machine in ERROR 
    When user dismiss the error 
    Then the machine is switeched to IDLE


  Scenario: Transition from READY to IDLE
    Given machine in READY 
    When operation finished 
    Then the machine is switeched to IDLE

  Scenario: Transition from IDLE to OFF
    Given machine in IDLE 
    When user turn off the machine
    Then the machine is switeched to OFF 

    
 Scenario Outline: Transition to OFF
    Given machine in <state> 
    When user turn off the machine
    Then the machine is switeched to OFF 
   
    Examples:

       | state   | 
       | IDLE    | 
       | HEATING | 
       | READY   | 
       | ERROR   | 
       | OFF     |

# -----------------------------------------------path testing-----------------------------
 Scenario Outline: Normal Operation-Successful Heating
    # Given the temperature control unit is initially OFF
    When user turns ON the machine
    And the user selects a coffee <option>
    And once target temperature is reashed
    And operation finished
    Then the machine is switeched to IDLE
  
  Examples:

       | option  |
       | Espresso | 

  Scenario Outline: Timeout During Heating
    # Given the temperature control unit is initially OFF
    When user turns ON the machine
    And the user selects a coffee <option>
    And target temperature is not reached 
    And timeout reached
    And user dismiss the error
    Then the machine is switeched to IDLE
  
  
  Examples:

       | option  |
       | Espresso | 

  Scenario Outline: Immediate Turn Off
    # Given the temperature control unit is initially OFF
    When user turns ON the machine
    And the user selects a coffee <option>
    And user turn off the machine
    Then the machine is switeched to OFF
    
    Examples:

       | option  |
       | Espresso | 

  Scenario Outline: Transition from Error After Handling
    Given the temperature control unit is initially OFF
    When user turns ON the machine
    And the user selects a coffee <option1>
    And once target temperature is reashed
    And operation finished
    And the user selects a coffee <option2>
    And target temperature is not reached 
    And timeout reached
    And user dismiss the error 
    Then the machine is switeched to IDLE 
        
    Examples:

       | option1  | option2|
       | Espresso | Cappuccino|
     

@negative
Scenario: Choosing an Invalid Option
    Given machine in IDLE
    When user choose an invalid option "xxxxx"
    Then the machine should not make the caffee 
