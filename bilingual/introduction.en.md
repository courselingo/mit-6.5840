A "distributed system": a group of computers cooperating to provide a service.

Why useful? To increase capacity via parallel processing; to tolerate faults via replication; to match distribution of physical devices e.g. sensors; to increase security via isolation.

Hard to build: concurrency; complex interactions; performance bottlenecks; partial failure.

Partial failure is the real subject of this course. A single-machine program either runs or crashes; a distributed system lives permanently in between — part of it is broken while the rest keeps serving, and both are true at the same time.

Why is it hard? Because once the system must look like one system from the outside, you are simultaneously maintaining consistency (all replicas agree), availability (some node always answers), and performance (more machines must actually be faster). Under failure these pull against each other, so every design is a trade-off among them rather than a satisfaction of all three.
