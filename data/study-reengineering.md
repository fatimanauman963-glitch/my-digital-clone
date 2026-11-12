# My Software Reengineering study notes

## What reengineering is
Software reengineering means improving or changing an existing (often legacy) system so it is easier to maintain, understand and extend, without throwing away what already works. It is usually cheaper and less risky than rewriting everything. It includes reverse engineering (understanding the existing system and recovering its design), restructuring (cleaning the code or design without changing behaviour) and forward engineering (building the improved system).

## Migration methods
When a legacy system must be moved to a new platform there are three well-known strategies.
Cold Turkey, also called the big-bang approach, replaces the whole old system with a new one at once. It is simple in concept, but risky: if the new system fails, there is nothing to fall back on, and it needs a long period of building before anything is delivered.
Chicken Little is an incremental approach. The system is migrated in small steps, and during the migration the old and new systems run side by side, connected through gateways that let them exchange data. It lowers risk, but the gateways add complexity and extra work.
Butterfly is also incremental but avoids gateways. The old data is frozen as read-only while new data is written into temporary datastores, and the new system is built up step by step. At the end the temporary stores are merged into the new system. It reduces the gateway overhead, but needs careful planning of the data.

## Wrapping
Wrapping puts a modern interface around a legacy component so the rest of the system can use it without knowing its internals. It treats the legacy part like a black box. It is a quick and cheap way to reuse old functionality, but it does not remove the problems inside the legacy code.

## Cognition models in program comprehension
To reengineer a system you first have to understand it, so I studied how programmers understand code.
Letovsky's model says a programmer has a knowledge base, builds a mental model of the program, and has an assimilation process that connects the two. The programmer asks questions about the code, forms conjectures and searches for answers, using both top-down and bottom-up thinking.
Shneiderman and Mayer's model separates syntactic knowledge (language details) from semantic knowledge (what the program means). Programmers build up the meaning by grouping code into chunks and forming a higher-level internal representation.
The model of Soloway and his colleagues focuses on programming plans, which are stereotyped solutions to common goals, and on rules of discourse, which are programming conventions. Programmers understand code by recognising these plans and by checking whether the code follows the expected conventions.

## Why this matters
A good reengineering effort combines a suitable migration strategy with a realistic understanding of how people comprehend programs, because the biggest cost in maintenance is usually the time people spend understanding the code.
