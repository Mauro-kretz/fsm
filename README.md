# Finite State Machine (FSM) Library

## Overview

This library provides a flexible and efficient implementation of a Finite State Machine (FSM) in C. It's designed to be easily integrated into embedded systems or any C project requiring state management.

## Features

- Hierarchical state support
- Event-driven transitions
- Entry, exit, and run actions for states
- Event queue with configurable size
- Support for user-defined data associated with states and events
- Efficient implementation suitable for embedded systems

## Files

- `fsm.h`: Main header file with FSM definitions and function declarations
- `fsm.c`: Implementation of FSM functions
- `ring_buff.h`: Ring buffer implementation used for the event queue

## Key Concepts

### States

States are defined using the `fsm_state_t` structure, which includes:
- State ID
- Parent state (for hierarchical FSMs)
- Default substate
- Entry, exit, and run action function pointers

### Transitions

Transitions are defined using the `fsm_transition_t` structure, which includes:
- Source state
- Event triggering the transition
- Target state
- Transition action function pointer

You can declare a transition using the two macros available:
- FSM_TRANSITION_CREATE: creates a transition
- FSM_TRANSITION_WORK_CREATE: creates a transition with an action function.

### Events

Events are simple integers that trigger state transitions. They can be associated with user-defined data.

### Actors

Actors in this FSM implementation represent logical entities or components that manage the behavior of specific states within the system. Each actor consists of a collection of states, with each state defined by:

- **`state_id`**: A unique identifier for the state.
- **`entry_action`**: A function executed when entering the state.
- **`run_action`**: A function invoked while the state is active.
- **`exit_action`**: A function called when exiting the state.

Actors allow grouping related state behaviors and actions into cohesive units, making the FSM modular and easier to extend or modify. This design is particularly useful for systems where multiple independent or semi-independent components (e.g., a player, a menu, or a power manager) operate within the same FSM framework.

Actors enable you to perform actions when specific states are active, and these states can belong to different FSMs. By using an array of actor pointers, the FSM can efficiently manage state transitions and actions for multiple entities across different FSMs.

## Usage

### Defining States, Transitions and Actors

Use the provided macros to define states and transitions:

```c
//State table
FSM_STATES_INIT(my_fsm)
FSM_CREATE_STATE(my_fsm, STATE1, ROOT_ST, FSM_ST_NONE, enter_state1, run_state1, exit_state1)
FSM_CREATE_STATE(my_fsm, STATE2, ROOT_ST, FSM_ST_NONE, enter_state2, run_state2, exit_state2)
FSM_STATES_END()
// Transition table
FSM_TRANSITIONS_INIT(my_fsm)
FSM_TRANSITION_CREATE(my_fsm, STATE1, EVENT1, STATE2)
FSM_TRANSITION_CREATE(my_fsm, STATE2, EVENT2, STATE1)
FSM_TRANSITIONS_END()

// Actor 1
FSM_ACTOR_INIT(my_actor)
FSM_ACTOR_CREATE(my_fsm, STATE1, enter_state1_act1, run_state1_act1, NULL)
FSM_ACTOR_CREATE(my_fsm, STATE2, enter_state2_act1, run_state2_act1, NULL)
FSM_ACTOR_END()
// Actor 2
FSM_ACTOR_INIT(my_other_actor)
FSM_ACTOR_CREATE(STATE1, enter_state1_act2, run_state1_act2, NULL)
FSM_ACTOR_CREATE(STATE2, enter_state2_act2, run_state2_act2, NULL)
FSM_ACTOR_END()
```

### Initializing the FSM

```c
fsm_t my_fsm;
fsm_init(&my_fsm, my_fsm_transitions, FSM_TRANSITIONS_SIZE(my_fsm), num_events, &FSM_STATE_GET(my_fsm, INIT_ST), initial_data);
```
### Linking actor

```c
ret = fsm_actor_link(&my_fsm, FSM_ACTOR_GET(my_actor), FSM_ACTOR_SIZE(my_actor));
```

### Running the FSM

```c
while (!terminated) {
    fsm_run(&my_fsm);
}
```

### Dispatching Events

```c
fsm_dispatch(&my_fsm, EVENT1, event_data);
```

