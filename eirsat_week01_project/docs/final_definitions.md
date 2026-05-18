\# Final Definitions



\## Event Matching

A predicted event is counted as matched to a ground-truth event if the predicted event time window and ground-truth event time window overlap by any amount.



\## EventF1

EventF1 is computed from event-level precision and recall, where each matched event contributes a true positive according to the overlap rule.



\## Mean Detection Delay (MDD)

MDD is computed as:



`predicted\_event\_start - ground\_truth\_event\_start`



Negative MDD values indicate early-alarm behavior.



\## False Alarm Burden (FAB)

FAB is the count of unmatched predicted events in the evaluated run window.



\## Chronological Split Policy

All splits are chronological and leakage-safe:

\- train before val

\- val before test

\- no random shuffling across split boundaries



\## No Inflated Scoring

Point adjustment is not used. Point alarms are converted into predicted events, and scoring is performed only at the event level using the defined overlap rule.

