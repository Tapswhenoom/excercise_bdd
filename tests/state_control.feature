Feature: State Control Unit Behaviour

    Scenario: Transition from OFF to WAITING
      Given the scu state is initially OFF
      When the scu is turned on
      Then scu transitions to WAITING
    
    Scenario Outline: Transition from WAITING to VALID_REQUEST or WAITING (if valid or invalid choice)
      Given the scu state is initially WAITING
      When the user selects a coffee brewing option, ex: <number>
      Then scu transitions to <state>

      Examples:
      | number | state         |
      | 1      | VALID_REQUEST |
      | 2      | VALID_REQUEST |
      | 3      | VALID_REQUEST |
      | 4      | VALID_REQUEST |
      | f      | WAITING |
      | q      | OFF |
      | 7      | WAITING |

    Scenario: Transition from WAITING to OFF
      Given the scu state is initially WAITING
      When the scu is turned off
      Then the scu should transition to OFF


    Scenario: Transition from READY to WAITING
      Given a valid coffee choice
      And the scu receives a READY event
      When coffee is served
      Then scu transitions to WAITING