## Configuration

- `FSM_MAX_EVENTS`: Maximum number of events in the queue (default: 64)
- `MAX_HIERARCHY_DEPTH`: Maximum depth of state hierarchy (default: 8)
- `FSM_MAX_TRANSITIONS`: Maximum number of transitions that an event can trigger (default: 8)

## Best Practices

1. Keep state functions (entry, exit, run) small and focused.
2. Use hierarchical states to group related states and reduce code duplication.
3. Consider using an enum for state IDs and events for better code readability.
4. Regularly check for pending events and run the FSM to ensure responsive behavior.

## Example: Music Player State Machine

To illustrate the use of this FSM library, in the example folder theres a music player application implemented.
This state machine demonstrates several key features of the FSM library:

1. **Hierarchical States**: The `STATE_ROOT` contains `STATE_OFF`, `STATE_ON`, and `STATE_LOW_BATTERY`. `STATE_ON` further contains `STATE_PAUSED`, `STATE_PLAYING`, and `STATE_MENU`.

2. **Default Substates**: When entering `STATE_ON`, it automatically enters `STATE_PAUSED`. Similarly, `STATE_PLAYING` defaults to `STATE_NORMAL`.

3. **Multiple Transitions**: States like `STATE_MENU_HOME` have multiple possible transitions based on different events.

4. **Global Transitions**: The `EVENT_LOW_BATTERY` can trigger a transition to `STATE_LOW_BATTERY` from multiple states.

Refer to fsm_music.c to see the implementation.

## Using Mermaid for FSM Diagrams

We recommend using Mermaid for creating clear and visually appealing FSM diagrams. Mermaid is a markdown-based diagramming tool that can be easily integrated into documentation.

### Benefits of Using Mermaid

1. **Easy to Learn**: Mermaid uses a simple, text-based syntax.
2. **Version Control Friendly**: Diagrams are stored as text, making them easy to version control.
3. **Widely Supported**: Many platforms, including GitHub, support Mermaid diagrams.
4. **Interactive**: Mermaid diagrams can be made interactive, allowing users to explore complex state machines.

### Basic Mermaid Syntax for State Diagrams

```
stateDiagram-v2
    [*] --> StateA
    StateA --> StateB : SomeEvent
    StateB --> StateC : AnotherEvent
    StateC --> [*]
```

This creates a simple state diagram with three states and transitions between them.

### Tips for FSM Diagrams in Mermaid

1. Use meaningful state and event names for clarity.
2. Group related states using Mermaid's composite state feature.
3. Use comments to explain complex transitions or states.
4. Consider using different colors or styles for different types of states or transitions.

By using Mermaid to diagram your FSMs, you can easily keep your documentation in sync with your code, making it easier for developers to understand and maintain your state machines.

### Using script for building mermaid diagram
To make it easier to build your state machine diagrams, under fsm/tools there's a python script that you can use to facilitate this. 

This script takes a .c file that implemets a finite state machine using the FSM library macros:

- FSM_STATES_INIT()
- FSM_CREATE_STATE()
- FSM_TRANSITIONS_INIT()
- FSM_TRANSITION_CREATE()
    
Usage: Call script from command line 
```
    - python fsm/tools/fsm_2_mermaid file_name
```   
Where file_name is the .c file that implements the fsm (has to have FSM_CREATE_STATE and FSM_TRANSITION_CREATE somewhere)

### Using Claude AI for Assistance
To provide additional support for users of this FSM library, we recommend leveraging the capabilities of Claude AI, an advanced language model developed by Anthropic.
Claude was used to help in the library development and documentation creation process, demonstrating its capability to assist throughout the project lifecycle. 

Claude is particularly adept at creating Mermaid diagrams for Finite State Machines. You can provide Claude with your states and transition tables, and it will generate a well-structured Mermaid diagram representing your FSM. This feature can significantly streamline the process of visualizing and documenting your state machines.

## Limitations

- The library assumes that the transition table and state definitions are correctly defined by the user.
- The maximum number of events and hierarchy depth are fixed at compile-time.

## Contributing

Contributions to improve the library are welcome. Please submit pull requests or open issues on the project repository.

## License

MIT License

Copyright (c) 2024 Mauro Medina

